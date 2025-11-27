# Fractional quantum Hall effect and topological particles

## Introduction

This topic is introduced by Sankar Das Sarma from the university of Maryland.

```{youtube} 4gSJSo3olfg
:width: 560
:height: 315
```

## Interacting systems

One obvious thing that we completely ignored throughout the course is the effects of interactions on topology. It is of course possible to generalize all the symmetry classes that we have studied to many-body Hamiltonians, but what happens to the classification of the topological phases?

The first statement we should make here is that our work so far wasn't wasted: most of the usual topological insulators turn out to tolerate interactions as long as the interactions do not spontaneously break the symmetry, or close the bulk gap.
There are interesting cases where the classification collapses. For example, the 1D BDI chain with Majorana fermions on one of the two sublattice degrees of freedom allows a $\mathbb{Z}_8$ classification with interactions instead of $\mathbb{Z}$. The reason for this is that the 8-Majorana interaction term doesn't break the symmetries anymore.

However this is relatively minor compared to the real can of worms that the interactions open: the amount of possibilities for the interacting phases is much larger. To begin with, we'll discuss the oldest known example of a strongly interacting topological phase, the fractional quantum Hall effect. Note that it only covers a single dimension ($D=2$), and a single symmetry class (no symmetry at all). Yet, classifying all such states turns out to be a very hard task.

## Fractional charge and statistics in the fractional quantized Hall effect

If you followed what we learned about the integer quantum Hall effect, you'll remember that we used the pumping argument to establish that the Hall conductance in an incompressible liquid is quantized in integers. You might now wonder if the experimental evidence for the fractional quantum Hall effect completely invalidates this argument in some way. The key step in the argument was to realize that the pumped charge that results from the insertion of one flux quantum $\Phi_0$ into a Corbino geometry is

$$
Q_{pump}=\sigma_{xy}\Phi_0\equiv \nu e,
$$

where $\nu=\sigma_{xy}/G_0$ is the Hall conductance in dimensionless units. For the non-interacting system that we studied in the quantum Hall effect, we assumed that only an integer number of electrons could be transferred between the edges - so $\nu$ had to be an integer.

The real reason that the charge transferred had to be an integer multiple of the electron charge was that the Hamiltonian for the electrons was identical between flux $\Phi=0$ and flux $\Phi=\Phi_0$. Since the system is incompressible, it is reasonable to assume that all excitations in the system are local. Usually we expect different excited states to differ by rearranging electrons. Within this framework, such excitations can differ by integer multiples of electronic charge.

The existence of fractional values of $\nu$ implies that the edge can have local excitations that differ by a fractional electron charge. In principle, the inner edge of the Corbino geometry can be shrunk to a point, and if we do this, we're forced to conclude that the system can now host excitations that have fractional charge.

The fractional charged excitations are local particles just like the electrons themselves. So we can ask about the statistics under exchange of two such particles. On performing such an exchange, the total many-body wave function of the system returns to itself, but
the wave function can pick up a Berry phase. For fermions this phase is $\pi$ and for Bosons it is zero. Instead of computing the phase directly, let us consider doing a double exchange, which is topologically equivalent to taking a particle around another one and computing the phase for that.

![](figures/exchange.svg)

Let us first assume that one of the particles was created by a flux quantum. Since the flux quantum created this particle adiabatically by a pumping process, locality dictates that the particle going around the flux quantum + particle cannot know about the existence of the other particle. Thus the phase from going around a particle together with its flux quantum must vanish. On the other hand, the particle picks up a phase of $2\pi \nu$ from just going around the flux quantum. Thus double exchange of a pair of particles leads to a Berry phase of $-2\pi\nu$. This is another strange property of excitations in the FQH state! They must obey different statistics than both fermions and bosons, and are thus referred to as anyons. Therefore the exchange phase of anyons in the simple FQH states is given by

$$
\phi_{exch}=\pi\nu.
$$

```{multiple-choice} The Laughlin argument was used to prove that the Hall effect must be quantized in integers. What is the key assumptionthat must be dropped in order to understand the fractional quantum Hall effect?
:explanation: The key assumption in the Laughlin argument for the integer case was that the charge that was added by pumping couldonly be an integer multiple of an electronic charge.
:correct: 1
- Allow electrons to have fractional statistics.
- Allow quasiparticles with fractional charge.
- Require that the system forms an incompressible fluid.
- Allow electrons to have fractional charge.
- Allow quasiparticles to have fractional statistics.
```

## Topological degeneracy

Knowing that the system supports particles with nontrivial braiding statistics, we can derive its next important property, the topological degeneracy of the ground state.

To do this, we turn around the argument for computing the statistics of particles and consider the statistics of fluxes. A particle going around a flux acquires a phase of $2\pi\nu$. As noted in the last unit, the combination of a particle and flux does not have any non-trivial exchange statistics. So replacing the particle by another flux will lead to a phase of $-2\pi \nu$. Therefore the exchange phase of fluxes gives a phase of $\pi\nu$, just like the exchange of particles.

Let us now put the FQH system on a torus. A natural operation on the torus is to create a flux anti-flux pair, move them around a cycle of the torus and annihilate them at the end. This operation inserts a flux into one of the two nontrivial cycles of the torus. Let's label this operation $T_{1,2}$ for each of the cycles of the torus:

![](figures/torus.svg)

The last physical step to deriving the degeneracy is to ask what is the commutator $T_1^{-1}T_2^{-1}T_1 T_2$. This operator describes first moving a vortex around the red contour, then moving the vortex around the blue contour, moving the vortex back around the red contour, and finally undoing the motion of the vortex along the blue contour.
No matter which path we choose for this operation, we will need to take one vortex all the way around the other one. According to the braiding rule we get:

$$
T_1^{-1}T_2^{-1}T_1 T_2 =e^{i2\pi \nu}.
$$

Now all we need to do is an exercise in elementary quantum mechanics. First of all, both $T_{1,2}$ commute with the Hamiltonian. Let's take $|\Psi\rangle$ as a simultaneous ground state of the Hamiltonian and eigenstate of $T_1$. If in addition $e^{i\alpha}|\Psi\rangle=T_2|\Psi\rangle$, then $T_1$ and $T_2$ would commute. Since we know this isn't the case, $T_2|\Psi\rangle$ must be a ground state of the Hamiltonian which is not the same as $|\Psi\rangle$.

> We conclude that fractional quantum Hall phases have ground state degeneracy on the torus.

We have seen an example of ground state degeneracy in Majorana wires, where the degeneracy of the zero modes could not be lifted by any local perturbation. The difference between the Majorana case and fractional quantum Hall is that in the latter we don't rely on the presence of defects, and the degeneracy is a property of the surface on which we put the fractional quantum Hall state.

## Creating an FQH state

How can we describe a fractional quantum Hall state? Laughlin used a representation of the many-electron wave function in complex coordinates to guess a wave function of an incompressible state. We will instead follow the more intuitive "Composite Fermion" approach due to Jain to understand this state.

The starting point for the FQH state is of course the same as for the integer quantum Hall states, i.e. electrons in a magnetic field that occupy Landau levels. As we noticed in week 3, every state in a single Landau level is at exactly the same energy. The simplest family of FQH states are ones where the lowest Landau level states are only partially filled. Since there is no kinetic energy, the state is determined entirely by optimizing the Coulomb repulsion such that the electrons are as far away from each other as possible.

The composite fermion theory postulates that electrons manage to space themselves out by associating themselves with "vortex"-like excitations. As you hopefully recall, a vortex in a superconductor is a defect where the superconducting phase $\varphi$ winds by $2\pi$ when going around the vortex. An electron going around the vortex picks up a $\pi$-phase shift. On the other hand, an electron can go around a double vortex and pick up effectively no (i.e. $2\pi$) phase shift. However, the electron feels a phase gradient or a vector potential ${\bf A}={\bf\nabla}\varphi$ as it goes around the vortex. Such a vector potential is like a magnetic field and repels the electron.

Of course we have no superconductivity at hand, but we can mimic the vortex properties using a mathematical trick involving complex numbers. First let us introduce complex coordinates for the electrons $z=x+iy$. Then we notice that we can insert a double vortex at $z_0$ in a gas of electrons with wave function $\Psi(z_1,\dots)$ by the transformation

$$
\Psi(z_1,\dots)\rightarrow \prod(z_i-z_0)^2\Psi(z_1,\dots).
$$

> The basic trick of composite fermions in trying to keep electrons far apart is to say that each electron binds  an even number $(2m)$ vortices to form a composite fermion.

This amounts to the transformation of the many-body wave function $\Psi_{CF}(z_1,z_2,\dots)=\prod_{i < j}(z_i-z_j)^2\Psi(z_1,z_2,\dots)$, where $z_j$ are the electron wave-functions.

Pictorially the composite fermion transformation is represented as:

![](figures/composite.svg)

The next step in the composite fermion approach to the FQH state is to say that all the correlation effects of the Coulomb interaction are taken care of by the flux attachment. Beyond this, the composite fermions are weakly interacting particles. If we believe in this picture, then the only non-interacting incompressible states that we can get are integer quantum Hall states. This means that the FQH states are integer quantum Hall states of the composite fermions.

How does this explain a fractionally filled state? Well, the original electron is $2m$ flux quanta together with a composite fermion. If we smear out the flux created by the electron density $\nu$, we get a magnetic field of $2m\nu$ flux quanta per unit area. This is in addition to the one flux quantum per unit area of the external magnetic field. Therefore the composite fermions, which are at a density of $\nu$ per unit area, see a magnetic field of $2m\nu+1$ per unit area. We can make the composite fermions form an incompressible state with $p$-Landau levels filled if
$\nu=p(2m\nu+1),$ so that we describe a state of filling

$$
\nu=\frac{p}{2 m p-1}.
$$

Thus the composite fermion theory provides an explanation for how electrons can form incompressible states at a fractional sequence of filling fractions that is known as the "Jain sequence". These states were all seen in experiments.

```{multiple-choice} Composite fermions allow one to explain incompressible states at fractional filling of the Landau levels by postulating that:
:explanation: Composite fermions are electrons bound to fluxes. Electrons are the fundamental particles and they cannot change their charge. The fractional charged quasiparticles are invoked by composite fermions not explained by the theory.  The incompressible liquid is true for either integer or fractional quantum Hall.
:correct: 3
- The quantum Hall system forms an incompressible liquid.
- The fractionally charged quasiparticles bind to fluxes to reduce the filling.
- The electrons become fractionally charged.
- The electrons bind to fluxes and reduce the effective magnetic field.
```

## Classification and fractional topological insulators

Before we approach the classification of topological insulators in the presence of symmetries, let us discuss the fractional quantum Hall effect. In fact, there is a whole bunch of fractional quantum Hall states, so there is clearly room for classification. However, at first glance it looks more challenging because we cannot really solve general two dimensional interacting Hamiltonians. The tool that is used to understand what phases might exist is braiding. Based on all the examples of two-dimensional topological states with no symmetry that we have so far, it is believed that distinct topological states are characterized by distinct particle-like anyonic excitations with distinct topological properties. It is certainly obvious that if two states have topologically distinct excitations in the bulk they cannot be adiabatically deformed into one another, since the braiding rules cannot change continuously.

So the basic rule of the game is to ask what are all possible braiding rules for excitations in two dimensions. One would think that it would simply be arbitrary. Turns out that the situation is not quite as bad - locality and unitarity put rather strong constraints on the possible braidings of particles. The answer is obtained through a branch of mathematics called modular tensor category theory, and the theory tells us that valid sets of fractional excitations must obey the so-called pentagon and hexagon equations. All this being said, not all solutions of these equations are known - so basically the set of possible phases is not quite known. And this is all very abstract - and not even all the abstractly known phases that have acceptable braiding rules are known to be realized in nature. In fact, so far most of the known phases seem to be composite fermion ones that are well understood.

### Symmetries

To approach the classification of interacting topological insulators with symmetries, we can start by playing the same game as Kane and Mele, and combine two fractional quantum Hall states (instead of integer ones) to make a fractional topological insulator. If we choose a pair of FQH states which are related by time-reversal and stack them together for spin-up and spin-down electrons, that technically leads to a time-reversal invariant state. The key question that needs to be asked is whether one can gap out the edge states by adding time-reversal invariant perturbations. If one can do that, then unlike the Kane-Mele quantum spin Hall state, the state is not a phase that is protected by just time-reversal symmetry. This question is not too mathematically involved, though still beyond this course and can be answered by the bosonization technique as was done by [Stern and Levin](https://arxiv.org/abs/0906.2769).

We can however explain the result. If one stacks the two FQH states one obtains a spin-Hall conductance $\sigma_{sh}$, which is equal to the Hall conductance of each layer. Let the smallest charge of an excitation of our phase be $e^*$, some fraction of electron charge. It turns out that the edge states are protected from gapping by time-reversal invariant perturbations if and only if $\sigma_{sh}/e^*$ is an odd integer. This gives some idea as to what kind of interacting analogues of quantum spin Hall states one may get. But again, as with the non-symmetric case, the general classification is still up in the air. More importantly, we don't really have realistic candidates for such states yet.

## Conclusions

```{youtube} zrL-qxjKfGw
:width: 560
:height: 315
```
