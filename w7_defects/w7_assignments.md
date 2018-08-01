

```python
import sys
sys.path.append('../code')
from init_mooc_nb import *
init_notebook()
```

# Simulations: Majorana defects

As usual, start by grabbing the notebooks of this week (`w7_defects`). They are once again over [here](http://tiny.cc/topocm_smc).

## Quantum spin Hall junction

Let us study the spectrum of a Josephson junction on a quantum spin Hall edge in more detail. As in the lecture, we can add a magnet in the middle of the junction, which adds a Zeeman energy term to the Hamiltonian.

First, make such a junction. The code from week 2 for making a Josephson junction may be useful.

We are interested in the spectrum below the gap. There are two interesting parameters to vary: the Zeeman energy and the length of the junction. What happens to the energy levels as you increase the length of the junction. In particular, what happens when the junction is very long? What if you turn off the magnet?

Compare your results to the following paper, particularly Fig. 2.


```python
display_html(PreprintReference('0804.4469', show_abstract=False))
```

## Majorana in a crystalline defect

Following Taylor Hughes suggestion from the summary of the lecture about crystalline defects, create an edge dislocation carrying a Majorana mode in an array of weakly coupled Kitaev chains.

Then try to split the dislocation into two disclinations. What happens to the Majorana mode?

Note that Kwant only supports regular lattices, so crystallographic defects can be implemented by altering some hoppings, as was done in the simulations in the lecture.


```python
MoocSelfAssessment()
```

**Now share your results:**


```python
MoocDiscussion('Labs', 'Topological defects')
```

# Review assignment


```python
display_html(PreprintReference('0707.1692', description="In detail, how to create and manipulate Majoranas on the 3D TI surface."))
display_html(PreprintReference('1112.3527', description="The Josephson effect on a 3D TI, in real life."))
display_html(PreprintReference('1208.6303', description="Disclinations"))
display_html(PreprintReference('1105.4351', description="How weak is weak?"))
```

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!


```python
MoocPeerAssessment()
```

**Do you have questions about what you read? Would you like to suggest other papers? Tell us:**


```python
MoocDiscussion("Reviews", "Topological defects")
```
