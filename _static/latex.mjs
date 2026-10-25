export async function render({ model, el }) {
  await window.MathJax.startup.promise;
  const math = await window.MathJax.tex2svgPromise(model.get('latex'), { display: true });
  el.replaceChildren(math);
  return () => el.replaceChildren();
}

export default { render };
