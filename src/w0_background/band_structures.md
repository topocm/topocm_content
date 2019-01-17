```python
import sys
sys.path.append('../code')
from init_mooc_nb import *
init_notebook()
```

# A quick review of band structures

## Quicker intro to quantum mechanics from waves to electrons
For most of this course, all you would need to know 
quantum mechanics is that particles should really be treated
as waves. We can always write a wave equation for waves in the form of the famous Schrodinger equation 
$$i\hbar\partial_t \Psi = H\Psi,$$
where at this point $\Psi$ is the "wave-function" and $H$ is the Hamiltonian. 

Just to give you a sense of what a Schrodinger equation might look like let us convert a familiar wave-equation for a string to a Schrodinger-like form. You must have seen a wave-equation for a string that looks like $$\partial_t^2 h-c^2\partial_x^2 h=0,$$ where $h(x,t)$ is the vertical displacement of the string. This wave-equation is second order in time. Let's try to make it first order like the Schrodinger equation by defining $h_1(x,t)=c^{-1}\int_{-\inf}^x dx_1 \partial_t h(x_1,t)$. After doing this we see that our wave-equation turns into a pair of equations that are linear order in time:
$$\partial_t h = c\partial_x h_1$$ and 
$$\partial_t h_1=-c\partial_x h.$$

We can turn this into the Schrodinger equation if we define: $$\Psi(x,t)=\left(\begin{array}{c}h(x,t)\\h_1(x,t)\end{array}\right)\quad H=c\left(\begin{array}{cc}0& i\\-i & 0\end{array}\right)\partial_x.$$ Now those of you who know basic quantum mechanics might say this is a very strange Schrodinger equation. But this indeed is the wave-function for helical Majorana particles that we will encounter later on.

The wave-function $\Psi$ in the Schrodinger equation that describes electrons is typically a complex though the Hamiltonian is not a matrix (thankfully):$$H=-\frac{\hbar^2}{2m}\partial_x^2 + V(x),$$ where $m$ is the mass of the electron and $V(x)$ is the background potential energy over which the electron is moving.

The main things you should remember about wave equations for electrons is that (a) $\Psi(x,t)$ is complex, (b) H is a Hermitean (clarified later)  matrix or operator (c) density of electrons are related to $|\Psi(x,t)|^2$. The last more subtle point we need to talk about, which has to do with materials containing many electrons, is the \textit{Pauli exclusion principle}. When we have many electrons we have to choose wave-functions for each electron to occupy. These wave-functions must be taken to be "orthogonal" (elaborated later). 

Since we will be interested in static properties of electrons in materials for much of our course, it helps to make the simplofying ansatz: $\Psi=e^{-i E t/\hbar}\psi$.
This ansatz simplifies the Schrodinger equation to a time-independent form:
$$H\psi=E\psi,$$
which resembles the eigenvalue problem in linear algebra.

In fact the linear algebra connection goes further. We will often consider electrons in materials within the so=called "tight-binding" approximation where electrons are assumed to occupy a discrete set of orbitals on atoms. We will then take $\psi_a$ to denote the wave-function amplitude of the electron on orbital $a$. We then consider $\psi_a$ to be the components of the wave-function $\psi$, which then becomes a vector. In this linear algebra analogy the Hamiltonian $H$ is seen as a matrix with components $H_{ab}$. With these definitions, the time-independent Schrodinger equation from the last paragraph really becomes an eigenvalue problem. Once we know how to set-up the matrix $H_{ab}$ to model a particular material, we can extract the properties of the material from the wave-function components $\psi_a$ and energy (eigenvalue) $E$. How these are concretely done will become clearer as the course progresses.
<!-- YOUR TEXT GOES HERE -->