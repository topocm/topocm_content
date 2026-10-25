import { randomUUID } from 'node:crypto';

// Bypass the stable theme's Plotly 2 / MathJax 2 renderer. Only the website
// AST changes; downloadable notebooks retain their original Plotly MIME.
export function currentPlotly(tree) {
  if (!tree.children) return tree;
  tree.children = tree.children.map((node) => {
    const figure = node.type === 'output'
      && node.jupyter_data?.data?.['application/vnd.plotly.v1+json'];
    if (figure) return {
      type: 'anywidget', id: randomUUID(), esm: '/_static/plotly.mjs',
      model: { figure },
    };
    return currentPlotly(node);
  });
  return tree;
}

export default {
  name: 'Current Plotly renderer',
  transforms: [{ name: 'current-plotly', stage: 'document', plugin: () => currentPlotly }],
};
