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

# Tight-binding models in a magnetic field: Peierls substitution

```{code-cell} ipython3
:tags: [remove-cell]

# This first cell will be removed by the converter.
```

To understand how the vector potential enters a tight-binding model by the so-called Peierls substitution, let us remind ourselves that the gauge-invariance of the Schrodinger equation requires us to transform the wave-function amplitude or equivalently the creation operator of an electron at a site as

$$
c_j^\dagger \rightarrow c_j^\dagger \exp\left(-i\frac{e}{\hbar c}\Lambda(\bf r_j)\right),
$$

where $\Lambda(\bf r)$ generates the gauge transformation of the vector potential $\bf A(\bf r)\rightarrow \bf A(\bf r)+\bf\nabla \Lambda(\bf r)$. If there is no magnetic field then the vector potential can locally be set to $\bf A=0$ by an appropriate gauge choice of $\bf \Lambda$. The hopping term in the absence of a vector potential is written as $H_t=t_{jl}c_j^\dagger c_l+h.c$, which must gauge transform to

$$
H_t=t_{jl} \exp\left(-i\frac{e}{\hbar c}(\Lambda(\bf r_j)-\Lambda(\bf r_l))\right)c_j^\dagger c_l+h.c=t_{jl} \exp\left(-i\frac{e}{\hbar c}(\int_{\bf r_l}^{\bf r_j} d\bf r'\cdot\bf A(\bf r')\right)c_j^\dagger c_l+h.c.
$$

While this expression is derived for zero magnetic field, by choosing the integration path to be the shortest distance over nearest neighbor bond, this expression is used to include magnetic fields in lattice models. This is referred to as the Peierls substitution for lattices.

+++

If we put our topological nanowire in a ring (as with the Aharonov-Bohm effect) with a junction (as in the figure) and concentrate the magnetic field in the center of the ring, the vector potential $\bf A$ is constrained  by the magnetic flux $\Phi$ as

$$
\oint d\bf {r'\cdot\bf A(\bf r')}=\int d^2\bf {r'\bf \nabla\times \bf A(\bf r')}=\Phi.
$$

Choosing a gauge for the vector potential so that it vanishes everywhere except in the junction the hopping phase $\theta$ for the junction i.e. $H_t=t_{N,1}e^{i\theta}c_N^\dagger c_1+h.c.$ is written as

$$
\theta=\int_{\bf r_l}^{\bf r_j} d\bf r'\cdot\bf A(\bf r')=\pi \Phi/\Phi_0,
$$

where $\Phi_0=hc/2e$ is the superconducting flux quantum.
