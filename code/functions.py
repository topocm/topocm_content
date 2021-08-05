import collections
import itertools
from copy import copy
from types import SimpleNamespace

import holoviews as hv
import kwant
import numpy as np

if tuple(int(i) for i in np.__version__.split(".")[:3]) <= (1, 8, 0):
    raise RuntimeError("numpy >= (1, 8, 0) is required")

__all__ = ["spectrum", "hamiltonian_array", "h_k", "pauli"]

pauli = SimpleNamespace(
    s0=np.array([[1.0, 0.0], [0.0, 1.0]]),
    sx=np.array([[0.0, 1.0], [1.0, 0.0]]),
    sy=np.array([[0.0, -1j], [1j, 0.0]]),
    sz=np.array([[1.0, 0.0], [0.0, -1.0]]),
)

pauli.s0s0 = np.kron(pauli.s0, pauli.s0)
pauli.s0sx = np.kron(pauli.s0, pauli.sx)
pauli.s0sy = np.kron(pauli.s0, pauli.sy)
pauli.s0sz = np.kron(pauli.s0, pauli.sz)
pauli.sxs0 = np.kron(pauli.sx, pauli.s0)
pauli.sxsx = np.kron(pauli.sx, pauli.sx)
pauli.sxsy = np.kron(pauli.sx, pauli.sy)
pauli.sxsz = np.kron(pauli.sx, pauli.sz)
pauli.sys0 = np.kron(pauli.sy, pauli.s0)
pauli.sysx = np.kron(pauli.sy, pauli.sx)
pauli.sysy = np.kron(pauli.sy, pauli.sy)
pauli.sysz = np.kron(pauli.sy, pauli.sz)
pauli.szs0 = np.kron(pauli.sz, pauli.s0)
pauli.szsx = np.kron(pauli.sz, pauli.sx)
pauli.szsy = np.kron(pauli.sz, pauli.sy)
pauli.szsz = np.kron(pauli.sz, pauli.sz)


def spectrum(
    syst,
    p=None,
    k_x=None,
    k_y=None,
    k_z=None,
    title=None,
    xdim=None,
    ydim=None,
    zdim=None,
    xticks=None,
    yticks=None,
    zticks=None,
    xlims=None,
    ylims=None,
    zlims=None,
    num_bands=None,
    return_energies=False,
):
    """Function that plots system spectrum for varying parameters or momenta.

    Parameters:
    -----------
    syst : kwant.Builder object
        The un-finalized (in)finite system.
    p : dictionary
        A container used to store Hamiltonian parameters. The parameters that
        are sequences are used as plot axes.
    k_x, k_y, k_z : floats or sequences of floats
        Real space momenta at which the Hamiltonian has to be evaluated.
        If the system dimensionality is low, extra momenta are ignored.
    title : function or str
        Function that takes p as argument and generates a string. If a string
        it's used as static title.
    xdim, ydim, zdim : holoviews.Dimension or string
        The labels of the axes. Default to best guess, and extra ones
        are ignored.
    xticks, yticks zticks : list
        Lists of axes xticks, extra ones are ignored.
    xlims, ylims, zlims : tuple
        Upper and lower plot limit of the axes. If None the upper and lower
        limits of the ticks are used. Extra ones are ignored.
    num_bands : int
        Number of bands that should be plotted, only works for 2D plots. If
        None all bands are plotted.
    return_energies : bool
        If True the function only returns the energies in an array.

    Returns:
    --------
    plot : holoviews.Path object
        Plot of varying parameter vs. spectrum.
    """
    pi_ticks = [(-np.pi, r"$-\pi$"), (0, "$0$"), (np.pi, r"$\pi$")]
    if p is None:
        p = dict()
    dimensionality = syst.symmetry.num_directions
    k = [k_x, k_y, k_z]
    k = [(np.linspace(-np.pi, np.pi, 101) if i is None else i) for i in k]
    k = [(i if j < dimensionality else 0) for (j, i) in enumerate(k)]
    k_x, k_y, k_z = k

    hamiltonians, variables = hamiltonian_array(syst, p, k_x, k_y, k_z, True)
    # Don't waste effort calculating eigenvalues if we aren't going to plot
    # anything.
    if len(variables) in (1, 2):
        energies = np.linalg.eigvalsh(hamiltonians)

    if len(variables) == 0:
        raise ValueError("A 0D plot requested")

    if return_energies:
        return energies

    elif len(variables) == 1:
        # 1D plot.
        if xdim is None:
            if variables[0][0] in "k_x k_y k_z".split():
                xdim = r"${}$".format(variables[0][0])
            else:
                xdim = variables[0][0]
        if ydim is None:
            ydim = r"$E$"

        plot = hv.Path((variables[0][1], energies), kdims=[xdim, ydim])

        ticks = {}
        if isinstance(xticks, collections.abc.Iterable):
            ticks["xticks"] = list(xticks)
        elif xticks is None:
            pass
        else:
            ticks["xticks"] = xticks

        if isinstance(yticks, collections.abc.Iterable):
            ticks["yticks"] = list(yticks)
        elif isinstance(yticks, int):
            ticks["yticks"] = yticks

        xlims = tuple(xlims) if xlims is not None else (None, None)
        ylims = tuple(ylims) if ylims is not None else (None, None)

        if callable(title):
            plot = plot.relabel(title(p))
        elif isinstance(title, str):
            plot = plot.relabel(title)

        return plot.redim.range(**{xdim: xlims, ydim: ylims}).opts(plot={"Path": ticks})

    elif len(variables) == 2:
        # 2D plot.
        style = {}
        if xticks is None and variables[0][0] in "k_x k_y k_z".split():
            style["xticks"] = pi_ticks
        elif xticks is not None:
            style["xticks"] = list(xticks)
        if yticks is None and variables[1][0] in "k_x k_y k_z".split():
            style["yticks"] = pi_ticks
        elif yticks is not None:
            style["yticks"] = list(yticks)

        if xdim is None:
            if variables[0][0] in "k_x k_y k_z".split():
                xdim = r"${}$".format(variables[0][0])
            else:
                xdim = variables[0][0]
        if ydim is None:
            if variables[1][0] in "k_x k_y k_z".split():
                ydim = r"${}$".format(variables[1][0])
            else:
                ydim = variables[1][0]
        if zdim is None:
            zdim = r"$E$"

        if zticks is not None:
            style["zticks"] = zticks

        if xlims is None:
            xlims = np.round([min(variables[0][1]), max(variables[0][1])], 2)
        if ylims is None:
            ylims = np.round([min(variables[1][1]), max(variables[1][1])], 2)
        if zlims is None:
            zlims = (None, None)

        kwargs = {
            "extents": (xlims[0], ylims[0], zlims[0], xlims[1], ylims[1], zlims[1]),
            "kdims": [xdim, ydim],
            "vdims": [zdim],
        }

        xs = np.linspace(*xlims, energies.shape[1])
        ys = np.linspace(*ylims, energies.shape[0])

        if num_bands is None:
            plot = hv.Overlay(
                [
                    hv.Surface((xs, ys, energies[:, :, i]), **kwargs).opts(plot=style)
                    for i in range(energies.shape[-1])
                ]
            )
        else:
            mid = energies.shape[-1] // 2
            num_bands //= 2
            plot = hv.Overlay(
                [
                    hv.Surface((xs, ys, energies[:, :, i]), **kwargs).opts(plot=style)
                    for i in range(mid - num_bands, mid + num_bands)
                ]
            )

        if callable(title):
            plot = plot.relabel(title(p))
        elif isinstance(title, str):
            plot = plot.relabel(title)

        return plot.opts(plot={"Overlay": {"fig_size": 200}})

    else:
        raise ValueError("Cannot make 4D plots yet.")


def h_k(syst, p, momentum):
    """Function that returns the Hamiltonian of a kwant 1D system as a momentum.
    """
    return hamiltonian_array(syst, p, momentum)[0]


def hamiltonian_array(syst, params=None, k_x=0, k_y=0, k_z=0, return_grid=False):
    """Evaluate the Hamiltonian of a system over a grid of parameters.

    Parameters:
    -----------
    syst : kwant.Builder object
        The un-finalized kwant system whose Hamiltonian is calculated.
    params : dictionary
        A container of Hamiltonian parameters. The parameters that are
        sequences are used to loop over.
    k_x, k_y, k_z : floats or sequences of floats
        Momenta at which the Hamiltonian has to be evaluated.  If the system
        only has 1 translation symmetry, only `k_x` is used, and interpreted as
        lattice momentum. Otherwise the momenta are in reciprocal space.
    return_grid : bool
        Whether to also return the names of the variables used for expansion,
        and their values.

    Returns:
    --------
    hamiltonians : numpy.ndarray
        An array with the Hamiltonians. The first n-2 dimensions correspond to
        the expanded variables.
    parameters : list of tuples
        Names and ranges of values that were used in evaluation of the
        Hamiltonians.

    Examples:
    ---------
    >>> hamiltonian_array(syst, dict(t=1, mu=np.linspace(-2, 2)),
    ...                   k_x=np.linspace(-np.pi, np.pi))
    >>> hamiltonian_array(sys_2d, p, np.linspace(-np.pi, np.pi),
    ...                   np.linspace(-np.pi, np.pi))

    """
    # Prevent accidental mutation of input
    params = copy(params)

    try:
        space_dimensionality = syst.symmetry.periods.shape[-1]
    except AttributeError:
        space_dimensionality = 0
    dimensionality = syst.symmetry.num_directions

    if dimensionality == 0:
        syst = syst.finalized()

        def momentum_to_lattice(k):
            return {}

    else:
        if len(syst.symmetry.periods) == 1:

            def momentum_to_lattice(k):
                if any(k[dimensionality:]):
                    raise ValueError("Dispersion is 1D, but more momenta are provided.")
                return {"k_x": k[0]}

        else:
            B = np.array(syst.symmetry.periods).T
            A = B @ np.linalg.inv(B.T @ B)

            def momentum_to_lattice(k):
                lstsq = np.linalg.lstsq(A, k[:space_dimensionality], rcond=-1)
                k, residuals = lstsq[:2]
                if np.any(abs(residuals) > 1e-7):
                    raise RuntimeError(
                        "Requested momentum doesn't correspond"
                        " to any lattice momentum."
                    )
                return dict(zip(["k_x", "k_y", "k_z"], list(k)))

        syst = kwant.wraparound.wraparound(syst).finalized()

    changing = dict()
    for key, value in params.items():
        if isinstance(value, collections.abc.Iterable):
            changing[key] = value

    for key, value in [("k_x", k_x), ("k_y", k_y), ("k_z", k_z)]:
        if key in changing:
            raise RuntimeError(
                "One of the system parameters is {}, "
                "which is reserved for momentum. "
                "Please rename it.".format(key)
            )
        if isinstance(value, collections.abc.Iterable):
            changing[key] = value


    def hamiltonian(**values):
        k = [values.pop("k_x", k_x), values.pop("k_y", k_y), values.pop("k_z", k_z)]
        params.update(values)
        k = momentum_to_lattice(k)
        system_params = {**params, **k}
        return syst.hamiltonian_submatrix(params=system_params, sparse=False)

    names, values = zip(*sorted(changing.items()))


    hamiltonians = [
        hamiltonian(**dict(zip(names, value))) for value in itertools.product(*values)
    ] if changing else [
        hamiltonian(k_x=k_x, k_y=k_y, k_z=k_z)
    ]
    size = list(hamiltonians[0].shape)

    hamiltonians = np.array(hamiltonians).reshape(
        [len(value) for value in values] + size
    )

    if return_grid:
        return hamiltonians, list(zip(names, values))
    else:
        return hamiltonians
