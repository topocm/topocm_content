# Copyright 2016 Christoph Groth (INAC / CEA Grenoble).
#
# This file is subject to the 2-clause BSD license as found at
# http://kwant-project.org/license.

"""Replace symmetries of Kwant builders with momentum parameters to the
system."""

import sys
import itertools
import collections
import cmath
import numpy as np
import tinyarray as ta

import kwant
from kwant.builder import herm_conj


if sys.version_info >= (3, 0):
    def _hashable(obj):
        return isinstance(obj, collections.Hashable)
else:
    def _hashable(obj):
        return (isinstance(obj, collections.Hashable)
                and not isinstance(obj, np.ndarray))


def _memoize(f):
    """Decorator to memoize a function that works even with unhashable args.

    This decorator will even work with functions whose args are not hashable.
    The cache key is made up by the hashable arguments and the ids of the
    non-hashable args.  It is up to the user to make sure that non-hashable
    args do not change during the lifetime of the decorator.

    This decorator will keep reevaluating functions that return None.
    """
    def lookup(*args):
        key = tuple(arg if _hashable(arg) else id(arg) for arg in args)
        result = cache.get(key)
        if result is None:
            cache[key] = result = f(*args)
        return result
    cache = {}
    return lookup


def wraparound(builder, keep=None):
    """Replace translational symmetries by momentum parameters.

    A new Builder instance is returned.  By default, each symmetry is replaced
    by one scalar momentum parameter that is appended to the already existing
    arguments of the system.  Optionally, one symmetry may be kept by using the
    `keep` argument.
    """

    @_memoize
    def bind_site(val):
        assert callable(val)
        return lambda a, *args: val(a, *args[:mnp])

    @_memoize
    def bind_hopping_as_site(elem, val):
        def f(a, *args):
            phase = cmath.exp(1j * ta.dot(elem, args[mnp:]))
            v = val(a, sym.act(elem, a), *args[:mnp]) if callable(val) else val
            pv = phase * v
            return pv + herm_conj(pv)
        return f

    @_memoize
    def bind_hopping(elem, val):
        def f(a, b, *args):
            phase = cmath.exp(1j * ta.dot(elem, args[mnp:]))
            v = val(a, sym.act(elem, b), *args[:mnp]) if callable(val) else val
            return phase * v
        return f

    @_memoize
    def bind_sum(*vals):
        return lambda *args: sum((val(*args) if callable(val) else val)
                                 for val in vals)

    if keep is None:
        ret = kwant.Builder()
        sym = builder.symmetry
    else:
        periods = list(builder.symmetry.periods)
        ret = kwant.Builder(kwant.TranslationalSymmetry(periods.pop(keep)))
        sym = kwant.TranslationalSymmetry(*periods)

    mnp = -len(sym.periods)      # Used by the bound functions above.

    # Store lists of values, so that multiple values can be assigned to the
    # same site or hopping.
    for site, val in builder.site_value_pairs():
        ret[site] = [bind_site(val) if callable(val) else val]

    for hop, val in builder.hopping_value_pairs():
        a, b = hop
        b_dom = sym.which(b)
        b_wa = sym.act(-b_dom, b)

        if a == b_wa:
            # The hopping gets wrapped-around into an onsite Hamiltonian.
            # Since site `a` already exists in the system, we can simply append.
            ret[a].append(bind_hopping_as_site(b_dom, val))
        else:
            # The hopping remains a hopping.
            if b != b_wa or callable(val):
                # The hopping got wrapped-around or is a function.
                val = bind_hopping(b_dom, val)

            if (a, b_wa) in ret:
                ret[a, b_wa].append(val)
            else:
                ret[a, b_wa] = [val]

    # Convert lists of more than one element into summing functions.
    summed_vals = {}
    for site_or_hop, vals in itertools.chain(ret.site_value_pairs(),
                                     ret.hopping_value_pairs()):
        ret[site_or_hop] = vals[0] if len(vals) == 1 else bind_sum(*vals)

    return ret


def plot_bands_2d(syst, args=(), momenta=(31, 31)):

    """Plot the bands of a system with two wrapped-around symmetries."""
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import pyplot

    if not isinstance(syst, kwant.system.FiniteSystem):
        raise TypeError("Need a system without symmetries.")

    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    kxs = np.linspace(-np.pi, np.pi, momenta[0])
    kys = np.linspace(-np.pi, np.pi, momenta[1])

    energies = [[np.sort(np.linalg.eigvalsh(syst.hamiltonian_submatrix(
        args + (kx, ky), sparse=False)).real)
                 for ky in kys] for kx in kxs]
    energies = np.array(energies)

    mesh_x, mesh_y = np.meshgrid(kxs, kys)
    for i in range(energies.shape[-1]):
        ax.plot_wireframe(mesh_x, mesh_y, energies[:, :, i],
                          rstride=1, cstride=1)

    pyplot.show()


def _simple_syst(lat, E=0, t=1):
    """Create a builder for a simple infinite system."""
    sym = kwant.TranslationalSymmetry(lat.vec((1, 0)), lat.vec((0, 1)))
    # Build system with 2d periodic BCs. This system cannot be finalized in
    # Kwant <= 1.2.
    syst = kwant.Builder(sym)
    syst[lat.shape(lambda p: True, (0, 0))] = E
    syst[lat.neighbors(1)] = t
    return syst


def test_consistence_with_bands(kx=1.9, nkys=31):
    kys = np.linspace(-np.pi, np.pi, nkys)
    for lat in [kwant.lattice.honeycomb(), kwant.lattice.square()]:
        syst = _simple_syst(lat)
        wa_keep_1 = wraparound(syst, keep=1).finalized()
        wa_keep_none = wraparound(syst).finalized()

        bands = kwant.physics.Bands(wa_keep_1, (kx,))
        energies_a = [bands(ky) for ky in
                      (kys if kwant.__version__ > "1.0" else reversed(kys))]

        energies_b = []
        for ky in kys:
            H = wa_keep_none.hamiltonian_submatrix((kx, ky), sparse=False)
            evs = np.sort(np.linalg.eigvalsh(H).real)
            energies_b.append(evs)

        np.testing.assert_almost_equal(energies_a, energies_b)


def test_value_types(k=(-1.1, 0.5), E=0, t=1):
    for lat in [kwant.lattice.honeycomb(), kwant.lattice.square()]:
        syst = wraparound(_simple_syst(lat, E, t)).finalized()
        H = syst.hamiltonian_submatrix(k, sparse=False)
        for E1, t1 in [(float(E), float(t)),
                       (np.array([[E]], float), np.array([[1]], float)),
                       (ta.array([[E]], float), ta.array([[1]], float))]:
            for E2 in [E1, lambda a: E1]:
                for t2 in [t1, lambda a, b: t1]:
                    syst = wraparound(_simple_syst(lat, E2, t2)).finalized()
                    H_alt = syst.hamiltonian_submatrix(k, sparse=False)
                    np.testing.assert_equal(H_alt, H)


def test():
    test_consistence_with_bands()
    test_value_types()


def demo():
    """Calculate and plot the band structure of graphene."""
    lat = kwant.lattice.honeycomb()
    syst = wraparound(_simple_syst(lat)).finalized()
    plot_bands_2d(syst)


if __name__ == '__main__':
    test()
    demo()
