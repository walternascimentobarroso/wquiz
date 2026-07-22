import { useEffect, useState, type FormEvent } from 'react'
import { ZEND_THEMES } from '../constants/themes'
import type { Question, QuestionPayload } from '../api'
import { useI18n } from '../i18n'

export type DraftOption = { text: string; is_correct: boolean }

export type DraftReference = { url: string; label: string }

export type QuestionDraft = {
  prompt: string
  explanation: string
  theme: string
  options: DraftOption[]
  references: DraftReference[]
}

const MIN_OPTIONS = 2
const MAX_OPTIONS = 6
const MAX_REFERENCES = 5

function isHttpUrl(value: string): boolean {
  return /^https?:\/\//i.test(value.trim())
}

export function emptyQuestionDraft(): QuestionDraft {
  return {
    prompt: '',
    explanation: '',
    theme: '',
    options: [
      { text: '', is_correct: true },
      { text: '', is_correct: false },
      { text: '', is_correct: false },
      { text: '', is_correct: false },
    ],
    references: [],
  }
}

export function draftFromQuestion(question: Question): QuestionDraft {
  const options =
    question.options.length >= MIN_OPTIONS
      ? question.options
          .slice()
          .sort((a, b) => a.position - b.position)
          .map((opt) => ({ text: opt.text, is_correct: opt.is_correct }))
      : emptyQuestionDraft().options
  const references = (question.references ?? [])
    .slice()
    .sort((a, b) => a.position - b.position)
    .map((ref) => ({ url: ref.url, label: ref.label ?? '' }))
  return {
    prompt: question.prompt,
    explanation: question.explanation ?? '',
    theme: question.theme ?? '',
    options,
    references,
  }
}

type QuestionFormProps = {
  title: string
  initial: QuestionDraft
  busy?: boolean
  extraThemes?: string[]
  onCancel: () => void
  onSubmit: (payload: QuestionPayload) => Promise<void> | void
}

export function QuestionForm({
  title,
  initial,
  busy = false,
  extraThemes = [],
  onCancel,
  onSubmit,
}: QuestionFormProps) {
  const { t } = useI18n()
  const [prompt, setPrompt] = useState(initial.prompt)
  const [explanation, setExplanation] = useState(initial.explanation)
  const [theme, setTheme] = useState(initial.theme)
  const [options, setOptions] = useState<DraftOption[]>(initial.options)
  const [references, setReferences] = useState<DraftReference[]>(initial.references)
  const [error, setError] = useState('')

  useEffect(() => {
    setPrompt(initial.prompt)
    setExplanation(initial.explanation)
    setTheme(initial.theme)
    setOptions(initial.options)
    setReferences(initial.references)
    setError('')
  }, [initial])

  const themeChoices = Array.from(
    new Set([...ZEND_THEMES, ...extraThemes.filter(Boolean), theme].filter(Boolean)),
  )

  function toggleCorrect(index: number) {
    setOptions((prev) => {
      const next = prev.map((opt, i) =>
        i === index ? { ...opt, is_correct: !opt.is_correct } : opt,
      )
      if (!next.some((opt) => opt.is_correct) && next[index]) {
        next[index] = { ...next[index], is_correct: true }
      }
      return next
    })
  }

  function updateOptionText(index: number, text: string) {
    setOptions((prev) => prev.map((opt, i) => (i === index ? { ...opt, text } : opt)))
  }

  function addOption() {
    if (options.length >= MAX_OPTIONS) return
    setOptions((prev) => [...prev, { text: '', is_correct: false }])
  }

  function removeOption(index: number) {
    if (options.length <= MIN_OPTIONS) return
    setOptions((prev) => {
      const next = prev.filter((_, i) => i !== index)
      if (!next.some((opt) => opt.is_correct) && next.length > 0) {
        next[0] = { ...next[0], is_correct: true }
      }
      return next
    })
  }

  function addReference() {
    if (references.length >= MAX_REFERENCES) return
    setReferences((prev) => [...prev, { url: '', label: '' }])
  }

  function updateReference(index: number, patch: Partial<DraftReference>) {
    setReferences((prev) =>
      prev.map((ref, i) => (i === index ? { ...ref, ...patch } : ref)),
    )
  }

  function removeReference(index: number) {
    setReferences((prev) => prev.filter((_, i) => i !== index))
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError('')
    const filled = options
      .map((opt) => ({ ...opt, text: opt.text.trim() }))
      .filter((opt) => opt.text)
    if (filled.length < MIN_OPTIONS) {
      setError(t('questionForm.needOptions', { min: MIN_OPTIONS }))
      return
    }
    if (!filled.some((opt) => opt.is_correct)) {
      setError(t('questionForm.needCorrect'))
      return
    }
    if (!prompt.trim()) {
      setError(t('questionForm.needPrompt'))
      return
    }

    const filledRefs = references
      .map((ref) => ({
        url: ref.url.trim(),
        label: ref.label.trim(),
      }))
      .filter((ref) => ref.url || ref.label)

    for (const ref of filledRefs) {
      if (!ref.url || !isHttpUrl(ref.url)) {
        setError(t('questionForm.needValidUrl'))
        return
      }
    }

    if (filledRefs.length > MAX_REFERENCES) {
      setError(t('questionForm.needMaxReferences', { max: MAX_REFERENCES }))
      return
    }

    await onSubmit({
      prompt: prompt.trim(),
      explanation: explanation.trim(),
      theme: theme.trim(),
      options: filled.map((opt, index) => ({
        text: opt.text,
        is_correct: opt.is_correct,
        position: index,
      })),
      references: filledRefs.map((ref, index) => ({
        url: ref.url,
        label: ref.label,
        position: index,
      })),
    })
  }

  const correctMarked = options.filter((o) => o.is_correct).length

  return (
    <form className="question-form" onSubmit={(e) => void handleSubmit(e)}>
      <div className="drawer-header">
        <h2 id="question-form-title">{title}</h2>
        <button type="button" className="btn btn-ghost" disabled={busy} onClick={onCancel}>
          {t('common.close')}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="field">
        <label htmlFor="q-theme">{t('questionForm.theme')}</label>
        <select
          id="q-theme"
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          disabled={busy}
        >
          <option value="">{t('questionForm.noTheme')}</option>
          {themeChoices.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </div>

      <div className="field">
        <label htmlFor="q-prompt">{t('questionForm.prompt')}</label>
        <textarea
          id="q-prompt"
          className="textarea-tall"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          required
          disabled={busy}
          placeholder={t('questionForm.promptPlaceholder')}
        />
        <p className="field-hint">{t('questionForm.promptFenceHint')}</p>
      </div>

      <div className="field">
        <label htmlFor="q-explanation">{t('questionForm.explanation')}</label>
        <textarea
          id="q-explanation"
          value={explanation}
          onChange={(e) => setExplanation(e.target.value)}
          disabled={busy}
        />
      </div>

      <div className="field">
        <div className="field-row">
          <label>{t('questionForm.references')}</label>
          <button
            type="button"
            className="btn btn-ghost btn-sm"
            disabled={busy || references.length >= MAX_REFERENCES}
            onClick={addReference}
          >
            {t('questionForm.addReference')}
          </button>
        </div>
        <p className="field-hint">
          {t('questionForm.referencesHint', { max: MAX_REFERENCES })}
        </p>
        {references.length === 0 ? (
          <p className="muted">{t('questionForm.noReferences')}</p>
        ) : (
          references.map((ref, index) => (
            <div className="reference-row" key={index}>
              <input
                type="url"
                value={ref.url}
                placeholder={t('questionForm.urlPlaceholder')}
                disabled={busy}
                onChange={(e) => updateReference(index, { url: e.target.value })}
              />
              <input
                type="text"
                value={ref.label}
                placeholder={t('questionForm.labelPlaceholder')}
                disabled={busy}
                onChange={(e) => updateReference(index, { label: e.target.value })}
              />
              <button
                type="button"
                className="btn btn-ghost btn-sm"
                disabled={busy}
                onClick={() => removeReference(index)}
              >
                {t('questionForm.remove')}
              </button>
            </div>
          ))
        )}
      </div>

      <div className="field">
        <div className="field-row">
          <label>{t('questionForm.options')}</label>
          <button
            type="button"
            className="btn btn-ghost btn-sm"
            disabled={busy || options.length >= MAX_OPTIONS}
            onClick={addOption}
          >
            {t('questionForm.addOption')}
          </button>
        </div>
        <p className="field-hint">
          {t('questionForm.optionsHint', { min: MIN_OPTIONS, max: MAX_OPTIONS })}
          {correctMarked > 1
            ? t('questionForm.multiSuffix', { count: correctMarked })
            : ''}
        </p>
        {options.map((opt, index) => (
          <div className="option-row option-row-edit" key={index}>
            <textarea
              rows={2}
              value={opt.text}
              placeholder={t('questionForm.optionPlaceholder', { n: index + 1 })}
              disabled={busy}
              onChange={(e) => updateOptionText(index, e.target.value)}
            />
            <div className="option-controls">
              <label className="correct-label">
                <input
                  type="checkbox"
                  checked={opt.is_correct}
                  disabled={busy}
                  onChange={() => toggleCorrect(index)}
                />
                {t('questionForm.correct')}
              </label>
              <button
                type="button"
                className="btn btn-ghost btn-sm"
                disabled={busy || options.length <= MIN_OPTIONS}
                onClick={() => removeOption(index)}
              >
                {t('questionForm.remove')}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="actions drawer-actions">
        <button type="button" className="btn btn-ghost" disabled={busy} onClick={onCancel}>
          {t('common.cancel')}
        </button>
        <button type="submit" className="btn" disabled={busy}>
          {busy ? t('common.saving') : t('questionForm.save')}
        </button>
      </div>
    </form>
  )
}
