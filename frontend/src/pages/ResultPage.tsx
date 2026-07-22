import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api'
import { QuestionPrompt } from '../components/QuestionPrompt'
import {
  ReferenceLinks,
  type QuestionReferenceLink,
} from '../components/ReferenceLinks'
import { LanguageSwitcher, useI18n } from '../i18n'
import { formatDuration } from '../utils/time'

type AnswerReview = {
  question_id: number
  prompt: string
  is_correct: boolean
  explanation: string
  references?: QuestionReferenceLink[]
}

type Result = {
  score: number
  total_questions: number
  percentage: number
  mode: string
  duration_seconds?: number
  answers: AnswerReview[]
}

export function ResultPage() {
  const { t } = useI18n()
  const { sessionId } = useParams()
  const id = Number(sessionId)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .getResult(id)
      .then((data) => setResult(data as unknown as Result))
      .catch((err: Error) => setError(err.message))
  }, [id])

  if (error) {
    return (
      <div className="shell">
        <header className="topbar">
          <Link to="/" className="brand">
            W<span>Quiz</span>
          </Link>
          <LanguageSwitcher />
        </header>
        <p className="error">{error}</p>
        <Link to="/">{t('common.backHome')}</Link>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="shell">
        <header className="topbar">
          <Link to="/" className="brand">
            W<span>Quiz</span>
          </Link>
          <LanguageSwitcher />
        </header>
        <p className="muted">{t('result.calculating')}</p>
      </div>
    )
  }

  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand">
          W<span>Quiz</span>
        </Link>
        <LanguageSwitcher />
      </header>

      <section className="score-hero panel">
        <p className="muted">{t('result.title')}</p>
        <div className="big">{Math.round(result.percentage)}%</div>
        <p>
          {t('result.scoreLine', {
            score: result.score,
            total: result.total_questions,
          })}
        </p>
        {typeof result.duration_seconds === 'number' && (
          <p className="timer-result">
            {t('result.timeUsed', {
              duration: formatDuration(result.duration_seconds),
            })}
          </p>
        )}
        <div className="actions" style={{ justifyContent: 'center' }}>
          <Link className="btn" to="/">
            {t('result.newQuiz')}
          </Link>
        </div>
      </section>

      {result.answers?.length > 0 && (
        <div className="review-list">
          {result.answers.map((item) => (
            <article key={item.question_id} className="review-item">
              <div className="review-head">
                <span>{item.is_correct ? '✓' : '✗'}</span>
                <QuestionPrompt prompt={item.prompt} compact />
              </div>
              {item.explanation && (
                <p className="muted review-explanation">{item.explanation}</p>
              )}
              <ReferenceLinks references={item.references} />
            </article>
          ))}
        </div>
      )}
    </div>
  )
}
