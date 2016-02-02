import numpy as np
import holoviews as hv
from holoviews import plotting
from holoviews import Options, Store
import pfaffian as pf
import kwant
from types import SimpleNamespace


kron_prods = ['s0s0', 's0sx', 's0sy', 's0sz',
              'sxs0', 'sxsx', 'sxsy', 'sxsz',
              'sys0', 'sysx', 'sysy', 'sysz',
              'szs0', 'szsx', 'szsy', 'szsz']

__all__ = ['sigma0', 'sigmax', 'sigmay', 'sigmaz', 'spectrum',
           'plot_bands', 'h_k', 'plot_bands', 'find_pfaffian',
           'kitaev_chain', 'spinful_kitaev_chain', 'nanowire_chain'] + kron_prods

options = Store.options(backend='matplotlib')
options.Contours = Options('style', linewidth=2, color='k')
options.Contours = Options('plot', aspect='square')
options.HLine = Options('style', linestyle='--', color='b', linewidth=2)
options.VLine = Options('style', linestyle='--', color='r', linewidth=2)
options.Image = Options('style', cmap='gist_heat_r')
options.Image = Options('plot', title_format='{label}')
options.Path = Options('style', linewidth=1.2, color='k')
options.Path = Options('plot', aspect='square', title_format='{label}')
options.Curve = Options('style', linewidth=2, color='k')
options.Curve = Options('plot', aspect='square', title_format='{label}')
options.Overlay = Options('plot', show_legend=False, title_format='{label}')

sigma0 = np.array([[1., 0.], [0., 1.]])
sigmax = np.array([[0., 1.], [1., 0.]])
sigmay = np.array([[0., -1j], [1j, 0.]])
sigmaz = np.array([[1., 0.], [0., -1.]])

s0s0 = np.kron(sigma0, sigma0)
s0sx = np.kron(sigma0, sigmax)
s0sy = np.kron(sigma0, sigmay)
s0sz = np.kron(sigma0, sigmaz)
sxs0 = np.kron(sigmax, sigma0)
sxsx = np.kron(sigmax, sigmax)
sxsy = np.kron(sigmax, sigmay)
sxsz = np.kron(sigmax, sigmaz)
sys0 = np.kron(sigmay, sigma0)
sysx = np.kron(sigmay, sigmax)
sysy = np.kron(sigmay, sigmay)
sysz = np.kron(sigmay, sigmaz)
szs0 = np.kron(sigmaz, sigma0)
szsx = np.kron(sigmaz, sigmax)
szsy = np.kron(sigmaz, sigmay)
szsz = np.kron(sigmaz, sigmaz)


def spectrum(sys, xticks, yticks, xdim, ydim, xlims=None, ylims=None, **kwargs):
    p = SimpleNamespace(**kwargs)
    
    for key, value in kwargs.items():
        try:
            if len(value) > 0:
                changing_variable = key
                changing_values = value
        except:
            TypeError
    
    def energy(x):
        p.__dict__[changing_variable] = x
        H = sys.hamiltonian_submatrix(args=[p])
        return np.linalg.eigvalsh(H)
    
    spectrum = np.array([energy(x) for x in changing_values])
    
    plot = hv.Path((changing_values, spectrum), kdims=[xdim, ydim])
    
    if xlims is None:
        xlims = slice(xticks[0], xticks[-1])
    else:
        xlims = slice(xlims[0], xlims[1])
    if ylims is None:
        ylims = slice(yticks[0], yticks[-1], None)
    else:
        ylims = slice(ylims[0], ylims[1])
    
    return plot[xlims, ylims](plot={'xticks':xticks, 'yticks':yticks})

def h_k(sys, p, phase_fac=1):
    h, t = sys.cell_hamiltonian(args=[p]), sys.inter_cell_hopping(args=[p])
    return h + t * phase_fac + t.T.conj() * np.conjugate(phase_fac)

def find_pfaffian(H):
    return np.sign(np.real(pf.pfaffian(1j*H)))

def plot_bands(lead, p, momenta=np.linspace(-np.pi, np.pi)):
    bands = kwant.physics.Bands(lead, args=[p])
    evs = np.array([bands(k=k) for k in momenta])
    return hv.Path((momenta, evs), kdims=[r'$k$', r'$E$'])

def kitaev_chain(L=None, periodic=False):
    lat = kwant.lattice.chain()
    
    if L is None:
        sys=kwant.Builder(kwant.TranslationalSymmetry((-1,)))
        L = 1
    else:
        sys = kwant.Builder()

    # transformation to antisymmetric basis
    U = np.matrix([[1.0, 1.0], [1.j, -1.j]]) / np.sqrt(2)
    
    onsite = lambda onsite, p: - p.mu * U.dot(sigmaz.dot(U.H))
    for x in range(L):
        sys[lat(x)] = onsite
         
    hop = lambda site1, site2, p: U.dot((-p.t * sigmaz - 1j * p.delta * sigmay).dot(U.H))
    sys[kwant.HoppingKind((1,), lat)] = hop
    
    if periodic:
        last_hop = lambda site1, site2, p: hop(site1, site2, p) * (1 - 2 * p.lambda_)
        sys[lat(0), lat(L-1)] = last_hop
    return sys

def spinful_kitaev_chain(L=None, periodic=False):
    lat = kwant.lattice.chain()
    
    if L is None:
        sys=kwant.Builder(kwant.TranslationalSymmetry((-1,)))
        L = 1
    else:
        sys = kwant.Builder()

    # transformation to antisymmetric basis
    onsite = lambda onsite, p: (2*p.t - p.mu) * szs0 + p.B * szsz
    for x in range(L):
        sys[lat(x)] = onsite
         
    hop = lambda site1, site2, p: -p.t * szs0 - 1j * p.delta * sys0
    sys[kwant.HoppingKind((1,), lat)] = hop
    
    if periodic:
        last_hop = lambda site1, site2, p: hop(site1, site2, p) * (1 - 2 * p.lambda_)
        sys[lat(0), lat(L-1)] = last_hop
    return sys

def nanowire_chain(L=None, periodic=False):
    lat = kwant.lattice.chain()
    
    if L is None:
        sys=kwant.Builder(kwant.TranslationalSymmetry((-1,)))
        L = 1
    else:
        sys = kwant.Builder()

    onsite = lambda onsite, p: (-2*p.t + p.mu) * szs0 + p.B * s0sz + p.Delta * sxs0
    
    for x in range(L):
        sys[lat(x)] = onsite
         
    hop = lambda site1, site2, p: -p.t * szs0 - .5j * p.alpha * szsx
    sys[kwant.HoppingKind((1,), lat)] = hop
    
    if periodic:
        phase_diff = lambda site1, site2, p: np.kron(np.array([[np.exp(1j*p.flux/2), 0], 
                                                               [0, np.exp(-1j*p.flux/2)]]), sigma0)
        sys[lat(0), lat(L-1)] = lambda s1, s2, p : 0.7 * phase_diff(s1, s2, p).dot(hop(s1, s2, p))
    return sys