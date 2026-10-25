export async function render({ model, el }) {
  await window.MathJax.startup.promise;
  const math = await window.MathJax.tex2svgPromise(model.get('latex'), { display: true });
  // MathJax installs its display spacing and SVG rules in document.head;
  // MyST's widget shadow root needs its own copy.
  const doc = window.MathJax.startup.document;
  const style = doc.outputJax.styleSheet(doc).cloneNode(true);
  el.replaceChildren(style, math);
  return () => el.replaceChildren();
}

export default { render };
