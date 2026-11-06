// Inlined before hydration by postprocess_html.py. No downloads until requested.
(() => {
  let mathJax, plotly;
  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.async = true;
      script.onload = () => resolve();
      script.onerror = () => {
        script.remove();
        reject(new Error(`Could not load ${src}`));
      };
      document.head.append(script);
    });
  }
  // Window-scoped entry points share one instance across all widget modules.
  window.loadCourseMathJax = () => mathJax ??= (async () => {
    window.MathJax = {
      startup: { typeset: false },
      tex: { inlineMath: [['$', '$']] },
      svg: { fontCache: 'local' },
    };
    await loadScript('https://cdn.jsdelivr.net/npm/mathjax@4.1.3/tex-svg.js');
    await window.MathJax.startup.promise;
  })();
  window.loadCoursePlotly = () => plotly ??= (async () => {
    // Plotly detects MathJax during initialization; preserve that ordering.
    await window.loadCourseMathJax();
    await loadScript(window.coursePlotlyUrl);
  })();
})();
