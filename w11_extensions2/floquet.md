---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Floquet topological insulators

```{code-cell} ipython3
:tags: [remove-cell]

from scipy import linalg as la
from functools import reduce

import kwant
import numpy as np
import plotly.graph_objects as go

from course.init_course import init_notebook

from course.functions import (
    add_reference_lines,
    combine_plots,
    line_plot,
    slider_plot,
    pauli,
)

init_notebook()

pi_ticks = [
    (-np.pi, r"$-\pi$"),
    (-np.pi / 2, r"$-\pi/2$"),
    (0, r"$0$"),
    (np.pi / 2, r"$\pi/2$"),
    (np.pi, r"$\pi$"),
]
```

## Introduction

Today's topic, Floquet topological insulators, is introduced by Mark Rudner from the Niels Bohr Institute at Copenhagen.

```{youtube} 1peVp_IZ7Ts
:width: 560
:height: 315
```

## Periodically driven systems

We will now learn about a new generalization of topology, namely how it applies to the quantum evolution of systems with a time-dependent Hamiltonian. As you may recall, we've already encountered time dependence, back when we considered quantum pumps. However, back then we assumed that the time evolution was very slow, such that the system stayed in the ground state at all times, i.e. it was adiabatic. Can we relax the adiabaticity constraint? Can we find an analog of topology in systems that are driven so fast that energy isn't conserved?

For the same reasons as before, we'll consider periodic driving

$$
H(t + T) = H(t).
$$

Once again, this is necessary because otherwise, any system can be continuously deformed into any other, and there is no way to define a gap.

Before we get to topology, let's refresh our knowledge of time-dependent systems.

The Schrödinger equation is:

$$
i\frac{d \psi}{dt} = H(t) \psi.
$$

It is a linear equation, so we can write its solution as

$$
\psi(t_2) = U(t_2, t_1) \psi(t_1),
$$

where $U$ is a unitary *time evolution operator*. It solves the same Schrödinger equation as the wave function, and is equal to the identity matrix at the initial time. It is commonly written as

$$
U(t_2, t_1) = \mathcal{T} \exp\,\left[-i\int_{t_1}^{t_2} H(t) dt\right],
$$

where $\mathcal{T}$ represents time-ordering (not time-reversal symmetry). The time-ordering is just a short-hand notation for the need to solve the full differential equation, and it is necessary if the Hamiltonians evaluated at different times in the integral do not commute.

The time evolution operator satisfies a very simple multiplication rule:

$$
U(t_3, t_1) = U(t_3, t_2) U(t_2, t_1),
$$

which just says that time evolution from $t_1$ to $t_3$ is a product of time evolutions from $t_1$ to $t_2$ and then from $t_2$ to $t_3$. Of course an immediate consequence of this is the equality $U(t_2, t_1)^\dagger = U(t_2, t_1)^{-1} = U(t_1, t_2)$.

### Floquet theory

The central object for the study of driven systems is the evolution operator over one period of the driving,

$$
U(t + T, t) \equiv U,
$$

which is called the Floquet time evolution operator. It is important because it allows us to identify the wave functions that are the same if an integer number of drive periods passes. These are the stationary states of a driven system, and they are given by the eigenvalues of the Floquet operator:

$$
U \psi = e^{i \alpha} \psi.
$$

The stationary states are very similar to the eigenstates of a stationary Hamiltonian, except that they are only stationary if we look at fixed times $t + nT$. That's why the Floquet time evolution operator is also called a stroboscopic time evolution operator.

We can very easily construct a Hermitian matrix from $U$, the **Floquet Hamiltonian**:

$$
H_\textrm{eff} = i T^{-1} \,\ln U.
$$

Its eigenvalues $\varepsilon = \alpha / T$ are called quasi-energies, and they always belong to the interval $-\pi < \alpha \leq \pi$.

If the system is translationally invariant, we can study the effective band structure of $H_\textrm{eff}(\mathbf{k})$, find an energy in which the bulk Hamiltonian has no states, and study the topological properties of such a Hamiltonian: most of the things we already know still apply.

Of course, selecting a single quasi-energy as the Fermi level is arbitrary, since the equilibrium state of driven systems doesn't correspond to a Fermi distribution of filling factors, but at least it seems close enough for us to try to apply topological ideas.

```{multiple-choice} But wait, we arbitrarily chose the starting point $t$ in time for calculating the Floquet operator. What if we chose a different one?
:explanation: Choosing a different starting point applies a unitary transformation to the Floquet evolution operator, and so it keeps the quasienergies the same.
:correct: 3
- The starting time is just an extra parameter of our system, and topology depends on it.
- It doesn't matter, the wave function evolution within one period can be neglected, since we are interested in many periods.
- There's only one correct starting point in time.
- It doesn't matter since the quasienergies are independent of the starting point.
```

## Driven Majorana wire

Let us start by considering something we know very well, namely the superconducting Majorana nanowire model from week 2. This model has three important parameters which determine whether the wire is in the topological Majorana phase or not: the chemical potential $\mu$, the superconducting gap $\Delta$, and the magnetic field $B$. The topological phase with unpaired Majorana modes at zero energy is realized for $B > \sqrt{\mu^2 + \Delta^2}$.

Now, imagine that we can periodically drive some of these parameters. For instance, consider the simple example when

$$
\mu = \left\{
\begin{matrix}
\mu_1 \quad \text{for } 0 < t < T/2 \\
\mu_2 \quad \text{for } T/2 < t < T
\end{matrix}\right.
$$

Then, the integral to find the time evolution operator is easy to evaluate, and we simply have

$$
U = \exp(i T H_2 / 2) \exp(i T H_1 / 2)
$$

with $H_1$ and $H_2$ the nanowire Hamiltonians with chemical potential $\mu_1$ and $\mu_2$. A peculiar property of driven systems is that as the period becomes large, the band structure 'folds': if the driving is very weak, and the original Hamiltonian has energy $E$, the Floquet Hamiltonian has a much smaller quasienergy $(E\bmod 2\pi /T)$. This means that even when $H_1$ and $H_2$ correspond to trivial systems, we can still obtain nontrivial topology if we make the period large enough, as you can see for yourself:

```{code-cell} ipython3
def evolution_operator(hamiltonians, T):
    n = len(hamiltonians)
    exps = [la.expm(-1j * h * T / n) for h in hamiltonians]
    return reduce(np.dot, exps)


def calculate_finite_spectrum(periods, hamiltonians):
    energies = []
    for T in periods:
        U = evolution_operator(hamiltonians, T)
        phases = np.angle(la.eigvals(U))
        phases = np.sort(np.abs(phases))
        ev = np.sort([(-1) ** n * val for n, val in enumerate(phases)])
        energies.append(ev)
    return np.array(energies).real


def calculate_bands(momenta, hamiltonians_k, T):
    energies = []
    for k in momenta:
        hamiltonians = [h_k(k) for h_k in hamiltonians_k]
        U = evolution_operator(hamiltonians, T)
        phases = np.angle(la.eigvals(U))
        phases = np.sort(np.abs(phases))
        ev = np.sort([(-1) ** n * val for n, val in enumerate(phases)])
        energies.append(ev)
    return np.array(energies).real


def onsite(site, t, mu, B, delta):
    return (2 * t - mu) * pauli.szs0 + B * pauli.s0sz + delta * pauli.sxs0


def hopping(site1, site2, t, alpha):
    return -t * pauli.szs0 + 0.5 * 1j * alpha * pauli.szsx


lat = kwant.lattice.chain(norbs=4)
infinite_nanowire = kwant.Builder(kwant.TranslationalSymmetry((-1,)))
infinite_nanowire[lat(0)] = onsite
infinite_nanowire[kwant.HoppingKind((1,), lat)] = hopping
finite_nanowire = kwant.Builder()
finite_nanowire.fill(infinite_nanowire, (lambda site: 0 <= site.pos[0] < 20), (0,))
infinite_nanowire = kwant.wraparound.wraparound(infinite_nanowire).finalized()
finite_nanowire = finite_nanowire.finalized()

J = 2.0
p1 = dict(t=J / 2, mu=-1 * J, B=J, delta=2 * J, alpha=J)
p2 = dict(t=J / 2, mu=-3 * J, B=J, delta=2 * J, alpha=J)

H1 = finite_nanowire.hamiltonian_submatrix(params=p1)
H2 = finite_nanowire.hamiltonian_submatrix(params=p2)


def h1_k(k_x):
    return infinite_nanowire.hamiltonian_submatrix(params=dict(**p1, k_x=k_x))


def h2_k(k_x):
    return infinite_nanowire.hamiltonian_submatrix(params=dict(**p2, k_x=k_x))


periods = np.linspace(0.2 / J, 1.6 / J, 100)
momenta = np.linspace(-np.pi, np.pi)

energies = calculate_finite_spectrum(periods, [H1, H2])
spectrum = np.array([calculate_bands(momenta, [h1_k, h2_k], T) for T in periods])


def plot(n):
    T = J * periods[n]

    left = line_plot(
        J * periods,
        energies,
        x_label=r"$JT$",
        y_label=r"$ET$",
        x_ticks=5,
        y_ticks=pi_ticks,
        y_range=[-np.pi, np.pi],
        show_legend=False,
    )
    add_reference_lines(left, x=T, line_color="blue", line_dash="dash")
    right = line_plot(
        momenta,
        spectrum[n],
        x_label="$k$",
        y_label="$E_kT$",
        x_ticks=pi_ticks,
        y_ticks=pi_ticks,
        y_range=[-np.pi, np.pi],
        show_legend=False,
    )
    return combine_plots([left, right], cols=2)


slider_plot(
    {float(J * periods[idx]): plot(idx) for idx in range(len(periods))}, label="JT"
)
```

On the left you see the Floquet spectrum of a finite system as a function of the driving period measured in units of the hopping strength, and on the right you see the Floquet dispersion in momentum space.

We now witness a cool phenomenon: just like in the undriven case, the particle-hole symmetry maps $E \rightarrow -E$, but now this means that not only $E = 0$ is special, but also $E = \pi$!

In other words, this means that there are two relevant gaps in the effective Floquet BdG Hamiltonian $H_\textrm{eff}$. Now, by using the same argument as we used for the regular Majoranas, we learn that if we have an isolated Floquet state with a quasienergy $\epsilon=0$ or $\epsilon=\pi$, it cannot be removed unless the gap surrounding it closes.

In other words:

> A Floquet superconductor has two types of Majorana bound states: the usual ones with quasienergy $\epsilon=0$, and the $\pi$-Majoranas that are as far from zero energy as possible.

So the calculation above reveals two interesting features of driven systems: the first is that the periodic driving can turn a trivial system into a non-trivial system with topologically protected Floquet states. The second is that topology is richer than in the non-driven system: for instance, here the richness comes from the fact that the topologically protected states may occur at two different points in the spectrum.

Now try to answer the following question: what's the topological invariant of this system? How do we tell whether normal Majoranas are present, and whether $\pi$-Majoranas are present? (We'll return to this question in the end of the lecture.)

## A Floquet Chern insulator

As a second example of a driven system that shows something that the undriven system doesn't, let's consider the following toy model.

We take a square lattice with time-dependent nearest neighbor hopping $t$. Next, let's engineer a time-evolution of the hopping between sites such that during a period $T$ hoppings are turned on in an alternate fashion, as in the following figure:

![](figures/time_steps.svg)

Each step lasts one quarter of a period.

Now let's tune the period such that the probability for an electron to hop along a hopping is one at the end of each quarter period [$t = (\pi / 2) / (T / 4)$]. Over the complete period the trajectories of electrons will look like this:

![](figures/floquet_bulk.svg)

Every electron makes a closed loop and ends up back at its origin. After every single period the system is back to its initial state. In other words, the Floquet operator is $U=1$, and $H_\textrm{eff}=0$.

Let's have a look at the dispersion, and also see what happens as we tune the driving period:

```{code-cell} ipython3
lat = kwant.lattice.general([[2, 0], [1, 1]], [(0, 0), (1, 0)], norbs=1)
a, b = lat.sublattices
infinite_checkerboard = kwant.Builder(kwant.TranslationalSymmetry(*lat.prim_vecs))
infinite_checkerboard[lat.shape(lambda pos: True, (0, 0))] = 0
infinite_checkerboard[kwant.HoppingKind((0, 0), b, a)] = lambda s1, s2, t1: -t1
infinite_checkerboard[kwant.HoppingKind((-1, 1), b, a)] = lambda s1, s2, t2: -t2
infinite_checkerboard[kwant.HoppingKind((1, 0), a, b)] = lambda s1, s2, t3: -t3
infinite_checkerboard[kwant.HoppingKind((0, 1), a, b)] = lambda s1, s2, t4: -t4


def plot_dispersion_2D(T):
    syst = infinite_checkerboard
    B = np.array(syst.symmetry.periods).T
    A = B @ np.linalg.inv(B.T @ B)
    syst = kwant.wraparound.wraparound(syst).finalized()

    def hamiltonian_k(par):
        def f(k_x, k_y):
            k_x, k_y = np.linalg.lstsq(A, [k_x, k_y], rcond=None)[0]
            ham = syst.hamiltonian_submatrix(params=dict(**par, k_x=k_x, k_y=k_y))
            return ham

        return f

    hamiltonians_k = [
        hamiltonian_k(dict(t1=1, t2=0, t3=0, t4=0)),
        hamiltonian_k(dict(t1=0, t2=1, t3=0, t4=0)),
        hamiltonian_k(dict(t1=0, t2=0, t3=1, t4=0)),
        hamiltonian_k(dict(t1=0, t2=0, t3=0, t4=1)),
    ]

    def get_energies(k_x, k_y):
        hamiltonians = [h_k(k_x, k_y) for h_k in hamiltonians_k]
        U = evolution_operator(hamiltonians, T)
        ev = np.sort(np.angle(la.eigvals(U)))
        return ev

    K = np.linspace(-np.pi, np.pi, 50)
    energies = np.array([[get_energies(k_x, k_y) for k_x in K] for k_y in K])

    title = rf"$T = {T / np.pi:.2} \pi$"

    xs = np.linspace(-np.pi, np.pi, energies.shape[1])
    ys = np.linspace(-np.pi, np.pi, energies.shape[0])

    fig = go.Figure()
    max_abs = float(np.nanmax(np.abs(energies)))
    if not np.isfinite(max_abs) or max_abs == 0:
        max_abs = 1.0
    for band in range(energies.shape[-1]):
        fig.add_surface(
            x=xs,
            y=ys,
            z=energies[:, :, band],
            colorscale="RdBu",
            showscale=False,
            opacity=0.9,
            cmin=-max_abs,
            cmax=max_abs,
        )
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(
                title="kₓ",
                tickvals=[v for v, _ in pi_ticks[::2]],
                ticktext=["−π", "0", "π"],
                range=[-np.pi, np.pi],
            ),
            yaxis=dict(
                title="kᵧ",
                tickvals=[v for v, _ in pi_ticks[::2]],
                ticktext=["−π", "0", "π"],
                range=[-np.pi, np.pi],
            ),
            zaxis=dict(title="E", range=[-np.pi, np.pi], nticks=5),
            aspectmode="cube",
        ),
        width=680,
        height=560,
        margin=dict(l=30, r=30, t=60, b=20),
    )
    return fig


Ts = np.linspace(1, 3, 11, endpoint=True)
slider_plot({T: plot_dispersion_2D(np.pi * T) for T in Ts}, label="T/π")
```

Now, there isn't a Hamiltonian which is more topologically trivial than the zero Hamiltonian. We may be tempted to conclude that our system is trivial and, by bulk-boundary correspondence, has no edge states.

That's something we can also very easily verify by computing the dispersion of a finite size ribbon:

```{code-cell} ipython3
W = 10
ribbon = kwant.Builder(kwant.TranslationalSymmetry((1, 1)))
ribbon.fill(
    infinite_checkerboard, (lambda site: 0 <= site.pos[0] - site.pos[1] < W), (0, 0)
)
ribbon = ribbon.finalized()


def get_h_k(lead, p):
    bands = kwant.physics.Bands(ribbon, params=p)
    h, t = bands.ham, bands.hop
    return lambda k: h + t * np.exp(-1j * k) + t.T.conj() * np.exp(1j * k)


def calculate_bands(momenta, hamiltonians_k, T):
    energies = []
    for k in momenta:
        hamiltonians = [h_k(k) for h_k in hamiltonians_k]
        U = evolution_operator(hamiltonians, T)
        energies.append(np.sort(np.angle(la.eigvals(U))))
    return np.array(energies).real


hamiltonians_k = [
    get_h_k(ribbon, dict(t1=1, t2=0, t3=0, t4=0)),
    get_h_k(ribbon, dict(t1=0, t2=1, t3=0, t4=0)),
    get_h_k(ribbon, dict(t1=0, t2=0, t3=1, t4=0)),
    get_h_k(ribbon, dict(t1=0, t2=0, t3=0, t4=1)),
]

periods = np.linspace(0, 4 * np.pi, 11)
momenta = np.linspace(-np.pi, np.pi)
spectrum = np.array([calculate_bands(momenta, hamiltonians_k, T) for T in periods])


def plot(n):
    return line_plot(
        momenta,
        spectrum[n],
        x_label="$k$",
        y_label="$E_kT$",
        x_ticks=pi_ticks,
        y_ticks=pi_ticks,
        y_range=[-np.pi, np.pi],
        show_legend=False,
    )


slider_plot({(T / np.pi): plot(idx) for idx, T in enumerate(periods)}, label="T/π")
```

We see something very different from our expectations. All the bulk states are indeed at $E=0$, but there are two branches of dispersion that are clearly propagating. These can only belong to the edges, and since the two edges look identical, these two modes have to belong to the opposite edges. We seem to conclude that even though the bulk Hamiltonian is trivial, the edges carry chiral edge states, as if there was a finite Chern number.

When the driving period is tuned to ensure the absence of bulk dispersion, we can also understand why the edge states appear. If we select a state that starts on the edge, and follow it for one period, we find that there are modes that never leave the edge, since one of the hoppings in the vertical direction is absent.

![](figures/trajectories.svg)

So what is happening with bulk-edge correspondence?

```{multiple-choice} How can you change the chirality of the edge states in the figure above?
:explanation: Reversing the driving protocol is the same as applying time-reversal symmetry, so it will reverse the direction of the chiral edge modes
:correct: 1
- By changing the driving period.
- By reversing the driving protocol sequence.
- By changing the sign of the nearest neighbor hopping.
- By making the electrons start from the black sublattice.
```

## Bulk-edge correspondence in driven systems

The two examples we've studied reveal an imporant feature of topological Floquet insulators. It seems that knowing the bulk Floquet Hamiltonian is sufficient to calculate the topological invariant, by just applying the known expression to the Floquet Hamiltonian. However, that's not enough.

In rough terms, the reason for this insufficiency is due to Floquet topological insulators missing a topologically trivial state which can be taken as a reference. With any regular 2D Hamiltonian, we know that if we take $E \rightarrow -\infty$, we will get a trivial system with the Chern number zero. In a Floquet system, the only thing that lowering the energy tells us is that the Chern number is periodic in quasienergy, like any other observable property.

What do we need to know to derive the full topological invariant from the bulk properties? The answer is that we need the complete evolution operator for all moments in time, or in other words the full dependence $H(t)$. The actual calculation of the topological invariant is technically involved, and falls beyond what we can cover in this course. Moreover, to the best of our knowledge, the full classification of Floquet topological insulators is not yet accomplished.

## Conclusions

```{youtube} DbyqIczcR9c
:width: 560
:height: 315
```
