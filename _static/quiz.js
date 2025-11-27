(function () {
  const HIGHLIGHT_CLASSES = ['quiz-correct'];
  const WRONG_CLASSES = ['quiz-wrong'];
  const SELECTED_CLASSES = ['quiz-selected'];

  const revealQuiz = (root) => {
    const button = root.querySelector('[data-role="quiz-reveal"]');
    const explanation = root.querySelector('[data-role="quiz-explanation"]');
    const options = root.querySelectorAll('[data-correct="true"]');

    const reveal = () => {
      options.forEach((option) => {
        option.classList.add(...HIGHLIGHT_CLASSES);
        option.setAttribute('aria-checked', 'true');
        const marker = option.querySelector('[data-role="quiz-marker"]');
        if (marker) marker.textContent = '✓';
      });
      root.querySelectorAll('[data-role="quiz-option"]').forEach((option) => {
        const isCorrect = option.dataset.correct === 'true';
        const marker = option.querySelector('[data-role="quiz-marker"]');
        const isSelected = option.getAttribute('aria-pressed') === 'true';
        if (!isCorrect && isSelected) {
          option.classList.add(...WRONG_CLASSES);
          if (marker && !marker.textContent) marker.textContent = '✕';
        }
      });
      if (explanation) {
        explanation.hidden = false;
        explanation.classList.remove('hidden');
      }
      if (button) {
        button.setAttribute('aria-disabled', 'true');
        button.classList.add('pointer-events-none', 'opacity-80');
        button.textContent = 'Answer shown';
      }
    };

    button?.addEventListener('click', reveal, { once: true });
    button?.addEventListener(
      'keydown',
      (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          reveal();
        }
      },
      { once: true },
    );
  };

  const init = () => {
    document.querySelectorAll('[data-quiz]').forEach((quiz) => {
      if (quiz.dataset.quizBound === 'true') return;
      quiz.dataset.quizBound = 'true';
      const mode = quiz.dataset.quiz;
      const options = quiz.querySelectorAll('[data-role="quiz-option"]');

      options.forEach((option) => {
        option.addEventListener('click', () => {
          if (mode === 'multiple-choice') {
            options.forEach((node) => {
              node.setAttribute('aria-pressed', 'false');
              node.classList.remove(...SELECTED_CLASSES);
              const mark = node.querySelector('[data-role="quiz-marker"]');
              if (mark && mark.textContent !== '✓') mark.textContent = '';
            });
          }

          const isSelected = option.getAttribute('aria-pressed') === 'true';
          const nextState = !isSelected;
          option.setAttribute('aria-pressed', String(nextState));
          option.classList.toggle(SELECTED_CLASSES[0], nextState);
          const marker = option.querySelector('[data-role="quiz-marker"]');
          if (marker && marker.textContent !== '✓') {
            marker.textContent = nextState ? '•' : '';
          }
        });
      });

      revealQuiz(quiz);
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
