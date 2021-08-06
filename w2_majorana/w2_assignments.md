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

# Assignments

```{code-cell} ipython3
:tags: [remove-cell]

import sys

sys.path.append("../../code")
from init_course import *

init_notebook()
```

## Simulation: tweaking the nanowire

We have two choices for your coding assignments of this week. Consider the task complete when you finish one of the two.

This is especially true since both of the assignments constitute a complete paper :)

As usual, start by grabbing the notebooks of this week (`w2_majorana`). They are once again over [here](http://tiny.cc/topocm_smc).

### Tilted magnetic field

Explore what happens when we change one the important knobs of the nanowire model, the external magnetic field. We studied what happens when $B$ is pointing along the $z$ direction. However, what happens when the magnetic field is tilted?

Generalize the Hamiltonian of the nanowire to the case of a magnetic field with three components $B_x, B_y, B_z$. How do the new terms look like?

Go into the `nanowire` notebook. Modify the `nanowire_chain` function to include the magnetic field pointing in general direction.
Plot the band structure for different field directions, and compare to the original case of having only $B_z$. What changes?

Compare your results with what you find over here:

* arXiv:1403.4464

### From $4\pi$ to $2\pi$.

Now let's switch to the signatures of Majoranas. The code for these is in the `signatures` notebook.

How does the $4\pi$-periodic Josephson effect disapper? We argued that we cannot just remove a single crossing. Also periodicity isn't a continuous variable and cannot just change. So what is happening?

Study the spectrum of a superconducting ring as a function of magnetic field, as you make a transition between the trivial and the topological regimes.

What do you see? Compare your results with the paper below.

* arXiv:1210.3237

+++

## Review assignment

As we mentioned, there are really hundreds of papers that use the models and concepts that we used in the lecture.

Here is a small selection of the ones that you may find interesting.

### arXiv:1204.2792',

**Hint:** Welcome to the real world.

### arXiv:1101.5795',

**Hint:** Majorana conductance with many modes.

### arXiv:1006.4395',

**Hint:** To play a nice melody, you just need a keyboard.
This paper first showed how Majoranas in wire networks can be moved around

### arXiv:1008.0629

**Hint:** Real nanowires are more complicated.

+++

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!
