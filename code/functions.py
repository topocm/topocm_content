import itertools
import collections
import cmath
import tinyarray as ta
import numpy as np
import holoviews as hv
from types import SimpleNamespace
import kwant
from copy import copy
from wraparound import wraparound

__all__ = ['spectrum', 'plot_bands', 'h_k', 'pauli', 'update']


pauli = SimpleNamespace(s0=np.array([[1., 0.], [0., 1.]]),
                        sx=np.array([[0., 1.], [1., 0.]]),
                        sy=np.array([[0., -1j], [1j, 0.]]),
                        sz=np.array([[1., 0.], [0., -1.]]))

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

def update(p, **kwargs):
    "Simple function that updates a SimpleNamespace"
    for key, val in kwargs.items():
        p.__dict__[key] = val
    return p


def spectrum(sys, p, k_x=None, k_y=None, k_z=None, xdim='x', ydim='y',
             xticks=None, yticks=None, xlims=None, ylims=None):
    """Function that plots a spectrum for a varying parameter.

    Parameters:
    -----------
    sys : kwant.Builder object
        The un-finalized (in)finite system.
    xdim : holoviews.Dimension or string
        The label of the x-axis.
    ydim : holoviews.Dimension or string
        The label of the y-axis.
    xticks : list
        List of xticks.
    yticks : list
        List of yticks.
    xlims : tupple
        Upper and lower plot limit of the x-axis. If None the upper and lower
        limit of the xticks are used.
    ylims : tupple
        Upper and lower plot limit of the y-axis. If None the upper and lower
        limit of the xticks are used.
    kwargs : dict
        All the parameters that are used in sys. The parameter that is
        a numpy array or a list will be calculated for each value and plotted
        on the x-axis.

    Returns:
    --------
    plot : holoviews.Path object
        Plot of varying parameter vs. spectrum.
    """
    pars = copy(p)
    dimensionality = sys.symmetry.num_directions
    if dimensionality > 0:
        sys = wraparound(sys).finalized()
    else:
        sys = sys.finalized()

    k_x = 0 if k_x is None and dimensionality > 0 else k_x
    k_y = 0 if k_y is None and dimensionality > 0 else k_y
    k_z = 0 if k_z is None and dimensionality > 0 else k_z

    momenta = {'k_x': k_x, 'k_y': k_y, 'k_z': k_z}.items()

    for key, value in itertools.chain(pars.__dict__.items(), momenta):
        try:
            if len(value) > 0:
                changing_variable = key
                changing_values = value
        except TypeError:
            pass

    def energy(x):
        pars.__dict__[changing_variable] = x
        H = sys.hamiltonian_submatrix([pars, x][:dimensionality + 1])
        return np.linalg.eigvalsh(H)

    spectrum = np.array([energy(x) for x in changing_values])

    plot = hv.Path((changing_values, spectrum), kdims=[xdim, ydim])

    ticks = {}
    if isinstance(xticks, collections.Iterable):
        ticks['xticks'] = list(xticks)
    elif xticks is None:
        pass
    else:
        ticks['xticks'] = xticks

    if isinstance(yticks, collections.Iterable):
        ticks['yticks'] = list(yticks)
    elif isinstance(yticks, int):
        ticks['yticks'] = yticks

    xlims = slice(*xlims) if xlims is not None else slice(None)
    ylims = slice(*ylims) if ylims is not None else slice(None)

    return plot[xlims, ylims](plot=ticks)


def h_k(sys, p, momentum):
    """Function that returns the momentum of a kwant system as a momentum.

    Parameters:
    -----------
    sys : kwant.Builder object
        The un-finalized infinite kwant system.
    p : SimpleNamespace object
        A simple container that is used to store Hamiltonian parameters.
    momentum : float
        Momentum value in units of lattice constants.
    Returns:
    --------
    plot : holoviews.Path object
        Plot of varying parameter vs. spectrum.
    """
    sys = sys.finalized()
    h = sys.cell_hamiltonian(args=[p])
    t_rect = sys.inter_cell_hopping(args=[p])
    t = np.empty(h.shape, dtype=complex)
    t[:, :t_rect.shape[1]] = t_rect
    t[:, t_rect.shape[1]:] = 0
    t *= np.exp(1j * momentum)
    return h + t + t.T.conj()


def plot_bands(lead, p, momenta=None):
    """Function that plots a spectrum for a varying parameter.

    Parameters:
    -----------
    lead : kwant.builder.(In)finiteSystem object
        The finalized (in)finite system.
    p : SimpleNamespace object
        A simple container that is used to store Hamiltonian parameters.
    momentum : numpy array
        Range of momenta.

    Returns:
    --------
    plot : holoviews.Path object
        Plot of momentum vs. spectrum.
    """
    if momenta is None:
        pi_ticks = True
        momenta = np.linspace(-np.pi, np.pi)
        xticks = [(-np.pi, r'$-\pi$'), (0, '0'), (np.pi, r'$\pi$')]
    else:
        pi_ticks = False
    bands = kwant.physics.Bands(lead, args=[p])
    evs = np.array([bands(k=k) for k in momenta])
    plot = hv.Path((momenta, evs), kdims=[r'$k$', r'$E$'])

    if pi_ticks:
        return plot(plot={'xticks': xticks})
    else:
        return plot
