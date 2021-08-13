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

# About this course

```{code-cell} ipython3
:tags: [remove-cell]

# This cell is present in all the notebooks.
# It makes the necessary packages available and adjusts various settings.
# You should execute this cell at the start.

import sys

sys.path.append("../code")
from init_course import *

init_notebook()

from IPython.display import HTML
```

## A welcome word

Through this course we want to provide an introduction to the topic of topology in condensed matter.
We want it to be accessible and useful to people with different backgrounds and motivations.

We want the course to be useful to you if you are a **master student**, and you want to get an understanding of what topology is all about.

Or you could be a **PhD student or a postdoc** doing experiments, and you want to get a better theoretical grasp of what you should expect in your investigation.

You could even be a **theorist working in topology** and be extremely familiar with topological invariants and vector bundles, but you would like to get a better overview of how the mathematical ideas apply in physical systems.

Finally, we also want this course to be equally useful if you are, say, a **professor working in condensed matter** and you want to apply the ideas introduced by topology in your domain, so that you just need a quick overview of what research activity is there.

We hope that you find something useful, and we always appreciate your questions and feedback via the [course chat](https://chat.quantumtinkerer.tudelft.nl/topocondmat) or the course repository [issue tracker](https://github.com/topocm/topocm_content/issues).
So whenever you see a typo, or you would like to suggest an improvement, you can open an issue, (or even make a pull request right away).

### Course structure

The course is separated into 12 topics, each containing 2–3 lectures on related subjects. 
Each lecture is introduced by an expert in this subject.
We end each topic with suggestions of open-ended questions for self-study: numerical simulations or papers to read and review.

### Prerequisites

#### Background knowledge

While the math that we use only requires linear algebra and calculus, this course is complex.
Topology affects many physical phenomena, and therefore the course will touch a lot of different concepts in condensed matter physics.
In the [next chapter](band_structures) we provide a brief review of band theory—the main physical concept that you will need, however if you don't know condensed matter physics yet, you are likely to struggle.

#### Code

We provide source code for all the computer simulations used in the course as well as suggestions of what you can investigate on your own. In order to use these, you need to be familiar with Python's scipy stack (check e.g. [this course](https://scipy-lectures.org/)), as well as the [`Kwant`](http://kwant-project.org/) quantum transport package. You can run the code right away without installing anything, using the [Binder](https://mybinder.org/) project over here: [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/topocm/topocm_content).

To obtain a local version of the code, clone or download the [course repository](https://github.com/topocm/topocm_content), install the conda environment from `environment.yml`, and open the source files using the [`jupytext`](https://jupytext.readthedocs.io/en/latest/) jupyter extension.

+++

## Literature

We are mostly going to focus on the overall structure of the field and study the most basic and general phenomena. We will also skip detailed derivations or some details.

For a more formal and complete source of information on topological insulators and superconductors we recommend you to look into the reviews below. (Of course we think they will be much easier to follow after you finish the course).

+++

### Topological insulator reviews

* arXiv:0801.0901
* arXiv:1002.3895
* arXiv:1008.2026

### Majorana fermion reviews

* arXiv:1112.1950
* arXiv:1202.1293
* arXiv:1206.1736
* arXiv:1407.2131

### Advanced topics: Fractional particles and topological quantum computation

* arXiv:0707.1889
* arXiv:0711.4697
* arXiv:1404.0897

### Extra topics

* arXiv:1211.5623
* arXiv:1501.00531
