# Topics for self-study

## Simulations: Disorder, butterflies, and honeycombs

There are really plenty of things that one can study with the quantum Hall effect and pumps. Remember, that you don't need to do everything at once (but of course all of the simulations are quite fun!)

### Pumping with disorder

Grab the simulations of the Thouless pump, and see what happens to the pump when you add disorder. Try both the winding in a pump with reservoirs attached, and the spectrum of a closed pump. Can you explain what you observe?

### Butterfly

Take a look at how we calculate numerically the spectrum of Landau levels in the Laughlin argument chapter.
We were always careful to only take weak fields so that the flux per unit cell of the tight binding lattice is small.
This is done to avoid certain [notorious insects](https://en.wikipedia.org/wiki/Hofstadter%27s_butterfly), but nothing should prevent you from cranking up the magnetic field and seeing this beautiful phenomenon.

Plot the spectrum of a quantum Hall layer rolled into a cylinder at a fixed momentum as a function of $B$ as $B$ goes to one flux quantum per unit cell, so in lattice units $B = 2\pi$. Bonus (requires more work): attach a lead to the cylinder, calculate pumping, and color the butterfly according to the pumped charge.

### Graphene

Take a look at how to implement a honeycomb lattice in Kwant [tutorials](https://kwant-project.org/doc/1.0/tutorial/tutorial4), and modify the Hall bar from the Laughlin argument notebook to be made of graphene. Observe the famous [unconventional quantum Hall effect](https://arxiv.org/abs/cond-mat/0602565).

Bonus: See what happens to the edge states as you introduce a constriction in the middle of the Hall bar. This is an extremely useful experimental tool used in making quantum Hall interferometers (also check out the density of states using the code from the edge states notebook).

+++

**Now share your results:**

+++

## Review assignment

For the third week we have these papers:

### @10.48550/arXiv.1109.5983

**Hint:** Topological pumping can be used to characterize quasicrystals too!
Whether this is really unique to quasicrystals is debated though @10.48550/arXiv.1307.2577.

### @10.48550/arXiv.cond-mat/0602645

**Hint:** Quantum Hall effect applies beyond parabolic dispersions with interesting twists.
Figure out what different features arise from other cases.

### @10.48550/arXiv.1201.4167

**Hint:** An experiment detecting the interesting consequences of coexistence of quantum Hall and ferromagnetism in graphene.

### @10.48550/arXiv.0710.2806

**Hint:** Aharonov-Bohm interference using quantum hall edge quasiparticles.

### Bonus: Find your own paper to review!

Do you know of another paper that fits into the topics of this week, and you think is good?
Then you can get bonus points by reviewing that paper instead!
