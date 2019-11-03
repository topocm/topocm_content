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
    syst, params, title=None,
    num_bands=None, return_energies=False
):
    """Plot system spectrum for varying parameters or momenta.

    Parameters:
    -----------
    syst : kwant.System or callable
        kwant System or a function returning the Hamiltonian
    params : dict
        dictionary of parameters. The keys are either strings
        or instances of `hv.Dimension` for better formatting.
        Iterable values are expanded over and used as axes.
        If the system expects extra momenta arguments, these are added.
    title : function or str
        Function that takes params as argument and returns the title.
        If a string it's used as a static title.
    num_bands : int
        Number of bands near the middle that should be plotted.
    return_energies : bool
        If True the function only returns the energies in an array
        and do not produce a plot.

    Returns:
    --------
    plot : an appropriate holoviews object
        Plot of varying parameter vs. spectrum.
    """
    energy_dim = hv.Dimension(
        name='energy',
        label='$E$'
    )

    if params is None:
        params = {}

    # Add momenta to parameters
    if not callable(syst):
        momenta = {
            hv.Dimension(
                name=k, label=f'${k}$', range=(-np.pi, np.pi)
            ): np.linspace(-np.pi, np.pi, 101)
            for k in 'k_x k_y k_z'.split()
            if k in syst.parameters and not k in params
        }
    else:
        momenta = {}
        
    pi_ticks = [(-np.pi, r'$-\pi$'), (0, '$0$'), (np.pi, r'$\pi$')]

    params = {**momenta, **params}

    # Obtain the data
    hamiltonians = hamiltonian_array(
        syst, params={str(dim): value for dim, value in params.items()}
    )

    energies = np.linalg.eigvalsh(hamiltonians)

    if num_bands is not None:
        mid = energies.shape[-1] // 2
        to_take = (
            (slice(None),) * (len(energies.shape) - 1)
            + (slice(mid - num_bands//2, mid + num_bands//2),)
        )
        energies = energies[to_take]

    if return_energies:
        return energies

    # Separate the parameters into constant and varied
    constants = {
        k: v for k, v in params.items()
        if not hasattr(v, "__len__")
    }
    variables = {
        k: v for k, v in params.items()
        if hasattr(v, "__len__")        
    }

    # Actual plotting
    if not variables:
        raise ValueError("No variable parameters")

    elif len(variables) == 1:
        xdim, values = variables.popitem()
        plot = hv.Path((values, energies), kdims=[xdim, energy_dim])

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

        kwargs = {'kdims': [xdim, ydim], 'vdims': [zdim]}

        plot = hv.Overlay(
            [
                hv.Surface(energies[:, :, i], **kwargs)(plot=style)
                for i in range(energies.shape[-1])
            ]
        )


        return plot.opts(plot={'Overlay': {'fig_size': 200}})
    
    else:
        raise ValueError("Cannot make 4D plots yet.")
        
    if title is not None:
        plot = plot.relabel(
            title(**params) if callable(title) else title
        )
        
    return plot
