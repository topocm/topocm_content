export async function render({ model, el }) {
  await window.MathJax.startup.promise;
  const figure = model.get('figure');
  const plot = document.createElement('div');
  el.append(plot);
  await window.Plotly.newPlot(plot, figure.data, figure.layout,
    { ...figure.config, responsive: true });
  if (figure.frames?.length) await window.Plotly.addFrames(plot, figure.frames);

  // MyST widgets use a shadow root; Plotly installs its CSS in document.head.
  // Copy its generated rules (including modebar rules) into this widget.
  const style = document.createElement('style');
  style.textContent = [...document.querySelectorAll('style[id^="plotly.js-style"]')]
    .flatMap(sheet => [...sheet.sheet.cssRules].map(rule => rule.cssText)).join('\n');
  el.prepend(style);
  const resize = new ResizeObserver(() => window.Plotly.Plots.resize(plot));
  resize.observe(el);
  return () => {
    resize.disconnect();
    window.Plotly.purge(plot);
    el.replaceChildren();
  };
}

export default { render };
