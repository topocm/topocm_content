// The MyST widget lifecycle supplies an isolated element on every page visit.
async function render({ model, el }) {
  const question = model.get('question');
  const answers = model.get('answers');
  const correct = model.get('correctIndices');
  const multiple = model.get('kind') === 'checkboxes';
  const root = document.createElement('div');
  root.className = 'quiz-card';
  root.dataset.quiz = model.get('kind');
  const title = document.createElement('div');
  title.className = 'quiz-question';
  title.innerHTML = question;
  root.append(title);
  const group = document.createElement('div');
  group.className = 'quiz-options';
  group.setAttribute('role', 'group');
  group.setAttribute('aria-label', title.textContent);
  const options = answers.map((answer, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'quiz-option';
    button.setAttribute('aria-pressed', 'false');
    button.innerHTML = '<span class="quiz-marker" aria-hidden="true"></span><span class="quiz-answer"></span>';
    button.lastElementChild.innerHTML = answer;
    button.addEventListener('click', () => {
      const selected = button.getAttribute('aria-pressed') !== 'true';
      if (!multiple) options.forEach((option) => {
        option.setAttribute('aria-pressed', 'false');
        option.firstElementChild.textContent = '';
      });
      button.setAttribute('aria-pressed', String(selected));
      button.firstElementChild.textContent = selected ? '•' : '';
    });
    group.append(button);
    return button;
  });
  root.append(group);
  const reveal = document.createElement('button');
  reveal.type = 'button';
  reveal.className = 'quiz-reveal';
  reveal.textContent = correct.length > 1 ? 'Show correct answers' : 'Show correct answer';
  const explanation = document.createElement('div');
  explanation.className = 'quiz-explanation';
  explanation.hidden = true;
  explanation.setAttribute('aria-live', 'polite');
  explanation.innerHTML = model.get('explanation') || 'Correct answers highlighted above.';
  reveal.addEventListener('click', () => {
    options.forEach((option, index) => {
      if (correct.includes(index)) {
        option.classList.add('quiz-correct');
        option.firstElementChild.textContent = '✓';
      } else if (option.getAttribute('aria-pressed') === 'true') {
        option.classList.add('quiz-wrong');
        option.firstElementChild.textContent = '✕';
      }
      option.disabled = true;
    });
    explanation.hidden = false;
    reveal.disabled = true;
    reveal.textContent = 'Answer shown';
  }, { once: true });
  root.append(reveal, explanation);
  el.append(root);
  await window.MathJax.startup.promise;
  await window.MathJax.typesetPromise([root]);
  return () => {
    window.MathJax.typesetClear([root]);
    root.remove();
  };
}

export default { render };
