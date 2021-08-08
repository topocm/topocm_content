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

# Topics for self-study

```{code-cell} ipython3
:tags: [remove-cell]

import sys

sys.path.append("../code")
from init_course import *

init_notebook()
```

## Simulations

### 1D localization

Our aim now is to verify that Anderson localization works in one-dimensional systems.

Simulate the Anderson model of a ribbon of appropriate and large width $W$  as a function of length $L$.

Anderson model is just the simpest [tight binding model on a square lattice](https://kwant-project.org/doc/1.0/tutorial/tutorial1) with random onsite potential.

Tune your model in the clean limit such that it has a relatively large number of modes (at least 3). Then calculate conductance as a function of $L$ at a finite disorder, while keeping $W$ constant.

The weak disorder regime should look ohmic or classical i.e $g \sim N_{ch}\lambda_{MFP}/L$. Here $\lambda_{MFP}$ is the mean free path, and $N_{ch}$ is the number of channels.

First, verify that when $g \gtrsim 1$ you observe the classical behavior and evaluate the mean free path.

Verify that the scaling also holds for different disorder strengths and different widths.

Examine the plot for larger $L$, but this time plot $\textrm{ln}(g)$ to verify that at large $L$ the conductance $g$ goes as $g \sim \exp(-L/\xi)$. Try to guess how $\xi$ is related to $\lambda_{MFP}$ by comparing the numbers you get from the plot in this part and the previous.

Check what happens when you reduce the disorder? Is there sign of a insulator- metal transition at lower disorder?

### Griffiths phase

A disordered Kitaev chain has a peculiar property. Close to the transition point it can have infinite density of states even despite it is insulating.

Calculate the energies of all the states in a finite Kitaev chain with disorder. You'll need to get the Hamiltonian of the chain by using `syst.hamiltonian_submatrix` method, and diagonalize it (check the very beginning of the course if you don't remember how to diagonalize matrices).

Do so for many disorder realizations, and build a histograph of the density of states for different values of average $m$ and of disorder strengh around the critical point $m=0$.

If all goes well, you should observe different behaviors: the density of states in a finite region around $m=0$ has a weak power law divergence, that eventually turns into an actual gap. Check out this paper for details:

* arXiv:cond-mat/0011200

+++

**Now share your results:**

+++

## Review assignment

### arXiv:0908.0881

**Hint:** The topological Anderson insulator.

### arXiv:0705.0886

**Hint:** One-parameter scaling in graphene.

### arXiv:0705.1607

**Hint:** Scaling with Dirac fermions.

### arXiv:1208.3442

**Hint:** The average symmetry and weak transitions.

### arXiv:1411.5992

**Hint:** A technical paper about localization in 1D, but you don't need to follow the calculations.

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!

+++
