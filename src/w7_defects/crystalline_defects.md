---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.4
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Crystalline defects in weak topological insulators

```{code-cell} ipython3
:tags: [remove-cell]

import sys

sys.path.append("../../code")
from init_course import *

init_notebook()
import itertools
import warnings

warnings.simplefilter("ignore", UserWarning)
```

## Introduction: weak topological phases

Taylor Hughes from the University of Illinois at Urbana-Champaign will describe the interplay between defects in crystals and weak topological insulators.

```{code-cell} ipython3
:tags: [remove-input]

Video("k3ZKCg7jtTs")
```

As you can see, there is a simple and universal connection between weak topological phases and the ability of defects to carry topologically protected states. The topological invariant $\mathcal{Q}$ of a dislocation is the number of protected states that it carries. It can be determined from the vector of weak topological invariants, $\mathbf{\mathcal{Q}}_\textrm{weak}$, and the Burgers vector of the dislocation $\mathbf{B}$:

$$
\mathcal{Q} = \mathbf{\mathcal{Q}}_\textrm{weak}\cdot\mathbf{B}
$$

Let us now go through the main points that lead to this conclusion, and argue for why it has to be that way.

## Crystallographic defects and topology

There are many different types of [defects in crystals](http://en.wikipedia.org/wiki/Crystallographic_defect): vacancies, substitutions, grain boundaries, dislocations, and many more.

What kinds of defects are important for topology? Consider a vacancy for example:
![](figures/Formation_Point_Defect.png)
(By Safe cracker (Own work) [CC BY 3.0 (http://creativecommons.org/licenses/by/3.0)], via Wikimedia Commons)

To create a vacancy, we need to remove a single atom (or all the atoms following one line). Can this type of defect carry a topologically protected state?

We already know that topological protection requires a Hamiltonian that cannot be created locally. For example, in order to create a single Majorana bound state at a phase boundary, another Majorana must appear elsewhere. Removing an atom or a line of atoms only changes the system locally, so the *other* topologically protected state cannot appear anywhere.

A simple vacancy is therefore not interesting from a topological point of view. What kinds of topological defects would work then? Crystallographic defects leave nothing different since they leave the bulk Hamiltonian unchanged far away from the defect core. This means we need to do something nontrivial to the crystal so that it cannot be removed locally.

Examples of such defects are dislocations:

![](figures/burgers_vectors.png)
(By David Gabriel García Andrade (Own work) [Public domain], via Wikimedia Commons)

In order to create a dislocation we need to cut a crystal along one plane and displace all the atoms along that plane by the *Burgers vector*. This has to be done all the way to the crystal boundary (or infinity in an infinite crystal), so the dislocation affects the entire system. This means that a dislocation cannot be removed locally.

As Taylor Hughes explained, a dislocation can be detected infinitely far from its core by going around it and verifying that we don't return to the point of origin. We cannot simply remove a dislocation by locally replacing some atoms. Therefore, it may carry a topologically protected mode.

Unsurprisingly, crystallographic defects that cannot be removed locally are called "topological", which brings us to the first important conclusion:

> *Topological* crystallographic defects are the ones that may carry topologically protected modes.

This is a non-trivial observation, even though it sounds tautological. There are two different types of topology involved: the topology of the electronic modes and the topology of the crystal.

## The role of defect dimensionality

When do topological defects carry protected edge states?

Far away from the defect, the bulk is homogeneous. Hence, the appearance of an edge state must be encoded both in the properties of the defect and in the bulk Hamiltonian. Of course, the appearance of this state must also be controlled by a topological invariant, since the protected state cannot disappear without the closing of the bulk gap.

What kind of topological invariant can this be? Can a strong topological invariant create a protected edge state at a defect?

In a sense we already know that it does. We can think of the crystal surface as a defect that breaks translational symmetry, and so it is a crystallographic defect. The strong topological invariant is the quantity that tells us whether or not the bulk can be continuously deformed into vacuum, or equivalently, whether or not the surface can be smoothly removed without closing the bulk gap.

In a $d$-dimensional bulk, the strong invariant is responsible for the appearance of a $d-1$-dimensional topologically protected state. This state can only be bound to a surface, which is the only $d-1$-dimensional topological defect. Defects of lower dimensionality can not be impacted by the strong invariant. An example of such a defect of lower dimensionality is precisely a dislocation, as in the previous figure. It is a one-dimensional defect in a three-dimensional crystal.

This is where the weak invariants come into play.

First of all, we know that the dimensionality $d_\textrm{egde}$ of a protected state at a defect must match the dimensionality of the defect. Secondly, we know the dimensionality of the topological invariant that controls this protected state: it is the topological invariant in the dimension $d_\textrm{edge}+1$.

The topological invariants with dimensionality $d_{edge}+1$ form a vector or a tensor of the weak indices. The last thing we need to figure out is how to extract information about what happens at the defect from the weak indices.

## The defect topological invariant

We have almost arrived at the criterion for the appearance of protected states in dislocations.

To see how the weak topological invariant relates to the number of states in the dislocation, we start by deforming a weak topological insulator into a set of disconnected planes, each carrying protected states. If there is a single state approaching the dislocation, as is shown in the figure below, it cannot backscatter and must therefore continue through the dislocation core.

![](figures/dislocation_helical.svg)

(adapted from Cdang (Own work), via Wikimedia Commons, [CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0).)

Counting the number and the orientation of the crystal planes approaching the core of the dislocation is just the Burgers vector. Hence, the number of edge states entering the dislocation core is the Burgers vector times the number of states per crystal plane. This brings us to the conclusion:

$$
\mathcal{Q} = \mathbf{\mathcal{Q}}_\textrm{weak}\cdot\mathbf{B}.
$$

Let's now test this idea and see if we can observe the protected dislocation states.

## Electronic states in dislocations

Now that we know the main concepts, let's apply them to concrete examples. Let's take two models for topological insulators that we already know and apply them to lattice systems with dislocations.

We will create a 3D weak topological insulators by stacking many layers of 2D topological insulators along the $z$ direction. For the individual layers, we will use the BHZ model (by the way, note that the lecture today was given by the H of BHZ!) for a time-reversal invariant topological insulator, and the square lattice model for the quantum Hall effect that we used in week 4. In this way, we can study dislocations both with and without time reversal symmetry. In both cases, we take the hoppings between different layers to be relatively weak compared to those within the same layer.

Let's start with a screw dislocation connecting two layers. The system looks like this:

```{code-cell} ipython3
:tags: [remove-input]

# Layered BHZ and QAH models

def onsite(site, M, B, D, field):
    return (
        (M - 4 * B) * pauli.s0sz
        - 4 * D * pauli.s0s0
        + field * site.pos[1] * pauli.s0s0
    )


def hopx(site1, site2, B, D, A):
    return B * pauli.s0sz + D * pauli.s0s0 + 0.5j * A * pauli.szsx


def hopy(site1, site2, B, D, A):
    return B * pauli.s0sz + D * pauli.s0s0 - 0.5j * A * pauli.s0sy


def hopz(site1, site2, t_inter):
    return t_inter * np.eye(4)


lat = kwant.lattice.cubic(norbs=4)
layered_bhz_infinite = kwant.Builder(kwant.TranslationalSymmetry(*lat.prim_vecs))
layered_bhz_infinite[lat(0, 0, 0)] = onsite
layered_bhz_infinite[kwant.HoppingKind((1, 0, 0), lat)] = hopx
layered_bhz_infinite[kwant.HoppingKind((0, 1, 0), lat)] = hopy
layered_bhz_infinite[kwant.HoppingKind((0, 0, 1), lat)] = hopz


def onsite(site, mu, B, field):
    return (mu - 4 * B) * pauli.sz + field * site.pos[1] * pauli.s0


def hopx(site1, site2, B, A):
    return B * pauli.sz + 0.5j * A * pauli.sx


def hopy(site1, site2, B, A):
    return B * pauli.sz + 0.5j * A * pauli.sy


def hopz(site1, site2, t_inter):
    return t_inter * pauli.s0


lat = kwant.lattice.cubic(norbs=2)
layered_qah_infinite = kwant.Builder(kwant.TranslationalSymmetry(*lat.prim_vecs))
layered_qah_infinite[lat(0, 0, 0)] = onsite
layered_qah_infinite[kwant.HoppingKind((1, 0, 0), lat)] = hopx
layered_qah_infinite[kwant.HoppingKind((0, 1, 0), lat)] = hopy
layered_qah_infinite[kwant.HoppingKind((0, 0, 1), lat)] = hopz


def screw_dislocation(model, L=10, W=15):
    syst = kwant.Builder(
        kwant.TranslationalSymmetry((L, 0, 0), (0, W, 0), (0, 0, 1))
    )
    syst.fill(
        model,
        shape=(
            lambda site: 0 <= site.pos[0] < L and 0 <= site.pos[1] < W
        ),
        start=(0, 0, 0)
    )

    def crosses_branch_cut(hop):
        x1, y1, _ = hop[0].pos
        x2, *_ = hop[1].pos
        return (x1 - L//2 + .5) * (x2 - L//2 + .5) < 0 and W//4 < y1 < 3*W//4

    to_delete = [tuple(sorted(hop)) for hop in syst.hoppings() if crosses_branch_cut(hop)]
    hopping_values = [syst[hop] for hop in to_delete]
    del syst[to_delete]
    diagonal_hops = [
        (hop[0].family(*(hop[0].tag - [0, 0, 1])), hop[1])
        for hop in to_delete
    ]
    for hop, value in zip(diagonal_hops, hopping_values):
        syst[hop] = value

    return syst


L, W = 10, 15
x0, y0, y1 = L//2 - 0.5, W//4 + 0.5, 3*W//4 - 0.5

bzh_screw_dislocation = screw_dislocation(layered_bhz_infinite, L, W)
def displacement(x, y):
    x -= x0
    return -np.angle(np.sqrt((y - y0 - 1j*x) * (y - y1 + 1j*x))) / (np.pi)

fig = kwant.plot(
    bzh_screw_dislocation,
    site_size=.02, hop_lw=.05, fig_size=(9, 9), show=False,
    pos_transform=(
        lambda pos: [pos[0], pos[1], pos[2] + displacement(pos[0], pos[1])]
    )
)
ax = fig.axes[0]
ax.view_init(elev=40, azim=60)
ax.plot(
    [x0, x0, np.nan, x0, x0], [y0, y0, np.nan, y1, y1], [-2, 2, np.nan, -2, 2],
    lw=3, linestyle=":"
)
ax.axis("off");
```

The figure above shows a single unit cell in the $z$-direction that is infinitely repeated to obtain the dispersion relation. Along the $x$ and $y$ directions the system has periodic boundary conditions.

The Burgers' vector is parallel to the $z$-axis and has unit length (the dislocation connects neighboring layers). The dotted lines are the dislocation cores.

Let's look at the band structure along the $z$ direction, and the wave functions of the corresponding states.

```{code-cell} ipython3
:tags: [remove-input]

kwargs = {
    "k_x": 0,
    "k_y": 0,
    "k_z": np.linspace(np.pi - np.pi / 4, np.pi + np.pi / 4, 51),
    "ylims": [-0.6, 1.01],
    "yticks": [-0.5, 0, 0.5],
    "xticks": [
        (np.pi - np.pi / 4, r"$\pi-\pi/4$"),
        (np.pi, r"$\pi$"),
        (np.pi + np.pi / 4, r"$\pi+\pi/4$"),
    ],
}

screw_dislocations = dict(
    BHZ=screw_dislocation(layered_bhz_infinite, L, W),
    QAH=screw_dislocation(layered_qah_infinite, L, W)
)
parameters = dict(
    BHZ=dict(A=1.0, B=1.0, D=0.0, M=0.8, field=0.01, t_inter=-.1),
    QAH=dict(A=1.0, B=1.0, mu=0.8, field=0.005, t_inter=-0.1)
)

screw_dislocation_spectra = {
    name: spectrum(syst, p=parameters[name], **kwargs).relabel(f"Band structure, {name}")
    for name, syst in screw_dislocations.items()
}

def density_array(syst, psi):
    """Convert a wave function into a 2D array suitable for plotting."""
    density = kwant.operator.Density(syst)(psi)
    all_coords = np.array([site.tag for site in syst.sites])[:, :2]
    r_min = np.min(all_coords, axis=0) + 1
    data = np.zeros(np.ptp(all_coords, axis=0))
    data[tuple(all_coords.T - r_min.reshape(-1, 1))] = density
    return data


k_z = np.pi + 0.1
energies, densities = {}, {}
for name, syst in screw_dislocations.items():
    syst = kwant.wraparound.wraparound(syst).finalized()
    H = syst.hamiltonian_submatrix(params=dict(k_x=0, k_y=0, k_z=k_z, **parameters[name]))
    vals, vecs = np.linalg.eigh(H)
    # Select the energies close to the middle of the spectrum
    indices = slice(len(vals)//2 - 3, len(vals)//2 + 3)
    energies[name] = vals[indices]
    densities[name] = [density_array(syst, psi) for psi in vecs.T[indices]]


# %opts Raster(cmap='gist_heat_r' interpolation=None) {+framewise}

holoviews.HoloMap({
    (n, name): (
        (
            spectrum
            * holoviews.Points((k_z, energy)).opts(s=50)
            * holoviews.VLine(k_z)
        )
        + holoviews.Raster(density.T, label=r"$\left|\psi\right|^2$").opts(
            cmap='gist_heat_r', interpolation=None
        )
    )
    for name, spectrum in screw_dislocation_spectra.items()
    for n, (energy, density) in enumerate(zip(energies[name], densities[name]))
}, kdims=["n", "model"]).collate()
```

You see that the band structure is gapless: because of the presence of the dislocation, there are states dispersing below the bulk gap along the $z$ direction.

A look at their wave functions in the right panel shows that in the $x$-$y$ plane, these low-energy states are localized around the end points of the dislocation (we show the wave function corresponding to the blue dot in the band structure plot). On the other hand, when you look at the wave function of states above the gap, you see that they are spread out the whole $x$-$y$ plane.

Here, the fundamental difference between the BHZ model and the quantum anomalous Hall case is that in the former, the gapless states at the dislocation are helical, while in the latter they are chiral.

We can also look at an edge dislocation:

```{code-cell} ipython3
:tags: [remove-input]

def edge_dislocation(model, L=10, W=15):
    syst = kwant.Builder(
        kwant.TranslationalSymmetry((L, 0, 0), (0, W, 0), (0, 0, 1))
    )

    # Interchange x- and z- hopping
    lat = list(model.sites())[0].family
    rotated = kwant.Builder(model.symmetry)
    rotated[lat(0, 0, 0)] = model[lat(0, 0, 0)]
    rotated[kwant.HoppingKind((1, 0, 0), lat)] = model[next(kwant.HoppingKind((0, 0, 1), lat)(model))]
    rotated[kwant.HoppingKind((0, 1, 0), lat)] = model[next(kwant.HoppingKind((0, 1, 0), lat)(model))]
    rotated[kwant.HoppingKind((0, 0, 1), lat)] = model[next(kwant.HoppingKind((1, 0, 0), lat)(model))]
    syst.fill(
        rotated,
        shape=(
            lambda site: 0 <= site.pos[0] < L and 0 <= site.pos[1] < W
        ),
        start=(0, 0, 0)
    )

    def removed_layer(site):
        x, y, _ = site.pos
        return x == L//2 and W//4 < y < 3*W//4

    to_delete = [site for site in syst.sites() if removed_layer(site)]
    for site in to_delete:
        syst[
            site.family(*(site.tag - (1, 0, 0))),
            site.family(*(site.tag + (1, 0, 0)))
        ] = syst[
            site, site.family(*(site.tag + (1, 0, 0)))
        ]
    del syst[to_delete]

    return syst

L, W = 10, 15
x0, y0, y1 = L//2, W//4 + 0.5, 3*W//4 - 0.5

bzh_edge_dislocation = edge_dislocation(layered_bhz_infinite, L, W)
def displacement(x, y):
    x -= x0
    return -np.angle(np.sqrt((y - y0 - 1j*x) * (y - y1 + 1j*x))) / (np.pi)

fig = kwant.plot(
    bzh_edge_dislocation,
    site_size=.02, hop_lw=.05, fig_size=(9, 9), show=False,
    pos_transform=(
        lambda pos: [pos[0] + displacement(pos[0], pos[1]), pos[1], pos[2]]
    )
)
ax = fig.axes[0]
ax.view_init(elev=40, azim=60)
ax.plot(
    [x0, x0, np.nan, x0, x0], [y0, y0, np.nan, y1, y1], [-2, 2, np.nan, -2, 2],
    lw=3, linestyle=":"
)
ax.axis("off");
```

The Burgers vector is now along the $y$-direction, and it still has unit length. The band structure and the wave function plots show similar behavior.

```{code-cell} ipython3
:tags: [remove-input]

kwargs = {
    "k_x": 0,
    "k_y": 0,
    "k_z": np.linspace(-np.pi / 4, np.pi / 4, 51),
    "ylims": [-0.6, 0.95],
    "yticks": [-0.5, 0, 0.5],
    "xticks": [(-np.pi / 4, r"$-\pi/4$"), (0, r"$0$"), (np.pi / 4, r"$\pi/4$")],
}

edge_dislocations = dict(
    BHZ=edge_dislocation(layered_bhz_infinite, L, W),
    QAH=edge_dislocation(layered_qah_infinite, L, W)
)

edge_dislocation_spectra = {
    name: spectrum(syst, p=parameters[name], **kwargs).relabel(f"Band structure, {name}")
    for name, syst in edge_dislocations.items()
}

k_z = 0.1
energies, densities = {}, {}
for name, syst in edge_dislocations.items():
    syst = kwant.wraparound.wraparound(syst).finalized()
    H = syst.hamiltonian_submatrix(params=dict(k_x=0, k_y=0, k_z=k_z, **parameters[name]))
    vals, vecs = np.linalg.eigh(H)
    # Select the energies close to the middle of the spectrum
    indices = slice(len(vals)//2 - 3, len(vals)//2 + 3)
    energies[name] = vals[indices]
    densities[name] = [density_array(syst, psi).T for psi in vecs.T[indices]]


holoviews.HoloMap({
    (n, name): (
        (
            spectrum
            * holoviews.Points((k_z, energy)).opts(s=50)
            * holoviews.VLine(k_z)
        )
        + holoviews.Raster(density, label=r"$\left|\psi\right|^2$").opts(
            cmap='gist_heat_r', interpolation=None
        )
    )
    for name, spectrum in edge_dislocation_spectra.items()
    for n, (energy, density) in enumerate(zip(energies[name], densities[name]))
}, kdims=["n", "model"]).collate()
```

```{code-cell} ipython3
:tags: [remove-input]

question = (
    "What would happen in both simulations above if we changed the dislocation, "
    "making the Burgers vector twice as long?"
)

answers = [
    "The wave function would just spread out a bit more because the dislocation is larger.",
    "The number of gapless states would double for both models.",
    "The gapless states would be gapped out for both models.",
    "The dislocation would only have gapless states in the quantum anomalous Hall case, not for the BHZ model.",
]

explanation = (
    r"Doubling the Burgers vector doubles the topological invariant in the $\mathbb{Z}$ case, "
    r"and changes it from non-trivial to trivial in the $\mathbb{Z}_2$ case."
)

MultipleChoice(
    question=question, answers=answers, correct_answer=3, explanation=explanation
)
```

## Conclusions

```{code-cell} ipython3
:tags: [remove-input]

Video("MvcvJiZYSSk")
```
