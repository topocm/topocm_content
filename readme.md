# The source materials for the EdX course "Topology in Condensed Matter: Tying Quantum Knots"

The latest stable version of the course is located at http://topocondmat.org.  

Open these notebooks in [Binder](http://mybinder.org/): [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/topocm/topocm_content) such that you can experiment with the code.

## Development tip: shallow clone

Initially, this repository contained all the output of all computations, which means that its size is somewhat big (~300MB). In order to not download all the data, you can use the [shallow cloning](https://www.perforce.com/blog/141218/git-beyond-basics-using-shallow-clones) feature of git (at least v1.9) by using these or analogous commands:

```bash
mkdir topocm && cd topocm
git init
git remote add origin https://github.com/topocm/topocm_content.git # (Or the location of your fork)
git fetch --depth 1 origin +refs/tags/cleaned # Here we get the first commit that doesn't contain cruft
git fetch origin
git checkout master
```

The `cleaned` tag corresponds to the beginning of development that stores no output.
Then you get a repository that does not contain any cruft data, and has a size of ~15MB.

# [Topocondmat.org](http://topocondmat.org/)
The notebooks in this repo are executed and converted to html and available on [topocondmat.org](http://topocondmat.org/).
For building the website we use the [pelican](https://github.com/getpelican/pelican) static site generator, available under AGPL license.
