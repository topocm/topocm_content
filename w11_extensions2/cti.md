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

# Crystalline topological insulators

```{code-cell} ipython3
:tags: [remove-cell]

import numpy as np
import holoviews
import kwant
from course.functions import pauli
from course.functions import spectrum
from course.init_course import init_notebook

init_notebook()
holoviews.output(size=150)
```

## Introduction

Crystalline topological insulators are introduced by Liang Fu from MIT.

```{youtube} N9-tUYjXC1s
:width: 560
:height: 315
```

## The role of crystalline symmetries

In the very beginning of the course, we told you that conservation laws - unitary symmetries of the Hamiltonian - do not lead to striking consequences on topology. They allow to reduce the problem by making the Hamiltonian block-diagonal, but not much else (see also Shinsei Ryu's introductory video to week eight).

At first sight, it may seem that crystalline symmetries: mirror or reflection symmetries, rotation symmetries, and so on - are no exception to the above consideration. They are unitary symmetries whose operators commute with the Hamiltonian.

Nevertheless, the role of crystalline symmetries can be quite subtle and it can have important consequences. The reason is that crystalline symmetries are non-local. They relate one point in a crystal to another point, possibly a very distant point. This means that in terms of the Bloch Hamiltonian of the crystal, these symmetries mix different values of momentum.

Consider for instance a 2D crystal with a reflection symmetry $\mathcal{R}: (x, y) \to (-x, y)$ around the $x=0$ axis. In momentum space, this symmetry will read $RH(k_x, k_y)R^\dagger = H(-k_x, k_y)$, with a certain unitary operator $R$.

Due to this type of constraint on the Brillouin zone, crystalline symmetries can have important consequences on the topological properties of Bloch Hamiltonians.

Note however, that sometimes the mere presence of a surface can break a crystalline symmetry of the bulk, so that one should be careful when applying the bulk-boundary correspondence to properties based on crystalline symmetries.

```{multiple-choice} In which case can inversion symmetry protect gapless surface states?
:explanation: Any surface would break inversion symmetry of a crystal.
:correct: 0
- Never.
- In the case of 2D TIs with inversion symmetry.
- Only in three dimensions.
- Only in combination with particle-hole or time-reversal symmetry.
```

## Reflection symmetry

The second-simplest crystalline symmetry (after translation symmetry of course) occurring in many materials is reflection (or mirror) symmetry around one spatial coordinate. For instance, in a 3D crystal, reflection symmetry around the $z$ axis transforms the wave-wector as

$$
(k_x, k_y, k_z)\rightarrow (k_x, k_y, -k_z).
$$

Reflection symmetry also applies a 180 degree rotation about the $z$-axis to the electron spin, so $\psi_{\uparrow}\rightarrow -i \psi_{\uparrow}$ and $\psi_{\downarrow}\rightarrow i \psi_{\downarrow}$, so that the operator squares to $-1$ when acting on a spin.

Next, if we consider the application of reflection symmetry to either a two-dimensional material or a plane in a three dimensional material, then we can choose $k_z=0$ and the reflection symmetry just becomes a regular unitary symmetry i.e., the $C_2$ rotation.

In this case, the topological classification follows rather simply from our earlier discussion. $C_2$ is a unitary symmetry with eigenvalues $\pm i$. We can split our Hamiltonian into the corresponding two sector $H_{\pm}$ acting on the $C_2=\pm i$ sectors respectively. Each of the Hamiltonians $H_{\pm}$ are 2 dimensional Hamiltonians in class A (i.e. with no symmetry) and therefore we can associate a Chern number $N_{\pm}$ with each of them.

>If the Hamiltonian overall is trivial then the total Chern number $N_++N_-=0$ so we can classify the 2 dimensional mirror symmetric Hamiltonians by a **mirror Chern number** $N_M=N_+-N_-$.

The mirror Chern number is a topological invariant in the sense that it cannot change without a closure of the bulk gap provided the reflection symmetry remains intact. Moreover, the reflection symmetry together with non-trivial values of the invariant will guarantee edge states.

Naturally, the same recipe allows to construct a reflection symmetric topological insulator starting from any other topological invariant, not just a Chern number. We will now try to do this.

```{multiple-choice} How would you attempt to make a model of a topological insulator with surface states protected by reflection symmetry?
:explanation: Such a stack would have a reflection symmetry around any of the layers, which is not broken by the presence of a surface parallel to the stacking direction.
:correct: 1
- By using the interface of a material with reflection symmetry, and that of one without it.
- By stacking many layers of a lower dimensional topological insulator, and coupling them in a reflection-symmetric fashion.
- Reflection symmetry alone cannot protect any gapless surface state.
- By making a narrow ribbon of the material where only the momentum orthogonal to the reflection axis can be non-zero.
```

## Examples

Let's think, what could be the simplest topological system protected by reflection symmetry.

We need $d=2$, since the only possible reflection symmetry is broken by the boundary in $d=1$, and we can once again consider coupled Majorana nanowires.

We can put two nanowires in a unit cell of the lattice and make their parameters different. In this way, the weak topological invariant is trivial (there is an even number of Majoranas per unit cell).

On the other hand, if the hopping between the nanowires is reflection invariant, there will be a reflection symmetry axis passing through each nanowire, like this:

![](figures/reflection.svg)

If we do everything right (this does require some trial and error in searching for the hopping that actually can couple the two Majoranas from the edge), we get a painfully familiar dispersion:

```{code-cell} ipython3
def nanowire_chains(length=40, n=2):
    def onsite(site, t, mu, B, delta):
        (x, y) = site.pos
        return (
            (2 * t - mu) * pauli.szs0
            + delta * pauli.sxs0
            + (y % 2 == 0) * B * pauli.s0sz
            + (y % 2 == 1) * B * pauli.s0sy
        )

    def hopy(site1, site2, t, alpha):
        return -t * pauli.szs0 + 0.5 * 1j * alpha * pauli.szsx

    def hopx(site1, site2, tx):
        (x1, y1) = site1.pos
        (x2, y2) = site2.pos
        return 1j * (-1) ** ((x1 + x2 - 1) % 2 == 0) * tx * pauli.sysx

    def shape(pos):
        (x, y) = pos
        return (0 <= x < n) and (0 <= y < length)

    lat = kwant.lattice.square(norbs=4)
    sym = kwant.TranslationalSymmetry((n, 0))
    syst = kwant.Builder(sym)

    syst[lat.shape(shape, (0, 0))] = onsite
    syst[kwant.HoppingKind((1, 0), lat)] = hopx
    syst[kwant.HoppingKind((0, 1), lat)] = hopy

    return syst


syst = nanowire_chains()
p = dict(t=1.0, tx=0.2, mu=0.0, B=0.4, delta=0.15, alpha=0.3)
spectrum(
    syst,
    p,
    k_x=np.linspace(-1, 1, 101),
    ylims=(-0.2, 0.2),
    xticks=3,
    yticks=3,
    title="Stacked Majorana wires",
)
```

In a similar way, we can also construct a tight-binding model with a mirror Chern number. The only difference with the Majorana wires that we need to worry about is that Chern number is a $\mathbb{Z}$ invariant instead of $\mathbb{Z}_2$.

This means that the Chern number of the alternating layers has to have opposite signs, or otherwise the surface would just have surface states going in a single direction.

Once again, coupling the layers we get a familiar Dirac cone on the surface:

```{code-cell} ipython3
def stacked_qwz(w=50):
    def shape(pos):
        return 0 <= pos[2] < w

    def hopx(site1, site2, delta, t):
        return -0.5j * delta * pauli.sx - t * pauli.sz

    def hopy(site1, site2, gamma):
        return gamma * pauli.sy

    def hopz(site1, site2, delta, t):
        return -0.5j * delta * pauli.sy * (-1) ** (site1.pos[1]) - t * pauli.sz

    def onsite(site, t, mu):
        return pauli.sz * (4 * t + mu)

    lat = kwant.lattice.general(np.eye(3), norbs=4)
    syst = kwant.Builder(kwant.TranslationalSymmetry((1, 0, 0), (0, 2, 0)))

    syst[lat.shape(shape, (0, 0, 0))] = onsite
    syst[kwant.HoppingKind((1, 0, 0), lat)] = hopx
    syst[kwant.HoppingKind((0, 1, 0), lat)] = hopy
    syst[kwant.HoppingKind((0, 0, 1), lat)] = hopz

    return syst


xticks = [(-np.pi, r"$-\pi$"), (0, r"$0$"), (np.pi, r"$\pi$")]
yticks = [(0, r"$0$"), (np.pi / 2, r"$\pi/2$"), (np.pi, r"$\pi$")]

p = dict(t=1.0, delta=1, gamma=0.5, mu=-0.5)
syst = stacked_qwz(30)

spectrum(
    syst,
    p,
    num_bands=2,
    k_x=np.linspace(-np.pi, np.pi, 51),
    k_y=np.linspace(0, np.pi, 51),
    xticks=xticks,
    yticks=yticks,
    title="Stacked Chern insulator",
)
```

Again, the dispersion of the edge states looks exactly like what we saw already because the edge state dispersion in any topological insulator is just given by the Dirac equation.

## Experimental realization of a 3D crystalline topological insulator

As mentioned by Liang Fu, three dimensional crystalline topological insulators have been both predicted and also found in nature. The magical material, which is topological turns out to be SnTe, which is actually a "rock-salt" structure. We won't bore you with the details of the rock-salt structure, which you can find for yourself on [Wikipedia](https://en.wikipedia.org/wiki/Cubic_crystal_system#Rock-salt_structure).

We will just start with the key ingredients for the crystalline topological insulator, namely the symmetries of the crystal. These include, spatial inversion $P$, time-reversal symmetry $\Theta$ and most importantly the three mirror planes in the cubic Brillouin zone. The three mirror planes $\Gamma L_1 L_2$, $\Gamma L_3 L_4$ and $\Gamma L_3 L_1$ in the Brillouin zone are reflection-symmetric directions that are created out of four time-reversal invariant momenta $\Gamma, L_1, L_2, L_3, L_4$.

While the reflection symmetry acts non-trivially on general wave-vectors $\bf k$, the symmetry preserves the mirror planes in the Brillouin zone. Following the idea of dimensional reduction that we used for three dimensional topological insulators (week 6) and also in subsequent weeks, we can define the topological invariant for the crystalline topological insulator in terms of the three mirror Chern numbers for the three mirror planes. For SnTe, all these mirror Chern numbers turn out to be $N_{M}(\Gamma L_i L_j)=-2$. This topological invariant leads to surface Dirac cones on certain surfaces as shown below.

![](figures/SnTefig.png)

Figure copyright of the Zahid Hasan lab, Princeton, 2015, available under CC-BY-NC-SA 4.0 International license.

This surface spectrum is very easy to interpret.

The crystal surface you see here is perpendicular to two mirror planes projected on $\bar{\Gamma}\bar{X}$ axes. Since the mirror Chern number with respect to each of these planes is $-2$, there is a pair of Dirac cones near each $X$-point protected by a respective mirror symmetry.

The reflection symmetry pins the pairs of Dirac cones to the mirror planes, while time reversal symmetry requires their momenta to be opposite. The 90 degree rotation symmetry interchanges the pairs of cones.

## Conclusion

In short, crystalline topological insulators combine the variety of topological phases with the variety of the crystalline symmetry groups, leading to a multitude of new opportunities.
