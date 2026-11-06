import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { test } from 'node:test';

const loader = await readFile(new URL('../_static/libraries.js', import.meta.url), 'utf8');
const source = (await readFile(new URL('../_static/plotly.mjs', import.meta.url), 'utf8'))
  .replace('export default { render };', '').replaceAll('export ', '');

function fixture() {
  const scripts = [];
  const window = { coursePlotlyUrl: '/preview/_static/vendor/plotly-4.2.0.min.js' };
  const context = vm.createContext({ window, document: {
    createElement: () => ({ remove() {} }),
    head: { append: script => scripts.push(script) },
  }, setTimeout, clearTimeout, console: { error() {} } });
  vm.runInContext(loader + source, context);
  return { context, window, scripts, load: () => window.loadCoursePlotly() };
}

test('concurrent widgets share one load and wait for MathJax startup before Plotly', async () => {
  const f = fixture();
  const first = f.load();
  assert.equal(f.load(), first);
  assert.equal(f.scripts.length, 1);
  let ready;
  f.window.MathJax.startup.promise = new Promise(resolve => { ready = resolve; });
  f.scripts[0].onload();
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(f.scripts.length, 1);
  ready();
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(f.scripts[1].src, '/preview/_static/vendor/plotly-4.2.0.min.js');
  assert.equal(f.scripts[1].async, true);
  f.scripts[1].onload();
  await first;
  assert.equal(f.load(), first); // Includes subsequent client-side navigation.
});

test('load failure shows a local error instead of calling Plotly', async () => {
  const f = fixture();
  const el = { setAttribute(name, value) { this[name] = value; } };
  f.context.el = el;
  const rendered = vm.runInContext('render({el})', f.context);
  f.scripts[0].onerror();
  await rendered;
  assert.match(el.textContent, /could not load/);
  assert.equal(el.role, 'alert');
});


test('MathJax-only widgets do not load Plotly', async () => {
  const f = fixture();
  const ready = f.window.loadCourseMathJax();
  assert.equal(f.scripts.length, 1);
  f.window.MathJax.startup.promise = Promise.resolve();
  f.scripts[0].onload();
  await ready;
  assert.equal(f.scripts.length, 1);
  assert.equal(f.window.loadCourseMathJax(), ready);
});
