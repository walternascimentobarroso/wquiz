export const en = {
  common: {
    brand: 'WQuiz',
    back: 'Back',
    backHome: 'Back to home',
    loading: 'Loading…',
    cancel: 'Cancel',
    close: 'Close',
    language: 'Language',
  },
  modes: {
    practice: 'Practice test',
    study: 'Study',
    studyMode: 'Study mode',
    flashcard: 'Flashcards',
  },
  home: {
    heroTitle: 'Learn at your own pace',
    heroBody:
      'Pick a quiz and a mode: practice test, study with explanations, or Anki-style flashcards. In study mode you can filter by topic.',
    loadingQuizzes: 'Loading quizzes…',
    questionsCount: '{count} questions',
    startFailed: 'Failed to start',
  },
  studySetup: {
    title: 'Configure study',
    theme: 'Topic',
    allThemes: 'All topics ({count})',
    themeHint: 'Filters questions before picking the count.',
    questionCount: 'Number of questions',
    maxInTheme: 'Maximum in this topic: {count}',
    timeLimit: 'Time limit (minutes)',
    minutes: '{n} min',
    start: 'Start study',
  },
  session: {
    timeRemaining: 'Time remaining',
    score: 'Score: {score}',
    selectExact: 'Select exactly {n} options',
    selectN: 'Select {n} options',
    selectProgress: ' ({selected}/{needed})',
    correct: 'Correct!',
    incorrect: 'Incorrect answer',
    previous: 'Previous',
    confirm: 'Confirm',
    updateAnswer: 'Update answer',
    next: 'Next',
    finish: 'Finish',
    seeResult: 'See result',
    showAnswer: 'Show answer',
    again: 'Again',
    hard: 'Hard',
    good: 'Good',
    easy: 'Easy',
    loadFailed: 'Failed to load session',
    answerFailed: 'Failed to submit answer',
    nextFailed: 'Could not go forward',
    prevFailed: 'Could not go back',
    finishFailed: 'Failed to finish',
    revealFailed: 'Failed to reveal',
    rateFailed: 'Failed to rate',
    references: 'References',
  },
  finishModal: {
    title: 'There are still unanswered questions',
    body:
      'You answered {answered} of {total} questions. {remaining} still remain.',
    ask: 'Do you want to finish anyway or continue the quiz?',
    continue: 'Continue',
    finishAnyway: 'Finish anyway',
  },
  result: {
    title: 'Result',
    scoreLine: '{score} of {total} correct',
    timeUsed: 'Time used: {duration}',
    newQuiz: 'New quiz',
    calculating: 'Calculating result…',
  },
}

type DeepStringify<T> = {
  [K in keyof T]: T[K] extends string ? string : DeepStringify<T[K]>
}

export type FrontendMessages = DeepStringify<typeof en>