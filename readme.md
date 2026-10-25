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

## Building the website

Run `pixi run postprocess-html` to execute notebooks and export `_build/html`.
The task invokes MyST directly because Jupyter Book 2.1.7 does not apply its
`--execute-parallel` option. Set `JUPYTER_NUM_PROCS` to change the default of four
concurrent notebooks. MyST caches notebook execution; changes to the environment
or course helpers invalidate that cache. `BASE_URL=/branch_name` builds a branch
preview, including assets and legacy redirects.

The course retains its `youtube`, `multiple-choice`, and `checkboxes` directives.
Quizzes use MyST widgets because the former fabricated notebook outputs are
incompatible with MyST 1.11. Plot widgets use Plotly.js 4 and MathJax 4 rather than
the stable theme's bundled Plotly 2 renderer. Standalone notebook LaTeX uses native
MyST math, avoiding the theme's competing MathJax 2 loader. Downloadable notebooks
retain their original output data.

Run infrastructure tests with `pixi run python -m unittest discover -s tests` and
`pixi run node --test tests/*.test.mjs`. After changing rendering code, also check
plots, sliders, quizzes, videos, and legacy URLs in a browser, including under a
branch prefix.

Merge requests publish an artifact preview through the environment's **View app**
link, available for one week. `BASE_URL` includes the job's artifact path.
The preview-only `scripts/artifact_preview.py` keeps explicit `index.html` URLs
because the artifact viewer does not serve directory indexes. It patches the
pinned theme's URL helper and fails if that helper changes on a theme upgrade.
Production uses MyST's normal directory URLs.

The main-branch job publishes to the OVH VPS as the restricted `topocondmat`
account, using the existing `WEBSITE_UPLOAD_KEY` and the SSH host key pinned in
`.ci/known_hosts`. The account's rsync root is `/srv/www/topocondmat`.
