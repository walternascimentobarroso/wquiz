import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api'
import { QuestionPrompt } from '../components/QuestionPrompt'
import {
  ReferenceLinks,
  type QuestionReferenceLink,
} from '../components/ReferenceLinks'
import { ScoreDonut } from '../components/ScoreDonut'
import { LanguageSwitcher, useI18n } from '../i18n'
import { formatDuration } from '../utils/time'

type OptionLabel = {
  id: number
  text: string
}

type AnswerReview = {
  question_id: number
  prompt: string
  is_correct: boolean
  explanation: string
  selected_options?: OptionLabel[]
  correct_options?: OptionLabel[]
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

type ReviewFilter = 'all' | 'wrong' | 'correct'

function scoreTone(percentage: number): 'high' | 'mid' | 'low' {
  if (percentage >= 70) return 'high'
  if (percentage >= 40) return 'mid'
  return 'low'
}

function optionLines(options: OptionLabel[] | undefined): string {
  if (!options?.length) return ''
  return options.map((option) => option.text).join('\n')
}

export function ResultPage() {
  const { t } = useI18n()
  const { sessionId } = useParams()
  const id = Number(sessionId)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState<ReviewFilter>('all')

  useEffect(() => {
    api
      .getResult(id)
      .then((data) => setResult(data as unknown as Result))
      .catch((err: Error) => setError(err.message))
  }, [id])

  const wrongCount = result
    ? Math.max(0, result.total_questions - result.score)
    : 0

  const filteredAnswers = useMemo(() => {
    if (!result?.answers) return []
    if (filter === 'wrong') return result.answers.filter((item) => !item.is_correct)
    if (filter === 'correct') return result.answers.filter((item) => item.is_correct)
    return result.answers
  }, [filter, result])

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

  const tone = scoreTone(result.percentage)
  const hasReview = result.answers?.length > 0

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
        <ScoreDonut
          percentage={result.percentage}
          correct={result.score}
          wrong={wrongCount}
          tone={tone}
          label={t('result.donutLabel', {
            percent: Math.round(result.percentage),
            correct: result.score,
            wrong: wrongCount,
          })}
        />
        <p>
          {t('result.scoreLine', {
            score: result.score,
            total: result.total_questions,
          })}
        </p>
        <p className="score-breakdown">
          {t('result.breakdown', {
            correct: result.score,
            wrong: wrongCount,
          })}
        </p>
        {typeof result.duration_seconds === 'number' && (
          <p className="timer-result">
            {t('result.timeUsed', {
              duration: formatDuration(result.duration_seconds),
            })}
          </p>
        )}
        <div className="actions result-actions">
          <Link className="btn" to="/">
            {t('result.newQuiz')}
          </Link>
          {hasReview && wrongCount > 0 && (
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => {
                setFilter('wrong')
                document.getElementById('review-list')?.scrollIntoView({
                  behavior: 'smooth',
                  block: 'start',
                })
              }}
            >
              {t('result.reviewWrong')}
            </button>
          )}
        </div>
      </section>

      {hasReview && (
        <section className="review-section" id="review-list">
          <div className="review-toolbar">
            <h2 className="review-title">{t('result.reviewTitle')}</h2>
            <div className="filter-chips" role="group" aria-label={t('result.filterLabel')}>
              {(
                [
                  ['all', result.answers.length],
                  ['wrong', wrongCount],
                  ['correct', result.score],
                ] as const
              ).map(([key, count]) => (
                <button
                  key={key}
                  type="button"
                  className={`filter-chip${filter === key ? ' active' : ''}`}
                  aria-pressed={filter === key}
                  onClick={() => setFilter(key)}
                >
                  {t(`result.filter.${key}`)}
                  <span className="filter-count">{count}</span>
                </button>
              ))}
            </div>
          </div>

          {filteredAnswers.length === 0 ? (
            <p className="muted">{t('result.filterEmpty')}</p>
          ) : (
            <div className="review-list">
              {filteredAnswers.map((item) => {
                const selectedText = optionLines(item.selected_options)
                const correctText = optionLines(item.correct_options)
                const sameAnswer =
                  item.is_correct &&
                  selectedText.length > 0 &&
                  selectedText === correctText

                return (
                  <article
                    key={item.question_id}
                    className={`review-item ${item.is_correct ? 'is-correct' : 'is-wrong'}`}
                  >
                    <div className="review-head">
                      <span
                        className={`status-icon ${item.is_correct ? 'ok' : 'bad'}`}
                        aria-label={
                          item.is_correct ? t('result.statusCorrect') : t('result.statusWrong')
                        }
                      >
                        {item.is_correct ? '✓' : '✗'}
                      </span>
                      <QuestionPrompt prompt={item.prompt} compact />
                    </div>

                    {(selectedText || correctText) && (
                      <div className="review-answers">
                        {sameAnswer ? (
                          <p className="review-answer-line ok-line">
                            <span className="review-answer-label">
                              {t('result.correctAnswer')}
                            </span>
                            <span className="review-answer-text">{correctText}</span>
                          </p>
                        ) : (
                          <>
                            {selectedText && (
                              <p
                                className={`review-answer-line ${item.is_correct ? 'ok-line' : 'bad-line'}`}
                              >
                                <span className="review-answer-label">
                                  {t('result.yourAnswer')}
                                </span>
                                <span className="review-answer-text">{selectedText}</span>
                              </p>
                            )}
                            {correctText && !item.is_correct && (
                              <p className="review-answer-line ok-line">
                                <span className="review-answer-label">
                                  {t('result.correctAnswer')}
                                </span>
                                <span className="review-answer-text">{correctText}</span>
                              </p>
                            )}
                          </>
                        )}
                      </div>
                    )}

                    {item.explanation && (
                      <details className="review-explanation" open={!item.is_correct}>
                        <summary>{t('result.explanation')}</summary>
                        <p>{item.explanation}</p>
                      </details>
                    )}
                    <ReferenceLinks references={item.references} />
                  </article>
                )
              })}
            </div>
          )}
        </section>
      )}
    </div>
  )
}
