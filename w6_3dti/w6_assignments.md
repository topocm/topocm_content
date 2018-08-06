```python
import sys
sys.path.append('../code')
from init_mooc_nb import *
init_notebook()
```

# Simulations: more Chern insulators

As usual, start by grabbing the notebooks of this week (`w6_3dti`). They are once again over [here](http://tiny.cc/topocm_smc).

Simulations of the three-dimensional systems are hard, mostly because they take a lot of computational power. That's why we'll do something relatively simple this time.

### Breaking time-reversal

One mechanism of opening the gap on the surface of a topological insulator is to bring it into contact with a ferromagnet, which creates an effective Zeeman field.

* By calculating dispersion of a slab of 3D TI, observe the effect of Zeeman field pointing in different directions on the surface state dispersion. Find out which direction of the Zeeman field opens the gap in the surface state.
* Make a domain wall between different orientations of Zeeman field. Are there any modes in this domain wall?

### Many invariants

The BHZ model is rather rich and allows to produce every possible topological invariant. Can you find the parameter values that produce all the desired values of the invariants? (Hint: you need to make the model anisotropic). 


```python
MoocSelfAssessment()
```

**Now share your results:**


```python
MoocDiscussion('Labs', '3DTI')
```

# Review assignment


```python
display_html(PreprintReference('1410.0655', description="What enters the measurement of a Dirac point conductance"))
display_html(PreprintReference('0811.1303', description="Consequences of magneto-electric effect"))
display_html(PreprintReference('1401.7461', description="Weak and strong topological insulators with disorder"))
display_html(PreprintReference('1311.1758', description="Topological, but not insulator"))
display_html(PreprintReference('1005.3762', description="Threading flux through a topological insulator"))
```

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!


```python
MoocSelfAssessment()
```

**Do you have questions about what you read? Would you like to suggest other papers? Tell us:**


```python
MoocDiscussion("Reviews", "3DTI")
```
