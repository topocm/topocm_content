import assert from 'node:assert/strict';
import test from 'node:test';
import { currentPlotly } from '../myst_plugins/plotly.mjs';

test('plot widgets preserve traces, layouts, frames and configuration', () => {
  const figure = { data: [{ x: [1, 2], y: [3, 4], name: '</script>' }],
    layout: { sliders: [{ active: 2 }] }, frames: [{ name: 'next', data: [] }],
    config: { displayModeBar: false } };
  const output = { type: 'output', jupyter_data: {
    data: { 'application/vnd.plotly.v1+json': figure },
  } };
  const tree = { children: [output] };
  const widget = currentPlotly(tree).children[0];
  assert.equal(widget.type, 'anywidget');
  assert.deepEqual(widget.model.figure, figure);
  assert.equal(output.jupyter_data.data['application/vnd.plotly.v1+json'], figure);
});
