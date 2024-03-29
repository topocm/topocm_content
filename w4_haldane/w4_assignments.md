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

## Simulations: more Chern insulators

### Yet another Chern insulator

One more tight binding of a Chern insulator that you can encounter in the wild is a regular square lattice with half a flux quantum of magnetic field per unit cell. If you made the Hofstadter butterfly assignment from the previous week, it's just in the middle of the butterfly. Half a flux quantum per unit cell means that the hoppings in one direction are purely imaginary, and different rows have alternating signs

$$
t_y = t,\quad t_x = (-1)^y it.
$$

This model has a dispersion very similar to graphene: it has two Dirac cones without a gap. Like graphene it also has two sites per unit cell, and sublattice symmetry.

Simulate this model. Think which parameters you need to add to it to make it a Chern insulator. Check that the edge states appear, and calculate the Berry curvature.

### Back to the winding

Integration of Berry curvature is just another way to calculate the same quantity: the topological invariant. Verify that the winding of reflection phase gives the same results. To do that, make the pumping geometry out of a Chern insulator rolled into a cylinder, thread flux through it, and check that the topological invariant obtained through Berry curvature integration is the same as that obtained from winding.

We know that Berry curvature is concentrated close to the Dirac points. Do you notice anything similar for the pumped charge?

+++

**Now share your results:**

+++

## Review assignment

### arXiv:1012.4723

**Hint:** The hunt for flat bands.

### arXiv:1409.6715

**Hint:** Making a Chern insulator more like quantum Hall effect.

### arXiv:1208.4579

**Hint:** A Chern insulator without lattice.

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!

+++
