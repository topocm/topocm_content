```python
import sys
sys.path.append('../code')
from init_mooc_nb import *
init_notebook()

%output size=150
dims = SimpleNamespace(E_t=holoviews.Dimension(r'$E/t$'),
                       mu_t=holoviews.Dimension(r'$\mu/t$'),
                       lambda_=holoviews.Dimension(r'$\lambda$'),
                       x=holoviews.Dimension(r'$x$'),
                       k=holoviews.Dimension(r'$k$'),
                       amplitude=holoviews.Dimension(r'$|u|^2 + |v|^2$'))

holoviews.core.dimension.title_format = ''

def kitaev_chain(L=None, periodic=False):
    lat = kwant.lattice.chain()

    if L is None:
        syst = kwant.Builder(kwant.TranslationalSymmetry((-1,)))
        L = 1
    else:
        syst = kwant.Builder()

    # transformation to antisymmetric basis
    U = np.array([[1.0, 1.0], [1.j, -1.j]]) / np.sqrt(2)

    def onsite(onsite, p): 
        return - p.mu * U @ pauli.sz @ U.T.conj()
    
    for x in range(L):
        syst[lat(x)] = onsite

    def hop(site1, site2, p):
        return U @ (-p.t * pauli.sz - 1j * p.delta * pauli.sy) @ U.T.conj()
    
    syst[kwant.HoppingKind((1,), lat)] = hop

    if periodic:
        def last_hop(site1, site2, p):
            return hop(site1, site2, p) * (1 - 2 * p.lambda_)
        
        syst[lat(0), lat(L - 1)] = last_hop
    return syst


def bandstructure(mu, delta=1, t=1, Dirac_cone="Hide", show_pf=False):
    syst = kitaev_chain(None)
    p = SimpleNamespace(t=t, delta=delta, mu=mu)
    plot = holoviews.Overlay([spectrum(syst, p, ydim="$E/T$", xdim='$k$')][-4:4])
    h_1 = h_k(syst, p, 0)
    h_2 = h_k(syst, p, np.pi)
    pfaffians = [find_pfaffian(h_1), find_pfaffian(h_2)]
    
    if show_pf:
        signs = [('>' if pf > 0 else '<') for pf in pfaffians]
        title = "$\mu = {mu} t$, Pf$(iH_{{k=0}}) {sign1} 0$, Pf$(iH_{{k=\pi}}) {sign2} 0$"
        title = title.format(mu=mu, sign1=signs[0], sign2=signs[1])
        plot *= holoviews.VLine(0) * holoviews.VLine(-np.pi)
    else:
        if pfaffians[0] * pfaffians[1] < 0:
            title = "$\mu = {mu} t$, topological ".format(mu=mu)
        else:
            title = "$\mu = {mu} t$, trivial ".format(mu=mu)
        
    if Dirac_cone == "Show":
        ks = np.linspace(-np.pi, np.pi)
        ec = np.sqrt((mu + 2 * t)**2 + 4.0 * (delta * ks)**2)
        plot *= holoviews.Path((ks, ec), kdims=[dims.k, dims.E_t])(style={'linestyle':'--', 'color':'r'})
        plot *= holoviews.Path((ks, -ec), kdims=[dims.k, dims.E_t])(style={'linestyle':'--', 'color':'r'})
    return plot.relabel(title)
```

# A quick review of band structures

## Quicker intro to quantum mechanics from waves to electrons
For most of this course, all you would need to know about 
quantum mechanics is that particles should really be treated
as waves. The equation for any wave can be recast  in to  the form of the famous Schrodinger equation 
$$i\hbar\partial_t \Psi = H\Psi,$$
where at this point $\Psi$ is the "wave-function" and $H$ is the Hamiltonian. 

### Motivating the Schrodinger equation
In case you haven't been indoctrinated (skip this and the next paragraph if you have) with quantum mechanics , let me show you how to 
convert a familiar wave-equation for a string in to a Schrodinger-like form. You must have seen a wave-equation for a string that looks like $$\partial_t^2 h-c^2\partial_x^2 h=0,$$ where $h(x,t)$ is the vertical displacement of the string. This wave-equation is second order in time. Let's try to make it first order like the Schrodinger equation by defining $h_1(x,t)=c^{-1}\int_{-\inf}^x dx_1 \partial_t h(x_1,t)$. After doing this we see that our wave-equation turns into a pair of equations that are linear order in time:
$$\partial_t h = c\partial_x h_1$$ and 
$$\partial_t h_1=-c\partial_x h.$$

We can turn this into the Schrodinger equation if we define: $$\Psi(x,t)=\left(\begin{array}{c}h(x,t)\\h_1(x,t)\end{array}\right)\quad H=c\left(\begin{array}{cc}0& i\\-i & 0\end{array}\right)\partial_x.$$ Now those of you who know basic quantum mechanics might say this is a very strange Schrodinger equation. But this indeed is the wave-function for helical Majorana particles that we will encounter later on.

### Schrodinger equation and wave-functions
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

In fact, the good news for those of you familiar with linear algebra is that most of what we talk about is ultimately linear algebra. To model materials, We will often consider electrons within the so-called **tight-binding** approximation where electrons are assumed to occupy a discrete set of orbitals on atoms. We will then take $\psi_a$ to denote the wave-function amplitude of the electron on orbital $a$. We then consider $\psi_a$ to be the components of the wave-function $\psi$, which then becomes a vector. In this linear algebra analogy the Hamiltonian $H$ is seen as a matrix with components $H_{ab}$. With these definitions, the time-independent Schrodinger equation from the last paragraph really becomes an eigenvalue problem. Once we know how to set-up the matrix $H_{ab}$ to model a particular material, we can extract the properties of the material from the wave-function components $\psi_a$ and energy (eigenvalue) $E$. 
> A few key properties of the Schrodinger equation $H\psi^{(n)}=E^{(n)}\psi^{(n)}$ are: (a) if $H$ is an $N\times N$ matrix, the eigenvalue index $n$ goes from $n=1,\dots,N$. (b) $H$ is **Hermitean** i.e. $H_{ab}=H_{ba}^*$. (c) Eigenstates are **orthogonal** i.e. $\psi^\dagger_n \psi_m=0$ for $m\neq n$.


Physicists have a funny but convenient notation for doing linear algebra called the Dirac **bra-ket** notation. In this notation, wave-functions such as $\psi$ are represented by **kets** i.e. $\psi\rightarrow |\psi\rangle$. We construct The "ket" $|\psi\rangle$ from the components of the wave-function $\psi_a$ using the equation: $$|\psi\rangle=\sum_a \psi_a |a\rangle.$$
Similarly, we turn the Hamiltonian $H$ in to  an **operator** using the equation :$$H=\sum_{ab}H_{ab}|a\rangle \langle b|,$$
where $H_{ab}$ are the elements of the matrix $H$ from the last paragraph. The object $\langle b|$ is called a **bra** and together with the ket it forms a "bra-ket" with the property $\langle b| a\rangle=\delta_{ab}$. The Schrodinger equation now looks like $$H|\psi\rangle = E|\psi\rangle,$$
which can be checked to be the same equation as the linear algebra form. 

### Example: Atomic triangle
Let's now work out the simple example of electrons moving in a triangle of atoms, where each atom is assumed to have one orbital. We label the orbitals on the atoms as $|0\rangle,|1\rangle,|2\rangle$. With this labeling, the **hopping** amplitude $t$ of electrons between orbitals is represented by the Hamiltonian $$H=-t(|0\rangle \langle 1|+|1\rangle \langle 2|+|2\rangle \langle 0|)+h.c,$$
where $h.c.$ stands for Hermitean conjugate, which means that you reverse the ordering of the labels and take a complex conjugate. We can also write the Hamiltonian in matrix form $$H_{ab}=-\left(\begin{array}{ccc}0&t&t^*\\t^*&0&t\\t&t^*&0\end{array}\right).$$
You can dump this matrix into Mathematica and it will give you three eigenvectors $\psi^{(n=1,2,3)}_a$ with energy eigenvalues $E^{(n=1,2,3)}=-2 |t| \cos{\theta},|t|\cos{\theta}\pm |t|\sqrt{3}\sin{\theta}$ (where $t=|t|e^{i\theta}$). The corresponding eigenvectors $\psi^{(n=1,2,3)}_a$ are $(1,1,1),(1,\omega,\omega^2),(1,\omega^2,\omega)$ where $\omega$ is the cube-root of unity (i.e. $\omega^3=1$).

## Bloch's theorem for bulk electrons

Actually, we didn't really need Mathematica to solve the problem of an electron in a triangle. We can even solve an N site ring (triangle being $N=3$). The trick is a neat theorem called Bloch's theorem. To understand this model in the context of the tight-binding approximation, let us consider electrons in a crystal. The defining property of a crystal is that the atomic positions repeat in a periodic manner in space. We can account for ALL the atoms in the crystal by first identifying a group of orbitals labelled by $l$ called the **unit-cell**. We construct the crystal by translating the unit cell by a discrete set of vectors called lattice vectors to $n$. By combining the unit cell and the lattice vectors, we can construct positions $a=(l,n)$ 
of all the orbitals in the crystal. For our example of a atomic ring, $l$ wouldn't be needed and $n$ would take values $1$ to $N$. In a three-dimensional crystal, $n=(n_x,n_y,n_z)$ would be a vector of integers. 

The Hamiltonian for a crystal has matrix elements that satisfy $H_{(l,n),(l',m)}=H_{(l,n-m),(l',0)}$ for all pairs of unit-cell $n$ and $m$. 
> Bloch's theorem states that the Schrodinger equation for such Hamiltonians in crystals can be solved by the ansatz: $$\psi_{(l,n)}=e^{i k n}u_l,$$

where $u_l$ is the periodic part of the Bloch function which is identical in each unit-cell. The parameter $k$ is called crystal momentum and is quite analogous to momentum 
except that it is confined in the range $k\in [-\pi,\pi]$ which is referred to as the **Brillouin Zone**.
You can now substitute this ansatz into the Schrodinger equation: $\sum_{l'm}H_{(l,n),(l',m)}u_{l'}e^{i k m}=E_k e^{i k n}u_{l}$. 
>  Thus the Bloch functions $u_l^{(k)}$ and energies $E^{(k)}$ are obtained from the eigenvalue equation (so-called Bloch equation) $$H^{(k)Bloch}u^{(k)}=E^{(k)}u^{(k)},$$

where $$H^{(k)Bloch}_{ll'}=\sum_{m}H_{(l,-m),(l',0)}e^{-i k m}.$$
The Bloch equation written above is an eigenvalue problem at any momentum $k$. The resulting eigenvalues $E^{(n,k)}$ consitute the bandstructure of a material, where the eigenvalue label $n$ is also called a band index. 

### Example: Su-Schrieffer-Heeger model

Let us now work through an example. The Su-Schrieffer-Heeger (SSH) model is the simplest model for polyacetylene, which to a physicist can be thought of as a chain of atoms with one orbital per atom. However, the hopping strength alternates (corresponding to the alternating bond-length ) between $t_1$ and $t_2$. Ususally you could assume that since each orbital has one atom there is only one atom per unit cell. But this would mean all the atoms are identical. On the other hand, in polyacetylene, half the atoms are on the right end of a short bond and half of them are on the left. 
> Thus there are two kinds of atoms - the former kind we label $R$ and the latter $L$. Thus there are two orbitals per unit cell that we label $|L,n\rangle$ and $|R,n\rangle$ with $n$ being the unit-cell label.

![](figures/Trans-_CH_n.svg)

The Hamiltonian for the SSH model is $H=\sum_n \{t_1(|L,n\rangle\langle R,n|+|R,n\rangle\langle L,n|)+t_2(|L,n\rangle\langle R,n-1|+|R,n-1\rangle\langle L,n|)\}.$ This Hamiltonian is clearly periodic with shift of $n$ and the non-zero matrix elements of the Hamiltonian can be written as $H_{(L,0),(R,0)}=H_{(R,0),(L,0)}=t_1$ and $H_{(L,1),(R,0)}=H_{(R,-1),(L,0)}=t_2$. 
>The $2\times 2$ Bloch Hamiltonian is calculated to be: $$H^{(k,Bloch)}_{ll'=1,2}=\left(\begin{array}{cc}0& t_1+t_2 e^{i k}\\t_1+t_2 e^{-ik}&0\end{array}\right).$$

We can calculate the eigenvalues of this Hamiltonian by taking determinants and we find that the eigenvalues are $E^{(k,\pm)}=\pm \sqrt{t_1^2+t_2^2+2 t_1 t_2\cos{k}}.$ Since $L$ and $R$ on a given unit-cell surrounded one of the shorter bonds (i.e. with larger hopping ) we expect $t_1>t_2$. As $k$ varies across $[-\pi,\pi]$, E^{(k,+)} goes from $t_1-t_2$ to $t_1+t_2$. Note that the other energy eigenvalue is just the negative $E^{k,-}=-E^{(+,k)}$. 
> As $k$ varies no energy eigenvalue $E^{k,\pm}$ ever enters the range $-(t_1-t_2)$ to $t_1-t_2$. This range is called an **band gap**, which is the first seminal prediction of Bloch theory that explains insulators.

Let's see what this band structure looks like (**once again move the slider** to change $\mu$):


```python
mus = np.arange(-3, 3, 0.25)

plots = {(t1-t2, Dirac_cone): bandstructure(mu, Dirac_cone=Dirac_cone) 
         for mu in mus 
         for Dirac_cone in ["Show", "Hide"]}

holoviews.HoloMap(plots, kdims=[dims.mu_t, "Dirac cone"])
```

This notion of an insulator will be rather important in our course. So let us dewell on this a bit further. Assuming we have a periodic ring with $2N$ atoms so that $n$ takes $N$ values, single valuedness of the wave-function $\psi_{(l,n)}$ requires that $e^{i k N}=1$. This means that $k$ is allowed $N$ discrete values separated by $2\pi/N$ spanning the range $[-\pi,\pi]$. Next to describe the lower-energy state of the electrons we can fill only the lower eigenvalue $E^{(k,-)}$ with ane electron at each $k$ leaving the upper state empty. This describes a state with $N$ electrons. Furthermore, we can see that to excite the system one would need to transfer an electron from a negative energy state to a positive energy state that would cost at least $2(t_1-t_2)$ in energy. 
> Such a gapped state with a fixed number of electrons cannot respond to an applied voltage and as such must be an insulator. 

This insulator is rather easy to understand in the $t_2=0$ limit and corresponds to the double bonds in the polyacetylene chain being occupied by localized electrons. 

## $k\cdot p$ perturbation theory

Let us now think about how we can use the smoothness of $H^{k,Bloch}$ to predict energies and wave-functions at finite $k$ from $H^{k=0,Bloch}$ and its derivatives. We start by expanding the Bloch Hamiltonian $$H^{(k,Bloch)}=H^{(k=0,Bloch)}+k H^{'(k=0,Bloch)}+(k^2/2)H^{''(k=0,Bloch)}$$. Using standard perturbation theory 
>  we can conclude that the velocity and mass of a non-degenerate band near $k\sim 0$ is written as $v_n = u^{(n)\dagger} H^{'(k=0,Bloch)} u^{(n)}$ and $m_n^{-1}=u^{(n)\dagger} H^{''(k=0,Bloch)} u^{(n)}+\sum_{m\neq n}\frac{|u^{(n)\dagger} H^{'(k=0,Bloch)} u^{(m)}|^2}{E^{(k=0,n)}-E^{(k=0,m)}}$,

where $E^{(k=0,n)}$ and $u^{(n)}$ are energy eigenvalues and eigenfunctions of $H^{(k=0,Bloch)}$. One of the immediate consequences of this is that the effective mass $m_n $ vanishes as the energy denominator $E^{(k=0,n)}-E^{(k=0,m)}$ (i.e. gap ) becomes small. This can be checked to be the case by expanding $E^{(k,-)}\simeq -(t_1-t_2)+\frac{t_2^2}{(t_1-t_2)}k^2$. 

### Discretizing continuum models for materials
The series expansion of $H^{(k,Bloch)}$ that we discussed in the previous paragraph is often thought of as a continuum description of a material. This is because the series expansion is valid for small $k$ that is much smaller than the Brillouin zone. The continuum Hamiltonian is obtained by replacing $k$ in the series expasion by $\hbar^{-1}p$, where $p=-i\hbar\partial_x$ is the momentum operator. 

A continuum Hamiltonian is sometimes easier to work with analytically then the crystal lattice of orbitals. On the other hand, we need to discretize the continuum Hamiltonian to simulate it numerically. We can do this representing $k$ as a discrete derivative operator: $$k=-i\partial_x\approx -i\sum_n (|n+1\rangle\langle n|-|n\rangle\langle n+1|)$$. The label $n$ is discrete - analogous to the unit-cell label. In addition, we need to represent the $N\times N$ matrix structure of $H^{(k=0,Bloch)}$. This is done by introducing label $a=1,\dots N$ so that the Hamiltonian is defined on a space labeled by $|a,n\rangle$. Applying these steps to the Hamiltonian within the $k\cdot p$ approximation takes the discrete form:
$$H^{(k,Bloch)}\approx \sum_{n,a,b} (H^{(k=0,Bloch)}_{ab}|n,a\rangle \langle n,b| +i H^{'(k=0,Bloch)}_{ab}(|n+1, a\rangle\langle n,b|-|n,a\rangle\langle n+1,b|),$$
where we have dropped the $k^2$ term for compactness. Just in case you needed it in the future $k^2$ would discretize into $k^2=-\sum_n (|n\rangle \langle n+2|+|n+2\rangle\langle n|-2|n\rangle \langle n|)$.

But wait! Didn't we just go in a circle by starting in a lattice Hamiltonian and coming back to a discrete Hamiltonian? Well, actually, the lattice in the discretized model from the last paragraph has almost nothing to do with the microscopic lattice we started with. More often then not, the lattice constant (i.e. effective size of the unit-cell) in the latter representation is orders of magnitude larger than the microscopic lattice constant. So, the discrete model following from $k\cdot p$ is orders of more efficient to work with than tht microscopic model, which is why we will most often work with these. Of course, there is always a danger of missing certain lattice level phenomena in such a coarse-grained model. Practically, we will often not even bother with the microscopic lattice model, but rather start with a continuum $k\cdot p$ model and then discretize it. This is because, the latter models can often be constrained quite well by a combination symmetry arguments as well as experimental measurements.