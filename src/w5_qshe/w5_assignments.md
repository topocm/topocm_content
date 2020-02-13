```python
import sys
sys.path.append('../../code')
from init_mooc_nb import *
init_notebook()
```

# Simulations

As usual, start by grabbing the notebooks of this week (`w5_qshe`). They are once again over [here](http://tiny.cc/topocm_smc).

### Kane-Mele model

The first known implementation of quantum spin Hall effect is the Kane-Mele model, introduced in [this paper](http://arxiv.org/abs/cond-mat/0411737). It is a doubled copy of the Haldane model (get that one from the previous week's notebooks), with spin up and spin down having next-nearest neighbor hoppings complex conjugate of each other due to spin-orbit coupling.

Implement the Kane-Mele model and add a staggered onsite potential to also be able to create a trivial gap. Calculate the scattering matrix topological invariant of that model.

How would you add disorder and calculate the topological invariant? (Hint: you need to add disorder to the scattering region, and make leads on both sides conducting)

### Quantum Hall regime

The helical edge states of quantum spin Hall effect survive for some time when a magnetic field is added. Make a Hall bar out of the BHZ model. Can you reproduce the experimental results? What do you see? Are the inversion symmetry breaking terms important?

What about conductance in a two terminal geometry: can you see the crossover from quantum spin Hall regime to quantum Hall regime?


```python
MoocSelfAssessment()
```

**Now share your results:**


```python
MoocDiscussion('Labs', 'Quantum spin Hall effect')
```

# Review assignment

### arXiv:1306.1925

**Hint:** A better material?

### arXiv:0808.1723

**Hint:** What happens when edge states meet.

### arXiv:1104.3282

**Hint:** A completely different approach.

### arXiv:1312.2559

**Hint:** Adding superconductors.

### arXiv:1303.1766

**Hint:** Sources of back-scattering in QSHE edge.

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!

```python
MoocSelfAssessment()
```

**Do you have questions about what you read? Would you like to suggest other papers? Tell us:**


```python
MoocDiscussion("Reviews", "Quantum spin Hall effect")
```
