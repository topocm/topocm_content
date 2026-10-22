import assert from 'node:assert/strict';
import test from 'node:test';
import { nativeLatex } from '../myst_plugins/latex-output.mjs';

function output(data) {
  return { type: 'output', key: 'matrix', jupyter_data: { output_type: 'display_data', data }, children: [] };
}

test('standalone notebook math becomes native math without changing its formula', () => {
  const formula = String.raw`\begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}`;
  for (const latex of [formula, `$$${formula}$$`, String.raw`\[${formula}\]`, [formula]]) {
    const tree = { type: 'outputs', children: [output({ 'text/latex': latex, 'text/plain': 'matrix' })] };
    assert.deepEqual(nativeLatex(tree).children, [{ type: 'math', value: formula, key: 'matrix' }]);
  }
});

test('richer output bundles and plain text retain their native renderer', () => {
  for (const data of [
    { 'text/plain': 'plain output' },
    { 'text/latex': '$x$', 'text/html': '<b>richer output</b>' },
    { 'application/vnd.plotly.v1+json': { data: [] } },
  ]) {
    const node = output(data);
    const tree = { type: 'outputs', children: [node] };
    assert.equal(nativeLatex(tree).children[0], node);
    assert.deepEqual(node.jupyter_data.data, data);
  }
});
