---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Topics for self-study

```{code-cell} ipython3
:tags: [remove-cell]

from course.init_course import init_notebook

init_notebook()
```

## Simulations: what about other symmetries

So you've made it through the content of the first week. Congratulations!

Now let's get our hands dirty.

+++

### First task: combination of particle-hole and time-reversal symmetries

Look at the notebook about topology of zero-dimensional systems, and see how we generate Hamiltonians with a spinful time-reversal symmetry

$$
H = \sigma_y H^* \sigma_y.
$$

Now try to add this time reversal symmetry to a Hamiltonian which also has particle-hole symmetry. It is easiest to do in the basis where particle-hole symmetry has the form $H = -H^*$.
What do you think will happen? What will the extra symmetry do to the topological invariant?
Test your guess by plotting the spectrum and calculating the Pfaffian invariant.

+++

### Second task: Su-Schrieffer-Heeger (SSH) model

Similar to the Kitaev chain, the SSH model is simple a one-dimensional model where you can see all the essential aspects of topological systems. Unlike the Kitaev chain it does correspond to a physical system: electrons in a polyacetylene chain.

Here's such a chain:

![](figures/polyacetylene.png)

Due to the dimerization of the chain the unit cell has two atoms and the hoppings have alternating strengths $t_1$ and $t_2$, so that the Hamiltonian is

$$
H = \sum_{n=1}^N t_1 \left|2n-1\right\rangle\left\langle 2n\right|+t_2 \left|2n\right\rangle \left\langle 2n+1\right| + \textrm{h.c}
$$

We can choose to start a unit cell from an even-numbered site, so $t_1$ becomes intra-cell hopping and $t_2$ inter-cell hopping.

+++

Now get the notebook with the Kitaev chain and transform a Kitaev chain into an SSH chain.

Now repeat the calculations we've done with Majoranas using SSH chain. Keep $t_1 = 1$ and vary $t_2$.
You should see something very similar to what you saw with the Kitaev chain.

As you can guess, this is because the chain is topological.
Think for a moment: what kind of symmetry protects the states at the edges of the chain.
*(Hint: you did encounter this symmetry in our course.)*

The particle-hole symmetry, is a consequence of a mathematical transformation, and cannot be broken.
The symmetry protecting the SSH chain, however, can be broken.
Test your guess about the protecting symmetry by adding to your chain a term which breaks this symmetry and checking what it does to the spectrum of a finite chain and to its dispersion (especially as chain goes through a phase transition).

+++

**Now share your results:**

+++

## Review assignment

For the first week we have these papers:

### @10.48550/arXiv.1103.0780

**Hint:** Topological classification is not always applied to Hamiltonians.
Figure out what is the topological quantity in open systems.
See this idea also applied in @10.48550/arXiv.1405.6896.

### @10.48550/arXiv.1305.2924

**Hint:** This is a study of statistical properties of topological transitions.

### @10.48550/arXiv.1111.6600

**Hint:** A toy model may still be useful in practice.

+++

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!
