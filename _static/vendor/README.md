# Vendored Plotly browser bundle

`plotly-4.2.0.min.js` is the unmodified Plotly.js 4.2.0 full browser bundle:
https://cdn.jsdelivr.net/npm/plotly.js-dist-min@4.2.0/plotly.min.js

SHA-256: `fde93964a7511bfa54c5745c49b5d0e41715cbde0cc5ebeae3f9a02de0396cae`

The accompanying MIT license comes from:
https://cdn.jsdelivr.net/npm/plotly.js@4.2.0/LICENSE

To update, replace the bundle and license, update `PLOTLY_BUNDLE` in
`scripts/postprocess_html.py`, and verify plots with MathJax labels and frames.
The postprocessor copies these assets explicitly because their runtime URLs
are not discoverable by MyST's asset collector.
