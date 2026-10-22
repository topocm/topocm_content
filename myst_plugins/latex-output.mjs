// Use MyST's native math renderer for standalone notebook LaTeX (e.g. matrices).
// The stable theme otherwise creates a separate MathJax loader for every output,
// racing Plotly's use of the shared MathJax instance. Notebook downloads keep
// their original MIME bundles; this only changes the rendered document tree.
export function nativeLatex(tree) {
  if (!tree.children) return tree;
  tree.children = tree.children.map((node) => {
    const data = node.type === 'output' && node.jupyter_data?.data;
    if (data && Object.keys(data).every((key) => ['text/latex', 'text/plain'].includes(key))) {
      const latex = data['text/latex'];
      if (typeof latex === 'string' || Array.isArray(latex)) {
        let value = (Array.isArray(latex) ? latex.join('') : latex).trim();
        if (value.startsWith('$$') && value.endsWith('$$')) value = value.slice(2, -2);
        else if (value.startsWith('\\[') && value.endsWith('\\]')) value = value.slice(2, -2);
        else if (value.startsWith('$') && value.endsWith('$')) value = value.slice(1, -1);
        return { type: 'math', value, key: node.key };
      }
    }
    return nativeLatex(node);
  });
  return tree;
}

export default {
  name: 'Native notebook LaTeX outputs',
  transforms: [{ name: 'native-latex', stage: 'document', plugin: () => nativeLatex }],
};
