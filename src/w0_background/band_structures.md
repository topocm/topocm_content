```python
import sys
sys.path.append('../code')
from init_mooc_nb import *
init_notebook()
```

# A quick review of band structures

## Quicker intro to quantum mechanics from waves to electrons
For most of this course, all you would need to know about 
quantum mechanics is that particles should really be treated
as waves. The equation for any wave can be recast  in to  the form of the famous Schrodinger equation 
$$i\hbar\partial_t \Psi = H\Psi,$$
where at this point $\Psi$ is the "wave-function" and $H$ is the Hamiltonian. 

Just to give you a sense of what a Schrodinger equation actually looks like let us convert a familiar wave-equation for a string to a Schrodinger-like form. You must have seen a wave-equation for a string that looks like $$\partial_t^2 h-c^2\partial_x^2 h=0,$$ where $h(x,t)$ is the vertical displacement of the string. This wave-equation is second order in time. Let's try to make it first order like the Schrodinger equation by defining $h_1(x,t)=c^{-1}\int_{-\inf}^x dx_1 \partial_t h(x_1,t)$. After doing this we see that our wave-equation turns into a pair of equations that are linear order in time:
$$\partial_t h = c\partial_x h_1$$ and 
$$\partial_t h_1=-c\partial_x h.$$

We can turn this into the Schrodinger equation if we define: $$\Psi(x,t)=\left(\begin{array}{c}h(x,t)\\h_1(x,t)\end{array}\right)\quad H=c\left(\begin{array}{cc}0& i\\-i & 0\end{array}\right)\partial_x.$$ Now those of you who know basic quantum mechanics might say this is a very strange Schrodinger equation. But this indeed is the wave-function for helical Majorana particles that we will encounter later on.

The wave-function $\Psi$ in the Schrodinger equation that describes electrons is typically a complex though the Hamiltonian is not a matrix (thankfully):$$H=-\frac{\hbar^2}{2m}\partial_x^2 + V(x),$$ where $m$ is the mass of the electron and $V(x)$ is the background potential energy over which the electron is moving.

The main things you should remember about wave equations for electrons is that 

* $\Psi(x,t)$ is complex, 
* H is a Hermitean (clarified later)  matrix or operator 
* density of electrons are related to $|\Psi(x,t)|^2$.
* If N is the number of electrons, one needs to occupy $N$ orthogonal wave-functions to occupy.

The last point is more subtle and is called the **Pauli exclusion principle**. We will elaborate on orthogonality later.

Since we will be interested in static properties of electrons in materials for much of our course, it helps to make the simplifying ansatz: $\Psi=e^{-i E t/\hbar}\psi$.
This ansatz simplifies the Schrodinger equation to a time-independent form:
$$H\psi=E\psi,$$
which resembles the eigenvalue problem in linear algebra.

In fact, the linear algebra connection goes further. We will often consider electrons in materials within the so-called "tight-binding" approximation where electrons are assumed to occupy a discrete set of orbitals on atoms. We will then take $\psi_a$ to denote the wave-function amplitude of the electron on orbital $a$. We then consider $\psi_a$ to be the components of the wave-function $\psi$, which then becomes a vector. In this linear algebra analogy the Hamiltonian $H$ is seen as a matrix with components $H_{ab}$. With these definitions, the time-independent Schrodinger equation from the last paragraph really becomes an eigenvalue problem. Once we know how to set-up the matrix $H_{ab}$ to model a particular material, we can extract the properties of the material from the wave-function components $\psi_a$ and energy (eigenvalue) $E$. How these are concretely done will become clearer as the course progresses.

Physicists have a funny but convenient notation for doing linear algebra called the Dirac "bra-ket" notation. In this notation, wave-functions such as $\psi$ are represented by "kets" i.e. $\psi\rightarrow |\psi\rangle$. The components of the wave-function $\psi_a$ (i.e. the real information content) get represented by the equation: $$|\psi\rangle=\sum_a \psi_a |a\rangle.$$
Similarly the Hamiltonian $H$ is elevated to being an operator defined as:$$H=\sum_{ab}H_{ab}|a\rangle \langle b|.$$ The object $\langle b|$ is called a bra and together with the ket it forms a "bra-ket" with the property $\langle b| a\rangle=\delta_{ab}$. The Schrodinger equation now looks like $$H|\psi\rangle = E|\psi\rangle,$$
which can be checked to be the same equation as the linear algebra form. 

Let's now do the simple example of electrons stuck in a triangle of atoms, where each atom is assumed to have one orbital. We label the orbitals on the atoms as $|0\rangle,|1\rangle,|2\rangle$. With this labeling, the "hopping amplitude" $t$ of electrons between orbitals is represented by the Hamiltonian $$H=-t(|0\rangle \langle 1|+|1\rangle \langle 2|+|2\rangle \langle 0|)+h.c,$$
where $h.c.$ stands for Hermitean conjugate, which means that you reverse the ordering of the labels and take a complex conjugate. We can also write the Hamiltonian in matrix form $$H_{ab}=-\left(\begin{array}{ccc}0&t&t^*\\t^*&0&t\\t&t^*&0\end{array}\right).$$
You can dump this matrix into Mathematica and it will give you three eigenvectors $\psi^{(n=1,2,3)}_a$ with energy eigenvalues $E^{(n=1,2,3)}=-2 |t| \cos{\theta},|t|\cos{\theta}\pm |t|\sqrt{3}\sin{\theta}$ (where $t=|t|e^{i\theta}$). The corresponding eigenvectors $\psi^{(n=1,2,3)}_a$ are $(1,1,1),(1,\omega,\omega^2),(1,\omega^2,\omega)$ where $\omega$ is the cube-root of unity (i.e. $\omega^3=1$).

## Bloch's theorem for bulk electrons

Actually, we didn't really need Mathematica to solve the problem of an electron in a triangle. We can even solve an N site ring (triangle being $N=3$). The trick is a neat theorem called Bloch's theorem. To understand this model in the context of the tight-binding approximation, let us consider electrons in a crystal. The defining characteristic of a crystal is that the atomic positions repeat in a periodic manner in space. We call the repeating group of orbitals a **unit-cell**. Therefore, all orbitals in a crystal can be labeled as a pair $a=(l,n)$, where $l$ is the orbital poisition in the unit cell and $n$ labels the unit cell. For our example of a atomic ring, $l$ wouldn't be needed and $n$ would take values $1$ to $N$. In a three-dimensional crystal, $n=(n_x,n_y,n_z)$ would be a vector of integers. 

The Hamiltonian for a crystal has matrix elements that satisfy $H_{(l,n),(l',m)}=H_{(l,n-m),(l',0)}$ for all pairs of unit-cell $n$ and $m$. 
> Bloch's theorem states that the Schrodinger equation for such Hamiltonians in crystals can be solved by the ansatz: $$\psi_{(l,n)}=e^{i k n}u_l,$$

where $u_l$ is the periodic part of the Bloch function which is identical in each unit-cell. The parameter $k$ is called crystal momentum and is quite analogous to momentum 
except that it is confined in the range $k\in [-\pi,\pi]$ which is referred to as the **Brillouin Zone**.
You can now substitute this ansatz into the Schrodinger equation: $\sum_{l'm}H_{(l,n),(l',m)}u_{l'}e^{i k m}=E_k e^{i k n}u_{l}$. 
>Thus the Bloch functions $u_l^{(k)}$ and energies $E^{(k)}$ are obtained from the eigenvalue equation (so-called Bloch equation) $$H^{(k)Bloch}u^{(k)}=E^{(k)}u^{(k)},$$

where $$H^{(k)Bloch}_{ll'}=\sum_{m}H_{(l,-m),(l',0)}e^{-i k m}.$$
The Bloch equation written above is an eigenvalue problem at any momentum $k$. The resulting eigenvalues $E^{(n,k)}$ consitute the bandstructure of a material, where the eigenvalue label $n$ is also called a band index. 

### Example: Su-Schrieffer-Heeger model

Let us now work through an example. The Su-Schrieffer-Heeger (SSH) model is the simplest model for polyacetylene, which to a physicist can be thought of as a chain of atoms with one orbital per atom. However, the hopping strength alternates (corresponding to the alternating bond-length ) between $t_1$ and $t_2$. Ususally you could assume that since each orbital has one atom there is only one atom per unit cell. But this would mean all the atoms are identical. On the other hand, in polyacetylene, half the atoms are on the right end of a short bond and half of them are on the left. 
> Thus there are two kinds of atoms - the former kind we label $R$ and the latter $L$. Thus there are two orbitals per unit cell that we label $|L,n\rangle$ and $|R,n\rangle$ with $n$ being the unit-cell label.

The Hamiltonian for the SSH model is $H=\sum_n \{t_1(|L,n\rangle\langle R,n|+|R,n\rangle\langle L,n|)+t_2(|L,n\rangle\langle R,n-1|+|R,n-1\rangle\langle L,n|)\}.$ This Hamiltonian is clearly periodic with shift of $n$ and the non-zero matrix elements of the Hamiltonian can be written as $H_{(L,0),(R,0)}=H_{(R,0),(L,0)}=t_1$ and $H_{(L,1),(R,0)}=H_{(R,-1),(L,0)}=t_2$. 
>The $2\times 2$ Bloch Hamiltonian is calculated to be: $$H^{(k,Bloch)}_{ll'=1,2}=\left(\begin{array}{cc}0& t_1+t_2 e^{i k}\\t_1+t_2 e^{-ik}&0\end{array}\right).$$

We can calculate the eigenvalues of this Hamiltonian by taking determinants and we find that the eigenvalues are $E^{(k,\pm)}=\pm \sqrt{t_1^2+t_2^2+2 t_1 t_2\cos{k}}.$ Since $L$ and $R$ on a given unit-cell surrounded one of the shorter bonds (i.e. with larger hopping ) we expect $t_1>t_2$. As $k$ varies across $[-\pi,\pi]$, E^{(k,+)} goes from $t_1-t_2$ to $t_1+t_2$. Note that the other energy eigenvalue is just the negative $E^{k,-}=-E^{(+,k)}$. 
> As $k$ varies no energy eigenvalue $E^{k,\pm}$ ever enters the range $-(t_1-t_2)$ to $t_1-t_2$. This range is called an **band gap**, which is the first seminal prediction of Bloch theory that explains insulators.

This notion of an insulator will be rather important in our course. So let us dewell on this a bit further. Assuming we have a periodic ring with $2N$ atoms so that $n$ takes $N$ values, single valuedness of the wave-function $\psi_{(l,n)}$ requires that $e^{i k N}=1$. This means that $k$ is allowed $N$ discrete values separated by $2\pi/N$ spanning the range $[-\pi,\pi]$. Next to describe the lower-energy state of the electrons we can fill only the lower eigenvalue $E^{(k,-)}$ with ane electron at each $k$ leaving the upper state empty. This describes a state with $N$ electrons. Furthermore, we can see that to excite the system one would need to transfer an electron from a negative energy state to a positive energy state that would cost at least $2(t_1-t_2)$ in energy. 
> Such a gapped state with a fixed number of electrons cannot respond to an applied voltage and as such must be an insulator. 

This insulator is rather easy to understand in the $t_2=0$ limit and corresponds to the double bonds in the polyacetylene chain being occupied by localized electrons. 

## k.p perturbation theory

Let us now think about how we can use the smoothness of $H^{k,Bloch}$ to predict energies and wave-functions at finite $k$ from $H^{k=0,Bloch}$ and its derivatives. We start by expanding the Bloch Hamiltonian $H^{k,Bloch}=H^{k=0,Bloch}+k H^{'(k=0,Bloch)}+(k^2/2)H^{''(k=0,Bloch)}$. Using standrad perturbation theory 
> we can conclude that the velocity and mass of a non-degenerate band near $k\sim 0$ is written as $v_n = u^{(n)}^\dagger H^{'(k=0,Bloch)} u_n$ and $m_n^{-1}=u^{(n)}^\dagger H^{''(k=0,Bloch)} u_n+\sum_{m\neq n}\frac{|u^{(n)}^\dagger H^{'(k=0,Bloch)} u_n|^2}{E^{(k=0,n)}-E^{(k=0,m)}}$,

where $E^{(k=0,n)}$ and $u^{(n)}$ are energy eigenvalues and eigenfunctions of $H^{(k=0,Bloch)}$. One of the immediate consequences of this is that the effective mass $m_n $ vanishes as the energy denominator $E^{(k=0,n)}-E^{(k=0,m)}$ (i.e. gap ) becomes small. This can be checked to be the case by expanding $E^{(k,-)}\simeq -(t_1-t_2)+\frac{t_2^2}{(t_1-t_2)}k^2.$  