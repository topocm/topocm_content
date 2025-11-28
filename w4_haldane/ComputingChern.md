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

# Additional notes on computing Chern number

Computing the Chern number from the Berry connection  $\bf{a}(\bf {k})=i\langle u(\bf{k})|\bf{\nabla}(|u(\bf{k})\rangle)$ is annoying because one needs to find a gauge where the Bloch wave-functions $u_n({\bf k})$ are continuous.

On the other hand, the Chern number is really the integral of the Berry curvature

$$
{\bf{b}(k)}={\bf\nabla\times a(k)}
$$

as

$$
\Phi=\oint d^2\bf{k}\bf{z}\cdot \bf{b}(\bf{k}).
$$

Numerically it is more convenient to compute the integral $\Phi$ by breaking it down into small plaquettes, so that

$$
\Phi=\sum_n \oint_{\Gamma_n} d^2\bf{k}\bf{z}\cdot \bf{b}(\bf{k})=\sum_n \oint_{\Gamma_n} d{\bf k}\cdot {\bf a(k)},
$$

is broken down into chunks

$$
\Phi_n=i\oint_{\Gamma_n} d{\bf k}\cdot {\langle u(\bf{k})|\bf{\nabla}(|u(\bf{k})\rangle)}.
$$

For sufficiently small chunks $\Phi_n$ is small and one can get away with computing the exponential

$$
e^{i\Phi_n}=e^{\oint_{\Gamma_n} d{\bf k}\cdot {\langle u(\bf{k})|\bf{\nabla}(|u(\bf{k})\rangle)}}=\prod_p e^{\delta{\bf k}_{n,p}\cdot {\langle u(\bf{k}_{n,p})|\bf{\nabla}(|u(\bf{k}_{n,p})\rangle)}}\approx \prod_p (1+\delta k_{n,p}\langle u(\bf{k}_{n,p})|\bf{\nabla}(|u(\bf{k}_{n,p})\rangle)\approx \prod_p \langle u(\bf{k}_{n,p})|u(\bf{k}_{n,p+1})\rangle.
$$

+++

The flux on the small plaquette can be computed as

$$
\Phi_n=\textrm{Arg}(\prod_p \langle u({\bf k}_{n,p})|u({\bf k}_{n,p+1})\rangle).
$$

What is nice about this product is that it is gauge invariant as can be checked by multiplying each wave-function $|u({\bf k}_{n,p})\rangle\rightarrow e^{i\varphi({\bf k}_{n,p})}|u({\bf k}_{n,p})\rangle$.

The nice thing about this expression is that one can also generalize this to multiband systems to calculate the total Chern number so that the contribution from each plaquette

$$
e^{i\Phi_n}\approx \prod_p\prod_s \langle u_s(\bf{k}_{n,p})|u_s(\bf{k}_{n,p+1})\rangle=\prod_p Det[\langle u_s(\bf{k}_{n,p})|u_s(\bf{k}_{n,p+1})\rangle],
$$

where $s$ labels the band index.

What Vanderbilt and coworkers pointed out is that this expression can be written as

$$
e^{i\Phi_n}=\prod_p Det[\langle u_s(\bf{k}_{n,p})|u_{s'}(\bf{k}_{n,p+1})\rangle],
$$

is related to determinants of a bunch of matrices $\langle u_s(\bf{k}_{n,p})|u_{s'}(\bf{k}_{n,p+1})\rangle$, which in the diagonal basis of eigenstates is nearly diagonal, which takes us back to the previous expression.

The main advantage of this expression is that it is actually $U(N)$ invariant for any unitary transformation of the $N$ occupied eigenstates.

## Final recipe

So the final recipe to compute the Chern number is as follows:

* grid up the BZ into small plaquettes labelled by $n$

* Compute the flux through each plaquette

$$
\Phi_n=Arg[\prod_p Det[\langle u_s(\bf{k}_{n,p})|u_{s'}(\bf{k}_{n,p+1})\rangle]],
$$

where ${\bf k}_{n,p}$ are momenta on the corners of the lattice.

* The Chern number is calculated as

$$
\nu=(2\pi)^{-1}\sum_n \Phi_n.
$$
