import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, type QuizSummary } from '../api'
import { StudySetupModal } from '../components/StudySetupModal'
import { LanguageSwitcher, useI18n } from '../i18n'

const MODE_IDS = ['practice', 'study', 'flashcard'] as const

export function HomePage() {
  const { t } = useI18n()
  const [quizzes, setQuizzes] = useState<QuizSummary[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [studySetup, setStudySetup] = useState<QuizSummary | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    api
      .listQuizzes()
      .then((data) => setQuizzes(data.items))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function start(
    quizId: number,
    mode: (typeof MODE_IDS)[number],
    options?: { questionCount?: number; timeLimitMinutes?: number; theme?: string },
  ) {
    setBusy(true)
    setError('')
    try {
      const session = await api.startSession(quizId, mode, options)
      navigate(`/session/${session.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : t('home.startFailed'))
    } finally {
      setBusy(false)
    }
  }

  function handleModeClick(quiz: QuizSummary, mode: (typeof MODE_IDS)[number]) {
    if (mode === 'study') {
      setStudySetup(quiz)
      return
    }
    void start(quiz.id, mode)
  }

  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand">
          W<span>Quiz</span>
        </Link>
        <LanguageSwitcher />
      </header>

      <section className="hero">
        <h1>{t('home.heroTitle')}</h1>
        <p>{t('home.heroBody')}</p>
      </section>

      {loading && <p className="muted">{t('home.loadingQuizzes')}</p>}
      {error && <p className="error">{error}</p>}

      <div className="quiz-grid">
        {quizzes.map((quiz, index) => (
          <article
            key={quiz.id}
            className="quiz-row"
            style={{ animationDelay: `${index * 60}ms` }}
          >
            <div>
              <h2>{quiz.title}</h2>
              <p className="meta">
                {quiz.category} · {t('home.questionsCount', { count: quiz.question_count })}
              </p>
              <p className="muted">{quiz.description}</p>
            </div>
            <div className="mode-picks">
              {MODE_IDS.map((modeId) => (
                <button
                  key={modeId}
                  type="button"
                  className={modeId === 'practice' ? 'btn' : 'btn btn-ghost'}
                  disabled={busy}
                  onClick={() => handleModeClick(quiz, modeId)}
                >
                  {t(`modes.${modeId}`)}
                </button>
              ))}
            </div>
          </article>
        ))}
      </div>

      {studySetup && (
        <StudySetupModal
          quizTitle={studySetup.title}
          maxQuestions={Math.max(1, studySetup.question_count)}
          themes={studySetup.themes ?? []}
          busy={busy}
          onCancel={() => setStudySetup(null)}
          onConfirm={({ questionCount, timeLimitMinutes, theme }) => {
            void start(studySetup.id, 'study', {
              questionCount,
              timeLimitMinutes,
              theme,
            }).then(() => setStudySetup(null))
          }}
        />
      )}
    </div>
  )
}
