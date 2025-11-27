# The source materials for the EdX course "Topology in Condensed Matter: Tying Quantum Knots"

The latest stable version of the course is located at http://topocondmat.org.

Open these notebooks in [Binder](http://mybinder.org/): [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/topocm/topocm_content) so you can experiment with the code.

## Development tip: shallow clone

Initially, this repository contained the output of all computations, which means that its size is quite large (~300MB). To avoid downloading all the data, you can use the [shallow cloning](https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---depthdepth) feature of git by using these or analogous commands:

```bash
mkdir topocm && cd topocm
git init
git remote add origin https://github.com/topocm/topocm_content.git # (Or the location of your fork)
git fetch --depth 1 origin +refs/tags/cleaned # Here we get the first commit that doesn't contain cruft
git fetch origin
git checkout master
```

The `cleaned` tag marks the start of development that stores no output.
This gives you a repository without cruft data and a size of ~15MB.

## [Topocondmat.org](http://topocondmat.org/)

The files in this repo are executed and converted to HTML and available on [topocondmat.org](http://topocondmat.org/).
For building the website, we use the [Jupyter Book](https://jupyterbook.org/) static site generator, available under the BSD license.
