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
$$i\partial_t \Psi = H\Psi,$$
where at this point $\Psi$ is the "wave-function" and $H$ is the Hamiltonian. 

Just to give you a sense of what a Schrodinger equation might look like let us convert a familiar wave-equation for a string to a Schrodinger-like form. You must have seen a wave-equation for a string that looks like $$\partial_t^2 h-c^2\partial_x^2 h=0,$$ where $h(x,t)$ is the vertical displacement of the string. This wave-equation is second order in time. Let's try to make it first order like the Schrodinger equation by defining $h_1(x,t)=c^{-1}\int_{-\inf}^x dx_1 \partial_t h(x_1,t)$. After doing this we see that our wave-equation turns into a pair of equations that are linear order in time:
$$\partial_t h = c\partial_x h_1$$ and 
$$\partial_t h_1=-c\partial_x h.$$

We can turn this into the Schrodinger equation if we define: $$\Psi(x,t)=\left(\begin{array}{c}h(x,t)\\h_1(x,t)\end{array}\right)\quad H=c\left(\begin{array}{cc}0& i\\-i & 0h_1(x,t)\end{array}\right)\partial_x.$$ Now those of you who know basic quantum mechanics might say this is a very strange Schrodinger equation. But this indeed is the wave-function for helical Majorana particles that we will encounter later on.


<!-- YOUR TEXT GOES HERE -->