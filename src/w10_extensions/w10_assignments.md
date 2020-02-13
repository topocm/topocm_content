```python
import sys
sys.path.append('../../code')
from init_mooc_nb import *
init_notebook()
```

# Simulations

As usual, start by grabbing the notebooks of this week (`w10_extensions`). They are once again over [here](http://tiny.cc/topocm_smc).

## Weyl semimetal with time-reversal symmetry.

Time-reversal symmetry has a very similar effect on Weyl semimetals as it has on gapless superconductors: it keeps the value of the Chern number around the Weyl point the same, and leads to appearance of quadruplets of Weyl points.

Your task is to construct a Weyl semimetal with time reversal symmetry. As we discussed, 4 Weyl points are needed.

If you don't know where to start, here's a hint: you're not the first one who wants to construct a Weyl semimetal with time reversal, search on arxiv.

## Graphene edge states.

Graphene, just like $d$-wave superconductors has edge states. They only exist when the Dirac points are not located at coinciding momenta parallel to the boundary.

Define a graphene ribbon supporting edge states. For that you'll need to figure out which orientation to choose.

Then try to add a term to the boundary that breaks the sublattice symmetry and moves the edge states from zero energy. What happens?

What if you add the next-nearest neighbor hopping in the bulk. What do you see now?

Try to remove the edge states completely by tweaking the sublattice symmetry breaking term at the edge. Did you succeed? How?


```python
MoocSelfAssessment()
```

**Now share your results:**


```python
MoocDiscussion('Labs', 'Extensions')
```

# Review assignment

### arXiv:1504.01350

### arXiv:1503.06808

**Hint:** Different mechanical TI

### arXiv:1309.5846

**Hint:** Weyl + disorder

### arXiv:1410.1320

**Hint:** The best of both worlds

### arXiv:0909.5680

**Hint:** A general approach to gapless superconductors.

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!


```python
MoocSelfAssessment()
```

**Do you have questions about what you read? Would you like to suggest other papers? Tell us:**


```python
MoocDiscussion("Reviews", "Extensions")
```
