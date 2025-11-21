import { randomBytes } from 'node:crypto';

const uniqueId = () => {
  if (globalThis.crypto?.randomUUID) {
    return globalThis.crypto.randomUUID();
  }
  return `quiz-${Math.random().toString(36).slice(2, 10)}`;
};

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

const parseBase = (value) => {
  if (value === undefined || value === null) return 0;
  const baseNum = Number(value);
  if (baseNum === 0 || baseNum === 1) return baseNum;
  throw new Error('The :base: option must be 0 or 1.');
};

const normalizeIndex = (value, base, answersLength) => {
  if (!Number.isFinite(value)) {
    throw new Error('Correct answer indices must be numbers.');
  }
  const idx = value - base;
  if (idx < 0 || idx >= answersLength) {
    throw new Error(`Correct answer index ${value} is out of range for ${answersLength} answers.`);
  }
  return idx;
};

const parseIndexList = (raw, base, answersLength) => {
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
    return normalizeIndex(num, base, answersLength);
  });
  return [...new Set(indices)].sort((a, b) => a - b);
};

const buildQuizHtml = ({ question, answers, correctIndices, explanation, kind }) => {
  const id = uniqueId();
  const options = answers
    .map((answer, idx) => {
      const isCorrect = correctIndices.includes(idx);
      return `<button type="button" class="quiz-option" data-correct="${isCorrect}" data-role="quiz-option" aria-pressed="false">
        <span data-role="quiz-marker" aria-hidden="true" class="quiz-marker"></span>
        <span class="quiz-answer">${answer}</span>
      </button>`;
    })
    .join('');
  const explanationHtml = `<div data-role="quiz-explanation" class="quiz-explanation" hidden>${
    explanation && explanation.length > 0 ? explanation : 'Correct answers highlighted above.'
  }</div>`;
  const buttonText = correctIndices.length > 1 ? 'Show correct answers' : 'Show correct answer';
  const styleBlock = `<style data-quiz-style>
  .quiz-card{border:1px solid #e2e8f0;border-radius:12px;padding:18px;background:#fff;box-shadow:0 6px 18px 0 rgba(15,23,42,0.04);}
  .quiz-question{margin:0;color:#0f172a;font-size:1.05rem;font-weight:700;line-height:1.3;}
  .quiz-options{display:flex;flex-direction:column;gap:10px;margin:14px 0 0;padding:0;list-style:none;}
  .quiz-option{display:flex;align-items:flex-start;gap:12px;width:100%;border:1px solid #e2e8f0;border-radius:12px;background:#f8fafc;padding:10px 12px;cursor:pointer;text-align:left;transition:background 0.15s ease,border-color 0.15s ease,box-shadow 0.15s ease;}
  .quiz-option:hover{background:#fff;border-color:#cbd5e1;box-shadow:0 4px 12px rgba(148,163,184,0.28);}
  .quiz-option[aria-pressed="true"]{border-color:#94a3b8;background:#fff;box-shadow:0 4px 12px rgba(148,163,184,0.35);}
  .quiz-marker{margin-top:3px;display:inline-flex;height:18px;width:18px;flex-shrink:0;border-radius:999px;border:2px solid #cbd5e1;box-shadow:inset 0 0 0 2px #f8fafc;background:#fff;line-height:1;font-size:11px;color:#0f172a;align-items:center;justify-content:center;}
  .quiz-answer{display:block;color:#0f172a;font-size:0.98rem;line-height:1.45;}
  .quiz-explanation{margin-top:14px;border-left:4px solid #10b981;border-radius:10px;padding:12px 14px;background:#ecfdf3;color:#0f172a;font-size:0.94rem;}
  .quiz-reveal{display:inline-flex;align-items:center;gap:8px;margin-top:16px;border:1px solid #0f172a;border-radius:999px;padding:10px 16px;background:#0f172a;color:#fff;font-weight:650;font-size:0.95rem;cursor:pointer;transition:transform 0.1s ease,box-shadow 0.15s ease;}
  .quiz-reveal:hover{transform:translateY(-1px);box-shadow:0 10px 18px rgba(15,23,42,0.22);}
  .quiz-reveal[aria-disabled="true"]{opacity:0.65;cursor:default;box-shadow:none;transform:none;}
  .quiz-correct{border-color:#10b981;background:#ecfdf3;box-shadow:0 4px 12px rgba(16,185,129,0.28);}
  .quiz-wrong{border-color:#f43f5e;background:#fff5f7;box-shadow:0 4px 12px rgba(244,63,94,0.18);}
  .quiz-selected{border-color:#94a3b8;}
  </style>`;
  const quizHtml = `${styleBlock}<div id="${id}" data-quiz="${kind}" class="quiz-card"><div class="quiz-question" id="${id}-question">${question}</div><div class="quiz-options" role="group" aria-labelledby="${id}-question">${options}</div><button type="button" data-role="quiz-reveal" class="quiz-reveal">${buttonText}</button>${explanationHtml}</div>`;
  const payloadJson = JSON.stringify({ 'text/html': quizHtml });
  const bootstrap = `(function(){const root=document.currentScript?.parentElement;const dataEl=root?.querySelector('script[data-type="quiz-html"]');if(!root||!dataEl)return;let html='';try{const parsed=JSON.parse(dataEl.textContent||'{}');html=parsed['text/html']||'';}catch(e){return;}if(!html)return;root.insertAdjacentHTML('beforeend', html);const quiz=root.querySelector('[data-quiz]');if(!quiz||quiz.dataset.quizBound)return;quiz.dataset.quizBound='true';const mode=quiz.getAttribute('data-quiz');const options=Array.from(quiz.querySelectorAll('[data-role="quiz-option"]'));const button=quiz.querySelector('[data-role="quiz-reveal"]');const explanation=quiz.querySelector('[data-role="quiz-explanation"]');const correct=quiz.querySelectorAll('[data-correct="true"]');const markSelection=(target)=>{if(mode==='multiple-choice'){options.forEach((node)=>{node.setAttribute('aria-pressed','false');node.classList.remove('quiz-selected');const mark=node.querySelector('[data-role="quiz-marker"]');if(mark&&mark.textContent!=='✓')mark.textContent='';});}const isSelected=target.getAttribute('aria-pressed')==='true';const nextState=!isSelected;target.setAttribute('aria-pressed',String(nextState));target.classList.toggle('quiz-selected',nextState);const marker=target.querySelector('[data-role="quiz-marker"]');if(marker&&marker.textContent!=='✓'){marker.textContent=nextState?'•':'';}};options.forEach((option)=>{option.addEventListener('click',()=>markSelection(option));option.addEventListener('keydown',(event)=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();markSelection(option);}});});const reveal=()=>{correct.forEach((option)=>{option.classList.add('quiz-correct');option.setAttribute('aria-checked','true');const marker=option.querySelector('[data-role="quiz-marker"]');if(marker)marker.textContent='✓';});options.forEach((option)=>{const isCorrect=option.getAttribute('data-correct')==='true';const marker=option.querySelector('[data-role="quiz-marker"]');const isSelected=option.getAttribute('aria-pressed')==='true';if(!isCorrect&&isSelected){option.classList.add('quiz-wrong');if(marker&&!marker.textContent)marker.textContent='✕';}});if(explanation){explanation.hidden=false;explanation.classList.remove('hidden');}if(button){button.setAttribute('aria-disabled','true');button.classList.add('pointer-events-none','opacity-80');button.textContent='Answer shown';}};button?.addEventListener('click',reveal,{once:true});button?.addEventListener('keydown',(event)=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();reveal();}},{once:true});})();`;
  return `<div data-quiz-wrapper><script type="application/json" data-type="quiz-html">${payloadJson}</script><script>${bootstrap}</script></div>`;
};

const fallbackPlainText = '<IPython.core.display.HTML object>';

const emitNotebookHtml = (html) => {
  if (!html) return [];

  const codeKey = randomBytes(6).toString('hex');
  const outputKey = randomBytes(6).toString('hex');
  const blockKey = randomBytes(6).toString('hex');
  const outputId = randomBytes(12).toString('hex');

  return [
    {
      type: 'block',
      kind: 'notebook-code',
      children: [
        {
          type: 'code',
          lang: 'python',
          executable: false,
          value: '',
          visibility: 'remove',
          key: codeKey,
        },
        {
          type: 'output',
          id: outputId,
          data: [
            {
              output_type: 'execute_result',
              execution_count: 1,
              metadata: {},
              data: {
                'text/plain': fallbackPlainText,
                'text/html': html,
              },
            },
          ],
          key: outputKey,
        },
      ],
      key: blockKey,
    },
  ];
};

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
    base: {
      type: Number,
      doc: 'Set to 1 to author indices with a one-based convention.',
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
    const base = parseBase(data.options?.base);
    const correctRaw = data.options?.correct;
    if (correctRaw === undefined || correctRaw === null) {
      throw new Error('Specify :correct: for multiple-choice quizzes.');
    }
    const correctIdx = normalizeIndex(Number(correctRaw), base, answers.length);
    const explanation = (data.options?.explanation ?? '').trim();
    const html = buildQuizHtml({
      question,
      answers,
      correctIndices: [correctIdx],
      explanation,
      kind: 'multiple-choice',
    });
    return emitNotebookHtml(html);
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
    base: {
      type: Number,
      doc: 'Set to 1 to author indices with a one-based convention.',
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
    const base = parseBase(data.options?.base);
    const correctIndices = parseIndexList(data.options?.correct, base, answers.length);
    const explanation = (data.options?.explanation ?? '').trim();
    const html = buildQuizHtml({
      question,
      answers,
      correctIndices,
      explanation,
      kind: 'checkboxes',
    });
    return emitNotebookHtml(html);
  },
};

const plugin = {
  name: 'Interactive quiz directives',
  directives: [multipleChoiceDirective, checkboxDirective],
};

export default plugin;
