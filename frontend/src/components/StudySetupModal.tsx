import { useEffect, useMemo, useState, type FormEvent } from 'react'
import { useI18n } from '../i18n'

export type ThemeOption = {
  name: string
  question_count: number
}

type StudySetupModalProps = {
  quizTitle: string
  maxQuestions: number
  themes?: ThemeOption[]
  busy?: boolean
  onCancel: () => void
  onConfirm: (options: {
    questionCount: number
    timeLimitMinutes: number
    theme?: string
  }) => void
}

const TIME_PRESETS = [15, 30, 60, 90, 120]
const ALL_THEMES = ''

export function StudySetupModal({
  quizTitle,
  maxQuestions,
  themes = [],
  busy = false,
  onCancel,
  onConfirm,
}: StudySetupModalProps) {
  const { t } = useI18n()
  const [theme, setTheme] = useState(ALL_THEMES)
  const poolSize = useMemo(() => {
    if (!theme) {
      return maxQuestions
    }
    const match = themes.find((item) => item.name === theme)
    return Math.max(1, match?.question_count ?? maxQuestions)
  }, [theme, themes, maxQuestions])

  const defaultCount = Math.min(10, poolSize)
  const [questionCount, setQuestionCount] = useState(defaultCount)
  const [timeLimitMinutes, setTimeLimitMinutes] = useState(120)

  useEffect(() => {
    setQuestionCount((current) => Math.min(Math.max(1, current), poolSize))
  }, [poolSize])

  const countOptions = useMemo(() => {
    const presets = [5, 10, 15, 20].filter((n) => n <= poolSize)
    if (!presets.includes(poolSize)) {
      presets.push(poolSize)
    }
    return presets
  }, [poolSize])

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    onConfirm({
      questionCount: Math.min(Math.max(1, questionCount), poolSize),
      timeLimitMinutes: Math.min(Math.max(1, timeLimitMinutes), 600),
      theme: theme || undefined,
    })
  }

  return (
    <div className="modal-backdrop" role="presentation" onClick={onCancel}>
      <form
        className="modal-panel"
        role="dialog"
        aria-modal="true"
        aria-labelledby="study-setup-title"
        onClick={(event) => event.stopPropagation()}
        onSubmit={handleSubmit}
      >
        <h2 id="study-setup-title">{t('studySetup.title')}</h2>
        <p className="muted">{quizTitle}</p>

        {themes.length > 0 && (
          <div className="field">
            <label htmlFor="study-theme">{t('studySetup.theme')}</label>
            <select
              id="study-theme"
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
            >
              <option value={ALL_THEMES}>
                {t('studySetup.allThemes', { count: maxQuestions })}
              </option>
              {themes.map((item) => (
                <option key={item.name} value={item.name}>
                  {item.name} ({item.question_count})
                </option>
              ))}
            </select>
            <span className="field-hint">{t('studySetup.themeHint')}</span>
          </div>
        )}

        <div className="field">
          <label htmlFor="question-count">{t('studySetup.questionCount')}</label>
          <div className="chip-row">
            {countOptions.map((n) => (
              <button
                key={n}
                type="button"
                className={`chip ${questionCount === n ? 'chip-active' : ''}`}
                onClick={() => setQuestionCount(n)}
              >
                {n}
              </button>
            ))}
          </div>
          <input
            id="question-count"
            type="number"
            min={1}
            max={poolSize}
            value={questionCount}
            onChange={(e) => setQuestionCount(Number(e.target.value) || 1)}
          />
          <span className="field-hint">
            {t('studySetup.maxInTheme', { count: poolSize })}
          </span>
        </div>

        <div className="field">
          <label htmlFor="time-limit">{t('studySetup.timeLimit')}</label>
          <div className="chip-row">
            {TIME_PRESETS.map((n) => (
              <button
                key={n}
                type="button"
                className={`chip ${timeLimitMinutes === n ? 'chip-active' : ''}`}
                onClick={() => setTimeLimitMinutes(n)}
              >
                {t('studySetup.minutes', { n })}
              </button>
            ))}
          </div>
          <input
            id="time-limit"
            type="number"
            min={1}
            max={600}
            value={timeLimitMinutes}
            onChange={(e) => setTimeLimitMinutes(Number(e.target.value) || 1)}
          />
        </div>

        <div className="actions">
          <button type="button" className="btn btn-ghost" disabled={busy} onClick={onCancel}>
            {t('common.cancel')}
          </button>
          <button type="submit" className="btn" disabled={busy}>
            {t('studySetup.start')}
          </button>
        </div>
      </form>
    </div>
  )
}
