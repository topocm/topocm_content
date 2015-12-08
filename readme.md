# The source materials for the EdX course "Topology in Condensed Matter: Tying Quantum Knots"

The latest stable version of the course is located at http://topocondmat.org.  
We are currently reorganizing and updating the course materials, so that the repository is not functional in its current state.

## Development tip: shallow clone

Initially, this repository contained all the output of all computations, which means that its size is somewhat big (~300MB). In order to not download all the data, you can use the [shallow cloning](https://www.perforce.com/blog/141218/git-beyond-basics-using-shallow-clones) feature of git (at least v1.9) by using these or analogous commands:

```bash
mkdir topocm && cd topocm
git init
git remote add origin https://github.com/topocm/topocm_content.git # (Or the location of your fork)
git fetch --depth 1 origin +refs/tags/cleaned # Here we get the first commit that doesn't contain cruft
git fetch origin
```

The `cleaned` tag corresponds to the beginning of development that stores no output.
Then you get a repository that does not contain any cruft data, and has a size of ~15MB.
