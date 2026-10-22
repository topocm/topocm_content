import assert from 'node:assert/strict';
import test from 'node:test';
import plugin from '../myst_plugins/quizzes.mjs';

const [single, multi] = plugin.directives;
const data = { arg: 'Which state?', body: '- First\n- Second\n- Third', options: { correct: 1, explanation: 'The gap closes.' } };

test('directives preserve course questions, answers and explanations as widget state', () => {
  const [node] = single.run(data);
  assert.equal(node.type, 'anywidget');
  assert.deepEqual(node.model, {
    question: 'Which state?', answers: ['First', 'Second', 'Third'],
    correctIndices: [1], explanation: 'The gap closes.', kind: 'multiple-choice',
  });
  assert.equal(node.esm, '/_static/quiz.mjs');
  assert.equal(node.css, '/_static/quiz.css');
  assert.notEqual(node.id, single.run(data)[0].id);
});

test('checkbox indices are unique and remain zero-based', () => {
  const [node] = multi.run({ ...data, options: { correct: '[2, 0, 2]' } });
  assert.deepEqual(node.model.correctIndices, [0, 2]);
  assert.equal(node.model.kind, 'checkboxes');
});

test('invalid answer indices fail the build rather than silently misgrading', () => {
  for (const correct of [-1, 3, 0.5, NaN, undefined]) {
    assert.throws(() => single.run({ ...data, options: { correct } }));
  }
  for (const correct of ['', '-1', '3', '0.5', 'no', undefined]) {
    assert.throws(() => multi.run({ ...data, options: { correct } }));
  }
});
