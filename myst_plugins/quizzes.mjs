import { randomUUID } from 'node:crypto';

const sanitizeQuestion = (value) => {
  const question = (value ?? '').trim();
  if (!question) {
    throw new Error('Quiz directives require a question argument.');
  }
  return question;
};

const parseAnswerLines = (body) => {
  if (typeof body !== 'string') return [];
  return body
    .split(/\r?\n/)
    .map((line) => line.trim())
    .map((line) => line.replace(/^[-*]\s+/, '').trim())
    .filter((line) => line.length > 0);
};

const normalizeIndex = (value, answersLength) => {
  if (!Number.isInteger(value)) {
    throw new Error('Correct answer indices must be integers.');
  }
  const idx = value;
  if (idx < 0 || idx >= answersLength) {
    throw new Error(`Correct answer index ${value} is out of range for ${answersLength} answers.`);
  }
  return idx;
};

const parseIndexList = (raw, answersLength) => {
  if (raw === undefined || raw === null) {
    throw new Error('Checkbox quizzes require the :correct: option.');
  }
  const cleaned = String(raw).replace(/[\[\]]/g, ' ');
  const tokens = cleaned
    .split(/[,;\s]+/)
    .map((token) => token.trim())
    .filter((token) => token.length > 0);
  if (tokens.length === 0) {
    throw new Error('Provide at least one correct answer index.');
  }
  const indices = tokens.map((token) => {
    const num = Number(token);
    if (!Number.isFinite(num)) {
      throw new Error(`"${token}" is not a valid number.`);
    }
    return normalizeIndex(num, answersLength);
  });
  return [...new Set(indices)].sort((a, b) => a - b);
};

// MyST owns asset copying and widget mount/unmount, including client navigation.
const emitQuiz = (model) => [{
  type: 'anywidget',
  id: randomUUID(),
  esm: '/_static/quiz.mjs',
  css: '/_static/quiz.css',
  model,
}];

const multipleChoiceDirective = {
  name: 'multiple-choice',
  doc: 'Render a multiple choice quiz with a revealable answer block.',
  arg: { type: String, required: true, doc: 'Question text.' },
  options: {
    correct: {
      type: Number,
      required: true,
      doc: 'Index of the correct answer (0-based by default).',
    },
    explanation: {
      type: String,
      doc: 'Optional explanation shown alongside the answer.',
    },
  },
  body: {
    type: String,
    required: true,
    doc: 'Answer options, one per line (you may prefix each line with a dash for readability).',
  },
  run(data) {
    const question = sanitizeQuestion(data.arg);
    const answers = parseAnswerLines(data.body ?? '');
    if (answers.length < 2) {
      throw new Error('Multiple choice quizzes need at least two answers.');
    }
    const correctRaw = data.options?.correct;
    if (correctRaw === undefined || correctRaw === null) {
      throw new Error('Specify :correct: for multiple-choice quizzes.');
    }
    const correctIdx = normalizeIndex(Number(correctRaw), answers.length);
    const explanation = (data.options?.explanation ?? '').trim();
    return emitQuiz({
      question,
      answers,
      correctIndices: [correctIdx],
      explanation,
      kind: 'multiple-choice',
    });
  },
};

const checkboxDirective = {
  name: 'checkboxes',
  doc: 'Render a checkbox quiz where multiple answers may be correct.',
  arg: { type: String, required: true, doc: 'Question text.' },
  options: {
    correct: {
      type: String,
      required: true,
      doc: 'Comma or space separated list of correct answer indices (0-based by default).',
    },
    explanation: {
      type: String,
      doc: 'Optional explanation shown alongside the answer.',
    },
  },
  body: {
    type: String,
    required: true,
    doc: 'Answer options, one per line (you may prefix each line with a dash for readability).',
  },
  run(data) {
    const question = sanitizeQuestion(data.arg);
    const answers = parseAnswerLines(data.body ?? '');
    if (answers.length < 2) {
      throw new Error('Checkbox quizzes need at least two answers.');
    }
    const correctIndices = parseIndexList(data.options?.correct, answers.length);
    const explanation = (data.options?.explanation ?? '').trim();
    return emitQuiz({
      question,
      answers,
      correctIndices,
      explanation,
      kind: 'checkboxes',
    });
  },
};

const plugin = {
  name: 'Interactive quiz directives',
  directives: [multipleChoiceDirective, checkboxDirective],
};

export default plugin;
