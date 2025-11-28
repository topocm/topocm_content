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

# Thouless pumps and winding invariant

```{code-cell} ipython3
:tags: [remove-cell]

from course.functions import (
    add_reference_lines,
    combine_plots,
    line_plot,
    slider_plot,
    spectrum,
)
from course.init_course import init_notebook

import plotly.graph_objects as go
import kwant
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

init_notebook()
pi_ticks = [(-np.pi, r"$-\pi$"), (0, "0"), (np.pi, r"$\pi$")]
```

## Thouless pumps

Dganit Meidan from Ben Gurion University will introduce Thouless pumps.

```{youtube} gKZK9IGY9wo
:width: 560
:height: 315
```

## Hamiltonians with parameters

Previously, when studying the topology of systems supporting Majoranas (both the Kitaev chain and the nanowire), we were able to calculate topological properties by studying the bulk Hamiltonian $H(k)$.

There are two points of view on this Hamiltonian. We could either consider it a Hamiltonian of an infinite system with momentum conservation

$$
H = H(k) |k\rangle\langle k|,
$$

or we could equivalently study a finite system with only a small number of degrees of freedom (corresponding to a single unit cell), and a Hamiltonian which depends on some continuous periodic parameter $k$.

Of course, without specifying that $k$ is the real-space momentum, there is no meaning in bulk-edge correspondence (since the edge is an edge in real space), but the topological properties are still well-defined.

Sometimes we want to know how a physical system changes if we slowly vary some parameters of the system, for example a bias voltage or a magnetic field. Because the parameters change with time, the Hamiltonian becomes time-dependent, namely

$$
H = H(t).
$$

The slow [adiabatic](https://en.wikipedia.org/wiki/Adiabatic_theorem) change of parameters ensures that if the system was initially in the ground state, it will stay in the ground state, so that the topological properties are useful.

A further requirement for topology to be useful is the *periodicity* of time evolution:

$$
H(t) = H(t+T).
$$

The period can even go to $\infty$, in which case $H(-\infty) = H(+\infty)$. The reasons for the requirement of periodicity are somewhat abstract. If the Hamiltonian has parameters, we're studying the topology of a *mapping* from the space of parameter values to the space of all possible gapped Hamiltonians. This mapping has nontrivial topological properties only if the space of parameter values is compact.

For us, this simply means that the Hamiltonian has to be periodic in time.

Of course, if we want systems with bulk-edge correspondence, then in addition to $t$ our Hamiltonian must still depend on the real space coordinate, or the momentum $k$.

## Quantum pumps

In the image below (source: Chambers's Encyclopedia, 1875, via Wikipedia) you see a very simple periodic time-dependent system, an Archimedes screw pump.

![Archimedes screw pump illustration](figures/Archimedes_screw.jpg)

The changes to the system are clearly periodic, and the pump works the same no matter how slowly we use it (that is, change the parameters), so it is an adiabatic tool.

What about a quantum analog of this pump?

Let's take a one-dimensional region, coupled to two electrodes on both sides, and apply a strong sine-shaped confining potential in this region. As we move the confining potential, we drag the electrons captured in it.

So our system now looks like this:

```{code-cell} ipython3
# Plot of the potential in the pumping system as a function of coordinate.
# Some part of the leads is shown with a constant potential.
# Regions with E < 0 should be shaded to emulate Fermi sea.
A = 0.6
L = 10
lamb = (10 / 5.3) / (2 * np.pi)
mu = -0.4
mu_lead = -0.8


def f(x):
    if x < 0.0:
        return mu_lead
    if x >= 0.0 and x <= L:
        return mu + A * (1.0 - np.cos(x / lamb))
    if x > L:
        return mu_lead


x = np.linspace(-5, 15, 1000)
y = np.array([f(i) for i in x])

# Create plotly figure
fig_potential = go.Figure()

# Plot the potential
fig_potential.add_trace(
    go.Scatter(
        x=x, y=y, mode="lines", line=dict(color="black", width=2), showlegend=False
    )
)

# Fill the Fermi sea
y_fill = np.where(y <= 0, y, 0)
fig_potential.add_trace(
    go.Scatter(
        x=x,
        y=y_fill,
        fill="tozeroy",
        fillcolor="rgba(255, 0, 0, 0.5)",
        line=dict(color="black", width=1.5),
        mode="lines",
        showlegend=False,
    )
)

# Add arrow using annotation
fig_potential.add_annotation(
    x=7.0,
    y=1.25,
    ax=2.0,
    ay=1.25,
    xref="x",
    yref="y",
    axref="x",
    ayref="y",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=2,
    arrowcolor="black",
)

fig_potential.update_layout(
    xaxis=dict(title="$x$", range=[-2.5, 12.5], showticklabels=False),
    yaxis=dict(title="$U(x)$", range=[-2, 2], showticklabels=False),
    height=300,
    showlegend=False,
)

fig_potential
```

It is described by the Hamiltonian

$$
H(t) = \frac{k^2}{2m} + A [1 - \cos(x/\lambda + 2\pi t/T)].
$$

As we discussed, if we change $t$ very slowly, the solution will not depend on how fast $t$ varies.

When $A \gg 1 /m \lambda^2$ the confining potential is strong, and additionally if the chemical potential $\mu \ll A$, the states bound in the separate minima of the potential have very small overlap.

The potential near the bottom of each minimum is approximately quadratic, so the Hamiltonian is that of a simple Harmonic oscillator. This gives us discrete levels of the electrons with energies $E_n = (n + \tfrac{1}{2})\omega_c$, with $\omega_c = \sqrt{A/m\lambda^2}$ the oscillator frequency. In the large A limit, the states in the different minima are completely isolated so that the energy bands are flat with vanishing (group) velocity $d E_n(k)/d k=0$ of propagation.

We can numerically check how continuous bands in the wire become discrete evenly spaced bands as we increase $A$:

```{code-cell} ipython3
def hopping(site1, site2, t):
    return -t


def onsite(site, t, mu, A, phase, omega):
    return 2 * t - mu + A * (np.cos(omega * site.pos[0] + phase) + 1)


def infinite_modulated_wire(L):
    """Create an infinite wire with a periodic potential

    Chain lattice, one orbital per site.
    Returns kwant system.
    """
    lat = kwant.lattice.chain(norbs=1)
    pump = kwant.Builder(kwant.TranslationalSymmetry([-L]))

    pump[lat.shape((lambda x: True), [0])] = onsite
    pump[lat.neighbors()] = hopping

    return pump


L = 17
bulk = infinite_modulated_wire(L)
p = dict(t=1, mu=0.0, phase=0.0, omega=(2 * np.pi / L))


kwargs = {
    "ylims": [-0.2, 1.3],
    "xticks": pi_ticks,
    "yticks": [0, 0.5, 1.0],
    "xdim": r"$k$",
    "ydim": r"$E$",
    "k_x": np.linspace(-np.pi, np.pi, 101),
    "title": (lambda p: f"Band structure, A={p['A']:.2}"),
}


slider_plot(
    {p["A"]: spectrum(bulk, p, **kwargs) for p["A"] in np.linspace(0, 0.8, 10)},
    label="A",
)
```

So unless $\mu = E_n$ for some $n$, each minimum of the potential contains an integer number of electrons $N$.There are a large number of states at this energy and almost no states at $\mu$ away from $E_n$.

Since electrons do not move between neighboring potential minima, so when we change the potential by one time period, we move exactly $N$ electrons.

```{multiple-choice} Why are some levels in the band structure flat while some are not?
:explanation: The dispersion of the bands in a periodic potential appears when the wave functions from neighboring minima overlap.
:correct: 2
- The flat levels are the ones whose energies are not sensitive to the offset of confining potential.
- Destructive interference of the wave functions in neighboring minima suppresses the dispersion.
- The flat levels are localized deep in the potential minima, so the bandwidth is exponentially small.
- The flat levels correspond to filled states, and the rest to empty states.
```

## Quantization of pumped charge

As we already learned, integers are important, and they could indicate that something topological is happening.

At this point we should ask ourselves these questions: Is the discreteness of the number of electrons $N$ pumped per cycle limited to the deep potential limit, or is the discreteness a more general consequence of topology?

### Thought experiment

Let us consider the reservoirs to be closed finite (but large) boxes. When the potential in the wire is shifted the electrons clearly move from the left to the right reservoir. How do the reservoirs accommodate these electrons?

Since the Hamiltonian is periodic in time, the Hamiltonian together with all its eigenstates return to the initial values at the end of the period. The adiabatic theorem guarantees that when the Hamiltonian changes slowly the eigenstates evolve to an eigenstate that is adjacent in energy.

```{code-cell} ipython3
def modulated_wire(L, dL, bulk):
    """Create a pump.

    Chain lattice, one orbital per site.
    Returns kwant system.

    L is the length of the pump,
    dL is the number of lead unit cells to attach at either edge,
    bulk is the bulk model

    Arguments required in onsite/hoppings:
        t, mu, mu_lead, A, omega, phase
    """

    lat = kwant.lattice.chain(norbs=1)
    syst = kwant.Builder()
    syst.fill(bulk, shape=(lambda site: 0 <= site.pos[0] < L), start=[0])

    lead = kwant.Builder(kwant.TranslationalSymmetry([-1]))
    lead[lat(0)] = lambda site, t, mu_lead: 2 * t - mu_lead
    lead[lat.neighbors()] = hopping

    syst.attach_lead(lead, add_cells=dL)
    syst.attach_lead(lead.reversed(), add_cells=dL)

    return syst


L = 60
dL = 80
syst = modulated_wire(L=L, dL=dL, bulk=bulk).finalized()

p = dict(t=1, mu=0.0, mu_lead=0.1, A=0.3, omega=0.3)
phases = np.linspace(0, 2 * np.pi, 101)
en, all_vecs = zip(
    *[np.linalg.eigh(syst.hamiltonian_submatrix(params=p)) for p["phase"] in phases]
)
coord_operator = kwant.operator.Density(
    syst, onsite=(lambda site: site.pos[0] / (L + 2 * dL)), sum=True
)
centers = np.array([[coord_operator(vec) for vec in vecs.T] for vecs in all_vecs])

phase_scaled = phases / (2 * np.pi)

# Create figure with continuous colored lines by grouping into color buckets
n_buckets = 50
# Use a divergent colormap with dark middle
colormap = plt.get_cmap("coolwarm")
norm = mcolors.Normalize(vmin=centers.min(), vmax=centers.max())


# Convert matplotlib colormap to plotly format
def mpl_to_plotly_colorscale(cmap_name, n_samples=256):
    cmap = plt.get_cmap(cmap_name)
    return [
        [
            i / (n_samples - 1),
            f"rgb({int(cmap(i / (n_samples - 1))[0] * 255)},"
            f"{int(cmap(i / (n_samples - 1))[1] * 255)},"
            f"{int(cmap(i / (n_samples - 1))[2] * 255)})",
        ]
        for i in range(n_samples)
    ]


plotly_colorscale = mpl_to_plotly_colorscale("coolwarm")

fig = go.Figure()

# Group energy levels by their average color value
for i in range(centers.shape[1]):
    # Get the trajectory of this energy level
    x_vals = phase_scaled
    y_vals = np.array(en)[:, i]
    color_vals = centers[:, i]

    # Discretize color values into buckets
    color_indices = np.digitize(
        color_vals, np.linspace(centers.min(), centers.max(), n_buckets)
    )

    # Group consecutive points with the same color bucket
    segments_start = [0]
    for j in range(1, len(color_indices)):
        if color_indices[j] != color_indices[j - 1]:
            segments_start.append(j)
    segments_start.append(len(color_indices))

    # Plot each segment with its color, overlapping by one point to avoid gaps
    for k in range(len(segments_start) - 1):
        start_idx = segments_start[k]
        end_idx = segments_start[k + 1]
        # Extend to the next point to avoid gaps
        if k < len(segments_start) - 2:
            end_idx = min(end_idx + 1, len(x_vals))

        avg_color_val = np.mean(color_vals[start_idx:end_idx])
        rgba = colormap(norm(avg_color_val))
        color_str = (
            f"rgba({int(rgba[0] * 255)},{int(rgba[1] * 255)},"
            f"{int(rgba[2] * 255)},{rgba[3]})"
        )

        fig.add_trace(
            go.Scatter(
                x=x_vals[start_idx:end_idx],
                y=y_vals[start_idx:end_idx],
                mode="lines",
                line=dict(color=color_str, width=1.5),
                showlegend=False,
                hoverinfo="skip",
            )
        )

cmin = float(centers.min())
cmax = float(centers.max())

# put the (invisible) markers *inside* the y-range so plotly lays out the colorbar normally
y0 = 0.0  # within yaxis range [0, 0.3]

fig.add_trace(
    go.Scatter(
        x=[phase_scaled[0], phase_scaled[-1]],
        y=[y0, y0],
        mode="markers",
        marker=dict(
            size=6,
            opacity=0,  # invisible markers
            color=[cmin, cmax],  # spans full range
            colorscale=plotly_colorscale,
            cmin=cmin,
            cmax=cmax,
            showscale=True,
            colorbar=dict(
                title=dict(text=r"$\langle x \rangle$", side="right"),
                ticks="outside",
                nticks=6,
                tickformat=".1g",
                thickness=15,
                len=0.7,
                x=1.02,
                xanchor="left",
                y=0.5,
                yanchor="middle",
            ),
        ),
        showlegend=False,
        hoverinfo="skip",
    )
)

fig.update_layout(
    margin=dict(l=60, r=140, t=30, b=50),
    xaxis=dict(title="$t/T$", range=[0, 1]),
    yaxis=dict(title="$E$", range=[0, 0.3]),
    height=400,
)

fig
```

We indeed see that the levels move up and down in energies.
The states that don't shift in energy are the ones trapped in the minima of the periodic potential.

We see that the states in the gaps between the wire bands belong to either of the two reservoirs.
States in the left reservoir turn out to move down in energy and ones in the right reservoir move up in energy (right now this is numerical—we will see why later).

Let us imagine we park our Fermi energy (i.e. the energy that separates completely occupied and completely empty states) in the gap where there are few states.

With time, an empty level in the left reservoir moves from above the Fermi level to a state below the Fermi level. The occupation of this state cannot  change in this process because of the adiabatic theorem. Therefore after the pumping cycle is over the left reservoir has an empty state below the Fermi level i.e. one less electron. The reverse process happens in the right lead so that it has one extra electron.

So the electron that was transferred in the wire from the left reservoir to the right came from emptying the highest energy occupied state one the left and occupying the lowest energy unoccupied state on the right.

More generally, while levels do not have to move as shown in the figure, the energy level structure of the periodic in time Hamiltonian has to return to itself. The number (possibly negative) of levels in the left reservoir that crossed from being above the Fermi level to below  must exactly be the change in charge of the left reservoir. This is an INTEGER.

Therefore, our thoughts about "where the electrons came from" leads us to an interesting conclusion: The number of charges pumped in an adiabatic pumping cycle (independent of the strength $A$) is an integer (possibly $0$).

Furthermore, it is an integer as long as the wire is gapped at the chosen Fermi level (so as to isolate the reservoirs).


So without doing any calculations, we can conclude that:

> The number of electrons pumped per cycle of a quantum pump is an integer as long as
> the bulk of the pump is gapped. Therefore it is a **topological invariant**.

## Counting electrons through reflection

The expression for the pumped charge in terms of the bulk Hamiltonian $H(k, t)$ is complicated.

It's an integral over both $k$ and $t$, called a **Chern number** or in other sources a TKNN integer. Its complexity is beyond the scope of our course, but is extremely important, so we will have to study it... next week.

There is a much simpler way to calculate the same quantity using scattering formalism. This follows from returning to understanding how energy levels in the reservoir move as a function of time.

Consider levels in the energy gap of the wire so that the levels near the Fermi energy are confined to the reservoir. Now all the levels in the reservoir are quantized, and are standing waves, so they are equal weight superpositions of waves going to the left $\psi_L$ and to the right $\psi_R$,

$$
\psi_n = \psi_L(x) + \psi_R(x) \propto \exp(ik_n x) + \exp(-ik_n x + i\phi),
$$

where the wave number $k_n$ is of course a function of energy. The relative phase shift $\phi$ is necessary to satisfy the boundary condition at $x=0$, where $\psi_L = r \psi_R$, and so $\exp(i \phi) = r$. The energies of the levels are determined by requiring that the phases of $\psi_L$ and $\psi_R$ also match at $x = -L$. These boundary conditions lead to the relation

$$
2 k_n L = 2n \pi +\phi.
$$

Changing the phase continuously in time $t$ by $2\pi$ evolves $k_n$ from $(2 L)^{-1}[2n\pi+\phi]$ to $(2L)^{-1}[2n\pi+2\pi+\phi]=2k_{n+1}L$. This means that the change in phase $\phi$ results in the state with index $n$ evolving
into an index  $n+1$.
Thus, the winding of phase $\phi$ by $2\pi$ also changes the wave-function $\psi_n \rightarrow \psi_{n+1}$.

As discussed in the previous paragraph, such a movement of energy level in the reservoir is associated with transfer of charge between the reservoir through the wire.

> We conclude that if the reflection phase $\phi$ from the wire advances by $2\pi$, this corresponds to a unit charge pumped across the wire.

It's very easy to generalize our argument to many modes. For that we just need to sum all of the reflection phase shifts, which means we need to look at the phase of $\det r$.

We conclude that there's a very compact relation between charge $dq$ pumped by an infinitesimal change of an external parameter and the change in reflection matrix $dr$:

$$
dq = \frac{d \log \det r}{2\pi i} = \operatorname{Tr}\frac{r^\dagger dr }{ 2 \pi i}.
$$

While we derived this relation only for the case when all incoming particles reflect and $r$ is unitary, written in the form of a trace it also has physical implications even if there is transmission[^1].

[^1]: @10.48550/arXiv.cond-mat/9808347

Let's check if this expression holds to our expectations. If $\lVert r \rVert=1$, this is just the number of times the phase of $\det r$ winds around zero, and it is certainly an integer, as we expected.

This provides an independent argument (in addition to the movement of energy levels from the last section ) for why the pumped charge is quantized as long as the gap is preserved.

## Applying the topological invariant

We know now how to calculate the pumped charge during one cycle, so let's just see how it works in practice.

The scattering problem in 1D can be solved quickly, so let's calculate the pumped charge as a function of time for different values of the chemical potential in the pump.

```{code-cell} ipython3
def plot_charge(syst, p, energy):
    phases = np.linspace(0, 2 * np.pi, 100)
    determinants = [
        np.linalg.det(kwant.smatrix(syst, energy, params=p).submatrix(0, 0))
        for p["phase"] in phases
    ]
    charge = -np.unwrap(np.angle(determinants)) / (2 * np.pi)
    charge -= charge[0]

    return phases / (2 * np.pi), charge


kwargs = {
    "ylims": [-0.2, 1.3],
    "xticks": pi_ticks,
    "yticks": [0, 0.5, 1.0],
    "xdim": r"$k$",
    "ydim": r"$E$",
    "k_x": np.linspace(-np.pi, np.pi, 101),
    "title": "Band structure",
}

p.update(mu_lead=0.0, A=0.6, phase=0)

pump = modulated_wire(L=100, dL=0, bulk=bulk).finalized()

energies = [0.1, 0.3, 0.6, 0.9]
# Define colors for each energy level
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

base_spectrum = spectrum(bulk, p, **kwargs)
for energy, color in zip(energies, colors):
    add_reference_lines(
        base_spectrum, y=energy, line_color=color, line_dash="dash", line_width=2
    )

charge_phases, charge_vals = zip(*(plot_charge(pump, p, energy) for energy in energies))
charge_fig = line_plot(
    charge_phases[0],
    np.vstack(charge_vals).T,
    labels=[f"E={energy:.1f}" for energy in energies],
    x_label=r"$t/T$",
    y_label=r"$q/e$",
    x_ticks=[0, 1],
    y_ticks=[0, 1, 2, 3],
    show_legend=False,
    title="Pumped charge",
)
# Update line colors to match the band structure
for i, color in enumerate(colors):
    charge_fig.data[i].line.color = color
    charge_fig.data[i].line.width = 2

charge_fig.update_yaxes(range=[-0.5, 3.5])
combine_plots([base_spectrum, charge_fig], cols=2)
```

In the left plot, we show the band structure, where the different colors correspond to different chemical potentials. The right plot shows the corresponding pumped charge. During the pumping cycle the charge may change, and the relation between the offset $\phi$ of the potential isn't always linear. However we see that after a full cycle, the pumped charge exactly matches the number of filled levels in a single potential well.

```{multiple-choice} What happens to the dependence of the reflection phase shift on time if we remove one of the reservoirs and leave the other one?
:explanation: The total pumped charge must become equal to zero since there's nowhere to place the charge, but since the pump is insulating, the phase cannot change for most of the cycle unless a sharp resonance appears
:correct: 1
- It becomes constant.
- For most of the cycle it stays the same, but there appear sharp jumps such that the total winding becomes zero.
- Nothing changes, since the two ends of the pump are far apart from each other, and the pump is not conducting.
- The reflection phase gets a new time dependence with zero winding, unrelated to the original one.
```

## Quantized charge and scattering invariant

```{youtube} 6lXRAZ7hv7E
:width: 560
:height: 315
```
