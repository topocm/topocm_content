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
from init_mooc_nb import *

init_notebook()
```

## Simulations: Gaps and invariants

As usual, start by grabbing the notebooks of this week (`w8_general`). They are once again over [here](http://tiny.cc/topocm_smc).

### A different analytic continuation

You have learned how to map a winding number onto counting the zeros of an eigenproblem in a complex plane. This can be applied to other symmetry classes as well.

Let's try to calculate the invariant in the 1D symmetry class DIII. If you look in the table, you'll see it's the same invariant as the scattering invariant we've used for the quantum spin Hall effect,

$$
Q = \frac{\textrm{Pf } h(k=0)}{\textrm{Pf } h(k=\pi)} \sqrt{\frac{\det h(k=\pi)}{\det h(k=0)}}
$$

In [this paper](http://arxiv.org/abs/1106.6351) (around Eq. 4.13), have a look at how to use analytic continuation to calculate the analytic continuation of $\sqrt{h}$, and implement the calculation of this invariant without numerical integration, like we did before.

In order to test your invariant, you'll need a topologically non-trivial system in this symmetry class. You can obtain it by combining a Majorana nanowire with its time-reversed copy.

This is a hard task; if you go for it, try it out, but don't hesitate to ask for help in the discussion below.

### Finding gaps

The analytic continuation from $e^{ik}$ to a complex plane is also useful in telling if a system is gapped.

Using the mapping of a 1D Hamiltonian to the eigenvalue problem, implement a function which checks if there are propagating modes at a given energy.

Then implement an algorithm which uses this check to find the lowest and the highest energy states for a given 1D Hamiltonian $H = h + t e^{ik} + t^\dagger e^{-ik}$ (with $h$, $t$ arbitrary matrices, of course).

+++

**Now share your results:**

+++

## Review assignment

### arXiv:1006.0690

**Hint:** The most general classification.

### arXiv:1310.5281

**Hint:** Beyond classification.

### arXiv:1012.1019

**Hint:** The non-commutative invariants.

### arXiv:1106.6351

**Hint:** All about scattering.

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!

+++
