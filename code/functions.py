import itertools
import collections
from copy import copy
from types import SimpleNamespace

import kwant
import numpy as np
import holoviews as hv

__all__ = ['spectrum', 'hamiltonian_array', 'pauli']

pauli = dict(s0=np.array([[1., 0.], [0., 1.]]),
             sx=np.array([[0., 1.], [1., 0.]]),
             sy=np.array([[0., -1j], [1j, 0.]]),
             sz=np.array([[1., 0.], [0., -1.]]))

for first, second in itertools.product(pauli.items(), pauli.items()):
    pauli[first[0] + second[0]] = np.kron(first[1], second[1])

pauli = SimpleNamespace(**pauli)


def hamiltonian_array(syst, params):
    """Evaluate the Hamiltonian of a system over a grid of parameters.

    Parameters
    ----------
    syst : kwant.System or a callable
    params : dict
        A container of Hamiltonian parameters. The parameters that are
        sequences with length larger than 1 are used to loop over.

    Returns
    -------
    hamiltonians : numpy.ndarray
        An array with the Hamiltonians. The first n-2 dimensions correspond to
        the expanded variables.

    Examples
    --------
    >>> hamiltonian_array(syst, dict(t=1, mu=np.linspace(-2, 2),
    ...                              k_x=np.linspace(-np.pi, np.pi)))

    """
    if isinstance(syst, kwant.system.System):
        def ham(**kwargs):
            return syst.hamiltonian_submatrix(params=kwargs, sparse=False)
    else:
        ham = syst

    ham = np.vectorize(
        ham,
        signature = ','.join(['()'] * len(params)) + '->(n,n)'
    )

    return ham(**params)


def spectrum(
    syst, params, title=None, xdim=None,
    ydim=None, zdim=None, xticks=None, yticks=None, zticks=None,
    xlims=None, ylims=None, zlims=None, num_bands=None, return_energies=False
):
    """Plot system spectrum for varying parameters or momenta.

    Parameters:
    -----------
    syst : kwant.Builder object
        The un-finalized (in)finite system.
    p : SimpleNamespace object
        A container used to store Hamiltonian parameters. The parameters that
        are sequences are used as plot axes.
    title : function or str
        Function that takes params as argument and returns the title.
        If a string it's used as static title.
    xdim, ydim, zdim : holoviews.Dimension or string
        The labels of the axes. Default to best guess.
    xticks, yticks zticks : list
        Lists of axes xticks, extra ones are ignored.
    xlims, ylims, zlims : tuple
        Upper and lower plot limit of the axes. If None the upper and lower
        limits of the ticks are used. Extra ones are ignored.
    num_bands : int
        Number of bands near the middle that should be plotted.
    return_energies : bool
        If True the function only returns the energies in an array.

    Returns:
    --------
    plot : holoviews plot object
        Plot of varying parameter vs. spectrum.
    """
    pi_ticks = [(-np.pi, r'$-\pi$'), (0, '$0$'), (np.pi, r'$\pi$')]
    if params is None:
        params = dict()

    # Add momenta to parameters
    dimensionality = syst.symmetry.num_directions
    momenta_keys = 'k_x k_y k_z'.split()[:dimensionality]
    momenta = {
        k: params.get(k, np.linspace(-np.pi, np.pi, 101))
        for k in momenta_keys
    }
    params = {**momenta, **params}

    hamiltonians = hamiltonian_array(syst, params=params)

    energies = np.linalg.eigvalsh(hamiltonians)

    constants = {
        k: v for k, v in
    }
    if len(variables) == 0:
        raise ValueError("A 0D plot requested")

    if num_bands is not None:
        mid = energies.shape[-1] // 2
        to_take = (
            (slice(None),) * (len(energies.shape) - 1)
            + (slice(mid - num_bands//2, mid + num_bands//2),)
        )
        energies = energies[to_take]

    if return_energies:
        return energies

    elif len(variables) == 1:
        # 1D plot.
        if xdim is None:
            if variables[0][0] in momenta_keys:
                xdim = r'${}$'.format(variables[0][0])
            else:
                xdim = variables[0][0]
        if ydim is None:
            ydim = r'$E$'

        plot = hv.Path((variables[0][1], energies), kdims=[xdim, ydim])

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

        if callable(title):
            plot = plot.relabel(title(**params))
        elif isinstance(title, str):
            plot = plot.relabel(title)

        return plot[xlims, ylims].opts(plot={'Path': ticks})

    elif len(variables) == 2:
        # 2D plot.
        style = {}
        if xticks is None and variables[0][0] in momenta_keys:
            style['xticks'] = pi_ticks
        elif xticks is not None:
            style['xticks'] = list(xticks)
        if yticks is None and variables[1][0] in momenta_keys:
            style['yticks'] = pi_ticks
        elif yticks is not None:
            style['yticks'] = list(yticks)

        if xdim is None:
            if variables[0][0] in momenta_keys:
                xdim = r'${}$'.format(variables[0][0])
            else:
                xdim = variables[0][0]
        if ydim is None:
            if variables[1][0] in momenta_keys:
                ydim = r'${}$'.format(variables[1][0])
            else:
                ydim = variables[1][0]
        if zdim is None:
            zdim = r'$E$'

        if zticks is not None:
            style['zticks'] = zticks

        if xlims is None:
            xlims = np.round([min(variables[0][1]), max(variables[0][1])], 2)
        if ylims is None:
            ylims = np.round([min(variables[1][1]), max(variables[1][1])], 2)
        if zlims is None:
            zlims = (None, None)

        kwargs = {'extents': (xlims[0], ylims[0], zlims[0],
                              xlims[1], ylims[1], zlims[1]),
                  'kdims': [xdim, ydim],
                  'vdims': [zdim]}

        plot = hv.Overlay(
            [
                hv.Surface(energies[:, :, i], **kwargs)(plot=style)
                for i in range(energies.shape[-1])
            ]
        )

        if callable(title):
            plot = plot.relabel(title(p))
        elif isinstance(title, str):
            plot = plot.relabel(title)

        return plot.opts(plot={'Overlay': {'fig_size': 200}})

    else:
        raise ValueError("Cannot make 4D plots yet.")
