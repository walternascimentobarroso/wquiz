import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api, type Session } from '../api'
import { FinishModal } from '../components/FinishModal'
import { QuestionPrompt } from '../components/QuestionPrompt'
import { ReferenceLinks, type QuestionReferenceLink } from '../components/ReferenceLinks'
import { useSessionTimer } from '../hooks/useSessionTimer'
import { LanguageSwitcher, useI18n } from '../i18n'
import { DEFAULT_TIME_LIMIT_SECONDS } from '../utils/time'

type Option = { id: number; text: string; position: number }
type QuestionPayload = {
  type: 'question'
  index: number
  total: number
  question: {
    id: number
    prompt: string
    options: Option[]
    is_multi?: boolean
    correct_count?: number
  }
  selected_option_id?: number | null
  selected_option_ids?: number[]
  already_answered?: boolean
  can_go_previous?: boolean
  remaining?: number
  is_correct?: boolean
  correct_option_id?: number | null
  correct_option_ids?: number[]
  explanation?: string
  references?: QuestionReferenceLink[]
}
type FlashcardPayload = {
  type: 'flashcard'
  index: number
  total: number
  flashcard: { id: number; front: string }
  can_go_previous?: boolean
  remaining?: number
}
type CurrentPayload = QuestionPayload | FlashcardPayload | { completed: true }

function asIdList(value: unknown): number[] {
  if (!Array.isArray(value)) return []
  return value.filter((item): item is number => typeof item === 'number')
}

export function SessionPage() {
  const { t } = useI18n()
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const id = Number(sessionId)

  const [session, setSession] = useState<Session | null>(null)
  const [current, setCurrent] = useState<CurrentPayload | null>(null)
  const [selectedIds, setSelectedIds] = useState<number[]>([])
  const [feedback, setFeedback] = useState<Record<string, unknown> | null>(null)
  const [flipped, setFlipped] = useState(false)
  const [back, setBack] = useState('')
  const [cardReferences, setCardReferences] = useState<QuestionReferenceLink[]>([])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [initialRemaining, setInitialRemaining] = useState<number | null>(null)
  const [finishModal, setFinishModal] = useState<{ remaining: number; total: number } | null>(
    null,
  )
  const [timeLimitSeconds, setTimeLimitSeconds] = useState(DEFAULT_TIME_LIMIT_SECONDS)

  const handleTimeExpired = useCallback(() => {
    void (async () => {
      try {
        await api.finishSession(id, true)
        navigate(`/session/${id}/result`)
      } catch {
        navigate(`/session/${id}/result`)
      }
    })()
  }, [id, navigate])

  const { label: timerLabel, isLow } = useSessionTimer({
    initialRemaining,
    limitSeconds: timeLimitSeconds,
    running: session?.status === 'in_progress' && initialRemaining != null,
    onExpire: handleTimeExpired,
  })

  const loadCurrent = useCallback(async (mode?: Session['mode']) => {
    const data = (await api.getCurrent(id)) as CurrentPayload
    setCurrent(data)
    setFeedback(null)
    setFlipped(false)
    setBack('')
    setCardReferences([])
    if ('completed' in data && data.completed) {
      navigate(`/session/${id}/result`)
      return
    }
    if ('question' in data) {
      const fromList = asIdList(data.selected_option_ids)
      const fallback =
        typeof data.selected_option_id === 'number' ? [data.selected_option_id] : []
      setSelectedIds(fromList.length > 0 ? fromList : fallback)
      const activeMode = mode ?? session?.mode
      if (data.already_answered && activeMode === 'study') {
        setFeedback({
          is_correct: data.is_correct,
          correct_option_id: data.correct_option_id,
          correct_option_ids: data.correct_option_ids ?? asIdList(data.correct_option_ids),
          explanation: data.explanation,
          references: data.references ?? [],
          selected_option_id: data.selected_option_id,
          selected_option_ids: fromList.length > 0 ? fromList : fallback,
          advanced: false,
        })
      }
    } else {
      setSelectedIds([])
    }
  }, [id, navigate, session?.mode])

  useEffect(() => {
    async function boot() {
      try {
        const s = await api.getSession(id)
        setSession(s)
        if (s.status === 'completed') {
          navigate(`/session/${id}/result`)
          return
        }
        if (s.time_limit_seconds && s.time_limit_seconds > 0) {
          setTimeLimitSeconds(s.time_limit_seconds)
        }
        setInitialRemaining(
          typeof s.remaining_seconds === 'number'
            ? s.remaining_seconds
            : s.time_limit_seconds ?? DEFAULT_TIME_LIMIT_SECONDS,
        )
        await loadCurrent(s.mode)
      } catch (err) {
        setError(err instanceof Error ? err.message : t('session.loadFailed'))
      }
    }
    void boot()
  }, [id, loadCurrent, navigate, t])

  async function refreshSession() {
    const refreshed = await api.getSession(id)
    setSession(refreshed)
    return refreshed
  }

  async function submitAnswer() {
    if (!current || !('question' in current) || selectedIds.length === 0) return
    const needed = current.question.correct_count ?? (current.question.is_multi ? 2 : 1)
    if (current.question.is_multi && selectedIds.length !== needed) {
      setError(t('session.selectExact', { n: needed }))
      return
    }
    setBusy(true)
    setError('')
    try {
      const result = await api.submitAnswer(id, current.question.id, selectedIds)
      setFeedback(result)
      await refreshSession()
      if (session?.mode === 'practice' && result.advanced !== false && !result.is_last) {
        await loadCurrent()
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : t('session.answerFailed'))
    } finally {
      setBusy(false)
    }
  }

  function toggleOption(optionId: number, isMulti: boolean, maxSelect: number) {
    setSelectedIds((prev) => {
      if (!isMulti) return [optionId]
      if (prev.includes(optionId)) return prev.filter((id) => id !== optionId)
      if (prev.length >= maxSelect) return [...prev.slice(1), optionId]
      return [...prev, optionId]
    })
  }

  async function goNext() {
    setBusy(true)
    setError('')
    try {
      if (feedback?.advanced !== true) {
        await api.goNext(id)
      }
      await refreshSession()
      await loadCurrent()
    } catch (err) {
      setError(err instanceof Error ? err.message : t('session.nextFailed'))
    } finally {
      setBusy(false)
    }
  }

  async function goPrevious() {
    setBusy(true)
    setError('')
    try {
      await api.goPrevious(id)
      await refreshSession()
      await loadCurrent()
    } catch (err) {
      setError(err instanceof Error ? err.message : t('session.prevFailed'))
    } finally {
      setBusy(false)
    }
  }

  async function requestFinish() {
    setBusy(true)
    setError('')
    try {
      const result = await api.finishSession(id, false)
      if (result.needs_confirmation) {
        setFinishModal({
          remaining: result.remaining,
          total: result.total_questions ?? session?.total_questions ?? 0,
        })
        return
      }
      navigate(`/session/${id}/result`)
    } catch (err) {
      setError(err instanceof Error ? err.message : t('session.finishFailed'))
    } finally {
      setBusy(false)
    }
  }

  async function confirmFinish() {
    setBusy(true)
    setError('')
    try {
      await api.finishSession(id, true)
      setFinishModal(null)
      navigate(`/session/${id}/result`)
    } catch (err) {
      setError(err instanceof Error ? err.message : t('session.finishFailed'))
    } finally {
      setBusy(false)
    }
  }

  async function revealCard() {
    if (!current || !('flashcard' in current)) return
    setBusy(true)
    try {
      const card = await api.revealFlashcard(id, current.flashcard.id)
      setBack(card.back)
      setCardReferences(card.references ?? [])
      setFlipped(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : t('session.revealFailed'))
    } finally {
      setBusy(false)
    }
  }

  async function rate(rating: 'again' | 'hard' | 'good' | 'easy') {
    if (!current || !('flashcard' in current)) return
    setBusy(true)
    try {
      const result = await api.reviewFlashcard(id, current.flashcard.id, rating)
      await refreshSession()
      if (result.is_last || result.advanced === false) {
        setFlipped(false)
        setBack('')
        setCardReferences([])
        setFeedback({ is_last: true })
        return
      }
      await loadCurrent()
    } catch (err) {
      setError(err instanceof Error ? err.message : t('session.rateFailed'))
    } finally {
      setBusy(false)
    }
  }

  if (error && !session) {
    return (
      <div className="shell">
        <header className="topbar">
          <Link to="/" className="brand">
            W<span>Quiz</span>
          </Link>
          <LanguageSwitcher />
        </header>
        <p className="error">{error}</p>
        <Link to="/">{t('common.back')}</Link>
      </div>
    )
  }

  if (!session || !current || 'completed' in current) {
    return (
      <div className="shell">
        <header className="topbar">
          <Link to="/" className="brand">
            W<span>Quiz</span>
          </Link>
          <LanguageSwitcher />
        </header>
        <p className="muted">{t('common.loading')}</p>
      </div>
    )
  }

  const index = 'index' in current ? current.index : 0
  const total = 'total' in current ? current.total : session.total_questions
  const isLastQuestion = index >= total - 1
  const awaitingResult =
    Boolean(feedback?.is_last) ||
    (isLastQuestion && Boolean(feedback)) ||
    (isLastQuestion && 'already_answered' in current && current.already_answered)
  const pct = total ? ((index + (feedback && !isLastQuestion ? 1 : 0)) / total) * 100 : 0
  const canGoPrevious = Boolean(current.can_go_previous) && !busy
  const showNext =
    !awaitingResult &&
    (('already_answered' in current && current.already_answered && session.mode !== 'practice') ||
      (Boolean(feedback) && session.mode === 'study') ||
      (session.mode === 'practice' && feedback?.advanced === false))

  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand">
          W<span>Quiz</span>
        </Link>
        <div className="topbar-actions">
          <span className="muted">
            {session.mode === 'practice' && t('modes.practice')}
            {session.mode === 'study' && t('modes.studyMode')}
            {session.mode === 'flashcard' && t('modes.flashcard')}
          </span>
          <LanguageSwitcher />
        </div>
      </header>

      <div className="panel">
        <div className="progress">
          <span>
            {Math.min(index + 1, total)} / {total}
          </span>
          <span
            className={`timer ${isLow ? 'timer-low' : ''}`}
            aria-live="polite"
            aria-label={t('session.timeRemaining')}
          >
            {timerLabel}
          </span>
          {session.mode !== 'practice' && (
            <span>{t('session.score', { score: session.score })}</span>
          )}
        </div>
        <div className="progress-bar">
          <span style={{ width: `${pct}%` }} />
        </div>

        {error && <p className="error">{error}</p>}

        {'question' in current && (
          <>
            <QuestionPrompt prompt={current.question.prompt} />
            {current.question.is_multi && (
              <p className="muted multi-hint">
                {t('session.selectN', { n: current.question.correct_count ?? 2 })}
                {selectedIds.length > 0
                  ? t('session.selectProgress', {
                      selected: selectedIds.length,
                      needed: current.question.correct_count ?? 2,
                    })
                  : ''}
              </p>
            )}
            <div className="options">
              {current.question.options.map((opt) => {
                const isMulti = Boolean(current.question.is_multi)
                const maxSelect = current.question.correct_count ?? 2
                const selectedSet = new Set(selectedIds)
                const correctSet = new Set(
                  asIdList(feedback?.correct_option_ids).length > 0
                    ? asIdList(feedback?.correct_option_ids)
                    : typeof feedback?.correct_option_id === 'number'
                      ? [feedback.correct_option_id]
                      : [],
                )
                let cls = 'option'
                if (selectedSet.has(opt.id)) cls += ' selected'
                if (feedback && session.mode === 'study') {
                  if (correctSet.has(opt.id)) cls += ' correct'
                  else if (selectedSet.has(opt.id) && !feedback.is_correct) cls += ' wrong'
                }
                return (
                  <button
                    key={opt.id}
                    type="button"
                    className={cls}
                    disabled={(Boolean(feedback) && session.mode === 'study') || busy}
                    onClick={() => toggleOption(opt.id, isMulti, maxSelect)}
                  >
                    {isMulti && (
                      <span className="option-check" aria-hidden>
                        {selectedSet.has(opt.id) ? '☑' : '☐'}
                      </span>
                    )}
                    <span>{opt.text}</span>
                  </button>
                )
              })}
            </div>

            {feedback && session.mode === 'study' && (
              <div className={`feedback ${feedback.is_correct ? 'ok' : 'bad'}`}>
                <strong>
                  {feedback.is_correct ? t('session.correct') : t('session.incorrect')}
                </strong>
                <p>{String(feedback.explanation ?? '')}</p>
                <ReferenceLinks
                  references={
                    (feedback.references as QuestionReferenceLink[] | undefined) ?? []
                  }
                />
              </div>
            )}

            <div className="actions nav-actions">
              <button
                type="button"
                className="btn btn-ghost"
                disabled={!canGoPrevious}
                onClick={() => void goPrevious()}
              >
                {t('session.previous')}
              </button>

              {(!feedback || session.mode === 'practice') && (
                <button
                  type="button"
                  className="btn"
                  disabled={
                    selectedIds.length === 0 ||
                    busy ||
                    (Boolean(current.question.is_multi) &&
                      selectedIds.length !== (current.question.correct_count ?? 2))
                  }
                  onClick={() => void submitAnswer()}
                >
                  {current.already_answered
                    ? t('session.updateAnswer')
                    : t('session.confirm')}
                </button>
              )}

              {showNext && (
                <button type="button" className="btn" disabled={busy} onClick={() => void goNext()}>
                  {t('session.next')}
                </button>
              )}

              <button
                type="button"
                className={awaitingResult ? 'btn' : 'btn btn-warn'}
                disabled={busy}
                onClick={() => void requestFinish()}
              >
                {awaitingResult ? t('session.seeResult') : t('session.finish')}
              </button>
            </div>
          </>
        )}

        {'flashcard' in current && (
          <>
            <div className={`flashcard ${flipped ? 'flipped' : ''}`}>
              <div className="flashcard-inner">
                <div className="face">
                  <QuestionPrompt prompt={current.flashcard.front} compact />
                </div>
                <div className="face back">
                  <QuestionPrompt prompt={back || '…'} compact />
                  <ReferenceLinks references={cardReferences} />
                </div>
              </div>
            </div>
            <div className="actions nav-actions">
              <button
                type="button"
                className="btn btn-ghost"
                disabled={!canGoPrevious}
                onClick={() => void goPrevious()}
              >
                {t('session.previous')}
              </button>
              {!flipped ? (
                <button
                  type="button"
                  className="btn"
                  disabled={busy}
                  onClick={() => void revealCard()}
                >
                  {t('session.showAnswer')}
                </button>
              ) : (
                <>
                  <button
                    type="button"
                    className="btn btn-danger"
                    disabled={busy}
                    onClick={() => void rate('again')}
                  >
                    {t('session.again')}
                  </button>
                  <button
                    type="button"
                    className="btn btn-warn"
                    disabled={busy}
                    onClick={() => void rate('hard')}
                  >
                    {t('session.hard')}
                  </button>
                  <button
                    type="button"
                    className="btn"
                    disabled={busy}
                    onClick={() => void rate('good')}
                  >
                    {t('session.good')}
                  </button>
                  <button
                    type="button"
                    className="btn btn-ghost"
                    disabled={busy}
                    onClick={() => void rate('easy')}
                  >
                    {t('session.easy')}
                  </button>
                </>
              )}
              <button
                type="button"
                className={awaitingResult ? 'btn' : 'btn btn-warn'}
                disabled={busy}
                onClick={() => void requestFinish()}
              >
                {awaitingResult ? t('session.seeResult') : t('session.finish')}
              </button>
            </div>
          </>
        )}
      </div>

      {finishModal && (
        <FinishModal
          remaining={finishModal.remaining}
          total={finishModal.total}
          busy={busy}
          onCancel={() => setFinishModal(null)}
          onConfirm={() => void confirmFinish()}
        />
      )}
    </div>
  )
}
