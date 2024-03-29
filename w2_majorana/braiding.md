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

# Why Majoranas are cool: braiding and quantum computation

```{code-cell} ipython3
:tags: [remove-cell]

import sys

sys.path.append("../code")
from init_course import *

init_notebook()
```

## Braiding of Majoranas

```{code-cell} ipython3

Video("Ndf2Z84g1R0")
```

## Majorana zero modes in nanowire networks

As you just heard in the video, the goal of this lecture is to compute the quantum statistics of Majorana zero modes. In order to do this, we will have in mind a nanowire network where Majorana modes can be exchanged in space, like this one:

![](figures/nanowire_network.svg)

In the drawing, you can see a nanowire with many T-shaped junctions in between several Majorana zero modes (which is why we call it a network). We will not worry about the microscopic description of the nanowire network, which will differ in irrelevant ways from similar structures in alternative platforms for Majoranas (we'll learn about those later, in week 7). Just to fix the ideas, you can imagine that the system can be effectively described by the Kitaev chain toy-model, and that the Majoranas are at the positions of domain walls where the gap changes sign, as you saw in the first week of the course.

The only thing that distinguishes the Majorana zero modes is their position in the network. They have no other “flavour” that would allow us to characterize them. They are identical to each other, just like all electrons are identical to each other. If we exchanged two Majoranas in space, the system after the exchange would look exactly the same as it looked before the exchange.

>It is very interesting to ask what is the behaviour of the quantum state $\left|\Psi\right\rangle$ of a system of identical particles under the exchange of two of the particles. You already know that for bosons and fermions $\left|\Psi\right\rangle\,\to\,\pm\left|\Psi\right\rangle$. To see what happens in the case of Majoranas, we first have to learn how to write down the quantum state $\left|\Psi\right\rangle$ corresponding to a set of Majoranas like the one sketched above.

+++

### The Hilbert space of a set of Majoranas

From now on, it is important to keep in mind that by considering only the states corresponding to the Majorana zero modes, we are neglecting the existence of the states that live in the bulk. As mentioned in the video, we assume that the energy spectrum looks like this:

![](figures/gs_manifold.svg)

Based on your knowledge of the Kitaev chain, this assumption should sound reasonable to you. Because you have several Majoranas, there will be several states all at zero energy, forming a “ground state manifold”.

+++

Let's now explore more in detail the ground state manifold defined by this degenerate sets of states.

+++

In the drawing you see six Majoranas, that is three pairs, but let's consider here the more general case of $N$ pairs. It might appear that since the $\gamma_n$s don't appear in the Hamiltonian, there is a degenerate quantum state for each of the $2N$ values of $n$. However, just as Majorana modes appear in pairs, they can be assigned quantum states only in pairs.

>To assign quantum states to Majoranas, we can pair the Majoranas and form fermionic modes,

$$
c^\dagger_n = \tfrac{1}{2}(\gamma_{2n-1}+i\gamma_{2n})\,,\\
c_n =\tfrac{1}{2}(\gamma_{2n-1}-i\gamma_{2n})\,,
$$

for $n=1,\dots, N$. Using this notation, we have chosen to pair neighboring Majoranas into a fermionic mode. We have now a set of $N$ fermionic modes with corresponding creation and annihilation operators. Every mode can be empty or it can be occupied by a fermion, giving us two possible degenerate quantum states $\left|0\right\rangle$ and $\left|1\right\rangle$ for each pair of Majoranas.

+++

Going back to our sketch, we can represent the situation as follows:

![](figures/majoranas_pairing.svg)

The coloring of the Majorana modes now makes explicit our choice of how to pair them into fermionic modes. In total, the system above has 8 possible states, corresponding to all the possible combinations of the occupation numbers of the 3 fermionic modes. Generalizing, we will have $2^N$ possible quantum states for $N$ pairs of Majoranas. We can represent each such state with a ket

$$
\left| s_1, s_2, \dots, s_N\right\rangle\,,
$$

where $s_n$ is equal to $0$ if the $n$-th fermionic mode is not occupied, and equal to $1$ if it is occupied. These states are a *complete basis* for the Hilbert space of the set of Majorana modes. Note that these basis states are all eigenstates of the operators $P_n \equiv 1-2c^\dagger_n c_n \equiv i\gamma_{2n-1}\gamma_{2n}$. For instance, we have that

$$
P_1 \left| 0, \dots \right\rangle\ = (1-2c^\dagger_1 c_1)\left|0, \dots \right\rangle= + \left|0, \dots \right\rangle\,,
$$



$$
P_1 \left| 1, \dots \right\rangle\ = (1-2c^\dagger_1 c_1)\left|1, \dots \right\rangle= - \left|1, \dots \right\rangle\,,
$$

and so on. The operator $P_n$ is the *fermion parity operator* for the pair of Majoranas $\gamma_{2n-1}$ and $\gamma_{2n}$. At this point it is useful to remind you that different Majorana operators all anticommute with each other. This means that the product of a pair of Majorana operators commutes with the product of a different pair, for instance:

$$
(\gamma_1\gamma_2)(\gamma_3\gamma_4) = (\gamma_3\gamma_4)(\gamma_1\gamma_2)\,.
$$

However, if the two pairs share a Majorana, then they do not commute anymore, for instance:

$$
(\gamma_1\gamma_2)(\gamma_2\gamma_3) = - (\gamma_2\gamma_3)(\gamma_1\gamma_2)\,.
$$

Of course, the product above can also be simplified: since $\gamma_2^2=1$, you have that $(\gamma_1\gamma_2)(\gamma_2\gamma_3)=\gamma_1\gamma_3$.
 All $P_n$'s commute with each other, because they all involve a different pair of Majoranas. 
 
> Thus the  Hilbert space of states $|\Psi\rangle$ of a set of $N$ pairs of Majorana modes is spanned by the simultaneous eigenstates $|s_1,s_2,\dots,s_N\rangle$ of the commuting fermion parity operators $P_n$ and is written as
>
> $$
  \left|\Psi\right\rangle= \sum_{s_n=0,1} \alpha_{s_1s_2\dots s_N}\,\left| s_1, s_2, \dots, s_N\right\rangle\,
  $$

with complex coefficients $\alpha_{s_1s_2\dots s_N}$. 

 At this point an important consideration is in order. You will remember learning during the first week that, while a superconducting Hamiltonian may not conserve the total number of electrons due to the creation and annihilation of Cooper pairs, the parity of the number of electrons is always conserved. 
We can obtain the *total fermion parity* by multiplying all the operators $P_n$,

$$
P_\textrm{tot}=P_1\cdot P_2\cdot\, \dots\, \cdot P_N = i^N\,\gamma_1\gamma_2\dots\gamma_{2N}\,.
$$

The operator $P_\textrm{tot}$ has eigenvalues $s_1 s_2\dots s_N=\pm 1$, depending on whether the total number of occupied fermionic modes is even or odd. Applied to our case, this means that it is only meaningful to consider states $\left|\Psi\right\rangle$ which are *eigenstates* of the operator $P_\textrm{tot}$, that is

$$
P_\textrm{tot}\left|\Psi\right\rangle=\pm\left|\Psi\right\rangle\,.
$$

In particular, linear combinations of states with different total parity are forbidden. You can see this condition as a constraint on the allowed values of the coefficients $\alpha_{s_1s_2\dots s_N}$.

This consideration only applies to closed systems. It does not apply if we are considering a system which is in contact with a reservoir of electrons, such as a metallic lead, in which case electrons may tunnel in and out of the lead, changing the total parity of the system. Equivalently, it does not apply if we are considering only a part of the total system. You could for instance imagine that, in our sketch, there are more Majorana zero modes in the part of the network which is not drawn explicitly (represented by the dots which “continue” the nanowire). In such a case it is perfectly possible that the *total* network is in, say, a state of even parity, but that the subsystem under consideration is in a superposition of even and odd parity states.

```{code-cell} ipython3

question = (
    "Consider an isolated system with N=7 pairs of Majoranas, and an even total fermion parity. "
    "What is the ground state degeneracy of the system?"
)
answers = [
    "Trick question - it is not possible to get N=7 pairs of Majorana modes with even parity.",
    "2^7.",
    "2^6.",
    "14",
    "The system has an energy gap, so it cannot be degenerate.",
]
explanation = (
    "7 pairs of Majoranas means a Hilbert space with dimension 2^7, "
    "out of which half have even total parity and half have odd total parity. "
    "So the degeneracy at fixed even parity is 2^6."
)
MultipleChoice(
    question, answers, correct_answer=2, explanation=explanation
)
```

## Non-Abelian statistics of Majoranas

Let's now imagine that experimentalists are not only able to build such a network, but also to move the position of the domain walls and swap the positions of two Majoranas, for instance by performing the following trajectory:

![](figures/nanowire_network_exchange.svg)

Let's suppose that the trajectory takes a time $T$. During the trajectory, the system is described by a time-dependent Hamiltonian $H(t)$, $0\leq t \leq T$. This Hamiltonian contains all the details of the system, such as the positions of the domain walls where the Majoranas are located. Because the final configuration of the system is identical to the initial one, for instance all the domain walls are in the same positions as in the beginning, we have that $H(0)=H(T)$. In other words, we are considering a *closed trajectory* which brings the Hamiltonian back into itself. To ensure that the wave-function for the system does not leave the ground state manifold of states $|\Psi\rangle$, we need to change the Hamiltonian $H(t)$ slowly enough to obey the [adiabatic theorem](https://en.wikipedia.org/wiki/Adiabatic_theorem). 

So let's imagine that we are in the adiabatic limit and that we exchange two Majoranas $\gamma_n$ and $\gamma_m$. As usual in quantum mechanics, the initial and final quantum states are connected by a unitary operator $U$ ($U^{-1}=U^\dagger$),

$$
\left|\Psi\right\rangle \,\to\, U \left|\Psi\right\rangle\,.
$$

Because the quantum state $\left|\Psi\right\rangle$ never leaves the ground state manifold, which has $2^N$ states, the operator $U$ can be written a $2^N\times 2^N$ unitary matrix.

We can derive the exact form of $U$ without a direct calculation, which would require knowing $H(t)$, but only based on the following, general considerations. First, the adiabatic exchange of two Majoranas does not change the parity of the number of electrons in the system, so $U$ commutes with the total fermion parity, $[U, P_\textrm{tot}]=0$. Second, it is reasonable to assume that $U$ only depends on the Majoranas involved in the exchange, or in other words that it is a function of $\gamma_n$ and $\gamma_m$, and of no other operator. And because it has to preserve fermion parity, it can only depend on their product, that is on the parity operator $-i\gamma_n\gamma_m$, which is Hermitian. Finally, the exponential of $i$ times a Hermitian operator is a unitary operator. So, in general $U$ must take the form

$$
U\equiv\exp(\beta \gamma_n \gamma_m) = \cos(\beta) + \gamma_n\gamma_m \sin(\beta)\,,
$$

*up to an overall phase*. Here, $\beta$ is a real coefficient to be determined, and in the last equality we have used the fact that $(\gamma_n\gamma_m)^2=-1$. To determine $\beta$, it is convenient to go to the [Heisenberg picture](https://en.wikipedia.org/wiki/Heisenberg_picture) and look at the evolution of the Majorana operators in time. We have that

$$
\gamma_n\,\to\,  U\,\gamma_n\,U^\dagger\,,\\
\gamma_m\,\to\,  U\,\gamma_m\,U^\dagger\,.
$$

Inserting our guess for $U$ we obtain:

$$
\gamma_n\,\to\,   \cos (2\beta)\,\gamma_n  - \sin(2\beta)\,\gamma_m\,,\\
\gamma_m\,\to\,   \cos (2\beta)\,\gamma_m  + \sin(2\beta)\,\gamma_n\,.
$$

Now we have to remember that at time $T$ we have completed a closed trajectory, so that the Majorana $\gamma_n$ is now in the place initially occupied by $\gamma_m$, and vice versa. This condition leads to the choice $\beta = \pm \pi/4$. It is not strange that we find that both signs are possible - this distinguishes the clockwise and the counterclockwise exchange of the Majoranas. 

>Thus, we can write the unitary operator that exchanges the Majorana modes $\gamma_n$ and $\gamma_m$ in an explicit (and somewhat non-trivial looking!) form as:

$$
U = \exp \left(\pm\frac{\pi}{4}\gamma_n \gamma_m\right) = \tfrac{1}{\sqrt{2}}\left(1\pm\gamma_n\gamma_m\right)
$$


+++

To fix our ideas and study the consequences of $U$ more closely, it is convenient to just focus on four Majoranas $\gamma_1\,\gamma_2,\gamma_3$ and $\gamma_4$. For this discussion we will assume that counter-clockwise exchanges pick the $+$ sign in $U$. Their ground state manifold has four states, which in the notation introduced before we write down as

$$
\left|00\right\rangle, \left|11\right\rangle, \left|01\right\rangle, \left|10\right\rangle\,,
$$

where the first digit is the occupation number of the fermionic mode $c^\dagger_1=\tfrac{1}{2}(\gamma_1+i\gamma_2)$ and the second digit the occupation number of $c^\dagger_2=\tfrac{1}{2}(\gamma_3+i\gamma_4)$. The most generic possible wave function is a superposition

$$
\left|\Psi\right\rangle = s_{00}\left|00\right\rangle + s_{11} \left|11\right\rangle + s_{01} \left|01\right\rangle + s_{10} \left|10\right\rangle\,,
$$

which we can also represent as a vector with four entries, $\left|\Psi\right\rangle = (s_{00}, s_{11}, s_{01}, s_{10})^T$. The operator $U$ at this point can be written as a $4\times 4$ matrix. In order to do so, you just have to compute the action of a product of Majoranas on the basis states. This a simple but tedious operation, which we skip here. It results in the following matrices for the operators $U_{12}, U_{23}$ and $U_{34}$ exchanging neighboring Majoranas:

$$
U_{12} = \exp\left(\frac{\pi}{4}\gamma_1 \gamma_2\right) \equiv\begin{pmatrix}
e^{-i\pi/4} & 0 & 0 & 0 \\0 & e^{i\pi/4} & 0 &0 \\0 & 0& e^{-i\pi/4} &0 \\ 0&0& 0& e^{i\pi/4}
\end{pmatrix}\,,
$$



$$
U_{23} = \exp\left(\frac{\pi}{4}\gamma_2 \gamma_3\right) \equiv\frac{1}{\sqrt{2}}\begin{pmatrix}
1 & -i & 0 & 0\\ -i & 1 & 0& 0\\ 0& 0& 1 & -i\\ 0& 0& -i & 1
\end{pmatrix}\,,
$$



$$
U_{34} = \exp\left(\frac{\pi}{4}\gamma_3 \gamma_4\right) \equiv\begin{pmatrix}
e^{-i\pi/4} & 0 & 0 & 0\\ 0& e^{i\pi/4} & 0& 0\\ 0& 0& e^{i\pi/4} & 0\\ 0& 0& 0& e^{-i\pi/4}
\end{pmatrix}\,.
$$

These matrices indeed act in a very non-trivial way on the wave function. For instance, if we start from the state $\left|00\right\rangle$ and we exchange $\gamma_2$ and $\gamma_3$, we obtain

$$
\left|00\right\rangle\,\to\,U_{23}\left|00\right\rangle=\tfrac{1}{\sqrt{2}}\left(\left|00\right\rangle-i\left|11\right\rangle\right)\,,
$$

which is a superposition of states! Hence we have seen explicitly that the effect of the exchange two Majoranas on the wavefunction amounts to much more than just an overall phase, as it happens for bosons and fermions.

Let's now try a sequence of two exchanges. In this case, we have to multiply the corresponding $U$s, ordering them from right to the left according to the order of the exchanges. Given that the matrices above are not diagonal, it is not surprising that the order in the product matters a lot. For instance you can check that

$$
U_{23}U_{12}\neq U_{12}U_{23}\,
$$

>We have just shown that exchanging two Majorana modes leads to a non trivial rotation in the ground state manifold, and that changing the order of the exchanges changes the final result. These properties make Majorana modes **non-Abelian anyons**. The exchange of two non-Abelian anyons is usually called **braiding**, a name which is suggestive of the fact that, when thinking of the trajectories of the different particles, a sequence of exchanges looks like a braid made out of different strands.

Finally, you might object to the fact that the network of nanowires drawn in the figures only allows to exchange neighbouring Majoranas, even though our derivation of $U=\exp(\pi\gamma_n\gamma_m/4)$ seems to hold for any pair of Majoranas. This geometric constraint is not a big problem: by carefully composing many exchanges between neighbours, we can exchange any pair of Majoranas. As an example, you have that $U_{13}\equiv\exp\left(\pi\gamma_1 \gamma_3/4\right) = U_{12}^\dagger\,U^\dagger_{23}\,U_{12}$.

```{code-cell} ipython3

question = (
    "Consider a system with only one pair of Majorana modes, thus with just two degenerate states with different fermion parity. "
    "What happens when we exchange the pair of Majorana modes, starting from a given fermion parity eigenstate?"
)
answers = [
    "The fermion parity of the state flips.",
    "Nothing happens.",
    "The system wave-function picks up a phase that depends on the fermion parity.",
    "You end up in a superposition of the two states.",
]
explanation = (
    "The total fermion parity cannot change, "
    "but the two states can pick up a different phase. "
    "This is indeed what happens since the operator $U$ describing the exchange depends on fermion parity."
)
MultipleChoice(
    question, answers, correct_answer=2, explanation=explanation
)
```

## Majoranas and quantum computation: basic ideas

The non-Abelian statistics of Majorana modes is a very special property. Furthermore, it has some practical interest, since it could be used to realize a robust **quantum computer**. (If you are not yet interested in quantum computation, you can skip this part, even though we suggest that you get interested in it! Quantum computation is a huge topic of research, but [this](https://arxiv.org/abs/quant-ph/9708022) is a good place to start learning.)

Let's discuss very briefly how this can be done.

First, we can think of our network of nanowires with $2N$ Majoranas as a small computer. The $2^N$ states of the ground state manifold can encode a string of $N$ bits, so it's like having a small *register*. As always in quantum computation, and unlike in a classical computer, the register can be in a superposition of different states. So far, nothing really special about Majoranas.

How do we execute an *algorithm* on our register? Simply by exchanging the Majorana modes! Because of the non-Abelian statistics, different sequences of exchanges will yield different algorithms. Of course, to execute an interesting algorithm we may need a lot of Majorana modes and a very very long sequence of exchanges. However, it all begins with the small building blocks, the matrices that you have just studied in detail.

You might say that this is just another way to obtain a given unitary operator acting on the wave function. The beautiful thing, though, is that both the state of the register and the algorithms are *topologically protected*. Let's explain what we mean by that.

The state of the register is encoded in the fermion parity degrees of freedom, which are shared *non-locally* by the Majoranas. This means that no local perturbation can change the state of the register and cause *decoherence* of the quantum state. The environment cannot access the information stored in the Majoranas, as long as they are kept far away from each other. The only exception is a change in fermion parity due to the tunnelling of a stray quasiparticle into the system (this is the problem of quasiparticle poisoning, the same that can hinder the detection of the $4\pi$-periodic Josephson effect of Majorana modes, as you heard from Carlo Beenakker). But except from this, the Majoranas are a great *quantum memory*.

On the other hand, every step of the algorithm will be extremely accurate because it is given by an exchange of two Majoranas, which corresponds to *exactly* $\exp(\pi\gamma_n\gamma_m/4)$. When you are in the adiabatic limit, this operator does not depend on any of the details on how the exchange between Majoranas is performed. It does not depend on *how* you move the Majoranas, or on the particular trajectory that $\gamma_n$ and $\gamma_m$ followed, or on the timing of the trajectory. So the final result is extremely reliable.

These are the basic ideas of **topological quantum computation**. It is incredible that we can find condensed matter systems, such as networks of Majoranas, which are naturally endowed with these characteristics. 

## Summary

```{code-cell} ipython3

Video("V3e9r4S8GHs")
```
