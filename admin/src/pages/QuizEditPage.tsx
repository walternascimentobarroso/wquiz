import { useEffect, useMemo, useState, type FormEvent } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import {
  api,
  clearToken,
  getToken,
  type Question,
  type QuestionPayload,
  type Quiz,
} from '../api'
import {
  draftFromQuestion,
  emptyQuestionDraft,
  QuestionForm,
  type QuestionDraft,
} from '../components/QuestionForm'
import { PromptPreview } from '../components/PromptPreview'
import { LanguageSwitcher, useI18n } from '../i18n'
import { promptPreview } from '../utils/promptCode'

type EditorMode =
  | { kind: 'closed' }
  | { kind: 'create'; draft: QuestionDraft }
  | { kind: 'edit'; questionId: number; draft: QuestionDraft }

export function QuizEditPage() {
  const { t } = useI18n()
  const { quizId } = useParams()
  const id = Number(quizId)
  const navigate = useNavigate()

  const [quiz, setQuiz] = useState<Quiz | null>(null)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('')
  const [published, setPublished] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [busyQuiz, setBusyQuiz] = useState(false)
  const [busyQuestion, setBusyQuestion] = useState(false)
  const [themeFilter, setThemeFilter] = useState('')
  const [search, setSearch] = useState('')
  const [expandedId, setExpandedId] = useState<number | null>(null)
  const [editor, setEditor] = useState<EditorMode>({ kind: 'closed' })

  async function load() {
    try {
      const data = await api.getQuiz(id)
      setQuiz(data)
      setTitle(data.title)
      setDescription(data.description)
      setCategory(data.category)
      setPublished(data.is_published)
    } catch (err) {
      const msg = err instanceof Error ? err.message : t('quizEdit.loadFailed')
      setError(msg)
      if (/401|credenciais|autorizado|Unauthorized/i.test(msg)) {
        clearToken()
        navigate('/login')
      }
    }
  }

  useEffect(() => {
    if (!getToken()) {
      navigate('/login')
      return
    }
    void load()
    // boot once when quiz id changes
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, navigate])

  useEffect(() => {
    if (!message) return
    const timer = window.setTimeout(() => setMessage(''), 2800)
    return () => window.clearTimeout(timer)
  }, [message])

  const questions = useMemo(
    () =>
      (quiz?.questions ?? [])
        .slice()
        .sort((a, b) => a.position - b.position || a.id - b.id),
    [quiz],
  )

  const themesInQuiz = useMemo(() => {
    const set = new Set<string>()
    for (const q of questions) {
      if (q.theme?.trim()) set.add(q.theme.trim())
    }
    return Array.from(set).sort((a, b) => a.localeCompare(b))
  }, [questions])

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase()
    return questions.filter((item) => {
      if (themeFilter && (item.theme || '') !== themeFilter) return false
      if (!q) return true
      return (
        item.prompt.toLowerCase().includes(q) ||
        (item.explanation || '').toLowerCase().includes(q) ||
        (item.theme || '').toLowerCase().includes(q)
      )
    })
  }, [questions, themeFilter, search])

  async function saveQuiz(event: FormEvent) {
    event.preventDefault()
    setError('')
    setBusyQuiz(true)
    try {
      const data = await api.updateQuiz(id, {
        title,
        description,
        category,
        is_published: published,
      })
      setQuiz((prev) =>
        prev
          ? {
              ...prev,
              ...data,
              questions: prev.questions,
              question_count: prev.questions?.length ?? data.question_count,
            }
          : data,
      )
      setMessage(t('quizEdit.updated'))
    } catch (err) {
      setError(err instanceof Error ? err.message : t('quizEdit.saveFailed'))
    } finally {
      setBusyQuiz(false)
    }
  }

  async function submitQuestion(payload: QuestionPayload) {
    setError('')
    setBusyQuestion(true)
    try {
      if (editor.kind === 'create') {
        await api.addQuestion(id, payload)
        setMessage(t('quizEdit.created'))
      } else if (editor.kind === 'edit') {
        await api.updateQuestion(editor.questionId, payload)
        setMessage(t('quizEdit.questionUpdated'))
      }
      setEditor({ kind: 'closed' })
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : t('quizEdit.saveQuestionFailed'))
    } finally {
      setBusyQuestion(false)
    }
  }

  async function removeQuestion(questionId: number) {
    if (!confirm(t('quizEdit.confirmDeleteQuestion'))) return
    setError('')
    try {
      await api.deleteQuestion(questionId)
      if (editor.kind === 'edit' && editor.questionId === questionId) {
        setEditor({ kind: 'closed' })
      }
      setMessage(t('quizEdit.questionDeleted'))
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : t('quizEdit.deleteQuestionFailed'))
    }
  }

  function openCreate() {
    setEditor({ kind: 'create', draft: emptyQuestionDraft() })
  }

  function openEdit(question: Question) {
    setEditor({
      kind: 'edit',
      questionId: question.id,
      draft: draftFromQuestion(question),
    })
  }

  if (!quiz) {
    return (
      <div className="shell">
        <header className="topbar">
          <Link to="/" className="brand">
            W<span>Quiz</span> Admin
          </Link>
          <LanguageSwitcher />
        </header>
        <p className="muted">{t('common.loading')}</p>
        {error && <p className="error">{error}</p>}
      </div>
    )
  }

  return (
    <div className="shell shell-wide">
      <header className="topbar">
        <Link to="/" className="brand">
          W<span>Quiz</span> Admin
        </Link>
        <div className="topbar-actions">
          <LanguageSwitcher />
          <Link className="btn btn-ghost" to="/">
            {t('common.back')}
          </Link>
        </div>
      </header>

      {error && <p className="error">{error}</p>}
      {message && <p className="toast">{message}</p>}

      <section className="panel">
        <h1>{t('quizEdit.quizData')}</h1>
        <form className="quiz-meta-form" onSubmit={(e) => void saveQuiz(e)}>
          <div className="meta-grid">
            <div className="field">
              <label htmlFor="title">{t('quizEdit.fieldTitle')}</label>
              <input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                disabled={busyQuiz}
              />
            </div>
            <div className="field">
              <label htmlFor="category">{t('quizEdit.fieldCategory')}</label>
              <input
                id="category"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                disabled={busyQuiz}
              />
            </div>
          </div>
          <div className="field">
            <label htmlFor="description">{t('quizEdit.fieldDescription')}</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={busyQuiz}
            />
          </div>
          <div className="meta-actions">
            <label className="check-inline">
              <input
                type="checkbox"
                checked={published}
                onChange={(e) => setPublished(e.target.checked)}
                disabled={busyQuiz}
              />
              {t('quizEdit.published')}
            </label>
            <button className="btn" type="submit" disabled={busyQuiz}>
              {busyQuiz ? t('common.saving') : t('quizEdit.saveQuiz')}
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="section-head">
          <div>
            <h2>{t('quizEdit.questionsTitle', { count: questions.length })}</h2>
            <p className="muted">
              {filtered.length === questions.length
                ? t('quizEdit.questionsHint')
                : t('quizEdit.questionsFiltered', { count: filtered.length })}
            </p>
          </div>
          <button type="button" className="btn" onClick={openCreate}>
            {t('quizEdit.newQuestion')}
          </button>
        </div>

        <div className="filters">
          <div className="field">
            <label htmlFor="q-search">{t('common.search')}</label>
            <input
              id="q-search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={t('quizEdit.searchPlaceholder')}
            />
          </div>
          <div className="field">
            <label htmlFor="q-theme-filter">{t('common.theme')}</label>
            <select
              id="q-theme-filter"
              value={themeFilter}
              onChange={(e) => setThemeFilter(e.target.value)}
            >
              <option value="">{t('common.all')}</option>
              {themesInQuiz.map((theme) => (
                <option key={theme} value={theme}>
                  {theme}
                </option>
              ))}
            </select>
          </div>
        </div>

        {filtered.length === 0 ? (
          <p className="muted empty-state">{t('quizEdit.emptyFilter')}</p>
        ) : (
          <div className="question-list">
            {filtered.map((question, index) => {
              const open = expandedId === question.id
              const correctCount = question.options.filter((o) => o.is_correct).length
              return (
                <article key={question.id} className="question-card">
                  <div className="question-card-main">
                    <div className="question-card-meta">
                      <span className="q-index">#{index + 1}</span>
                      {question.theme ? (
                        <span className="badge">{question.theme}</span>
                      ) : (
                        <span className="badge off">{t('quizEdit.noTheme')}</span>
                      )}
                      {correctCount > 1 && (
                        <span className="badge">
                          {t('quizEdit.multi', { count: correctCount })}
                        </span>
                      )}
                      <span className="muted">
                        {t('quizEdit.optionsCount', {
                          count: question.options.length,
                        })}
                      </span>
                    </div>
                    <p className="question-card-preview">
                      {promptPreview(question.prompt, 160)}
                    </p>
                    {(() => {
                      const corrects = question.options.filter((o) => o.is_correct)
                      if (corrects.length === 0) return null
                      return (
                        <p className="correct-preview">
                          <strong>
                            {corrects.length > 1
                              ? t('quizEdit.correctMany')
                              : t('quizEdit.correctOne')}
                          </strong>{' '}
                          {corrects
                            .map((c) => c.text.replace(/\s+/g, ' ').slice(0, 80))
                            .join(' · ')}
                          {corrects.some((c) => c.text.length > 80) ? '…' : ''}
                        </p>
                      )
                    })()}
                    {open && (
                      <div className="question-card-detail">
                        <PromptPreview prompt={question.prompt} />
                        {question.explanation && (
                          <p className="muted pre-wrap">{question.explanation}</p>
                        )}
                        {(question.references?.length ?? 0) > 0 && (
                          <ul className="reference-list">
                            {question.references!
                              .slice()
                              .sort((a, b) => a.position - b.position)
                              .map((ref) => (
                                <li key={ref.id ?? ref.url}>
                                  <a
                                    href={ref.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    {ref.label?.trim() || ref.url}
                                  </a>
                                </li>
                              ))}
                          </ul>
                        )}
                        <ul className="option-list">
                          {question.options
                            .slice()
                            .sort((a, b) => a.position - b.position)
                            .map((opt) => (
                              <li
                                key={opt.id ?? `${question.id}-${opt.position}`}
                                className={opt.is_correct ? 'is-correct' : ''}
                              >
                                {opt.is_correct ? '✓ ' : ''}
                                {opt.text}
                              </li>
                            ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  <div className="question-card-actions">
                    <button
                      type="button"
                      className="btn btn-ghost btn-sm"
                      onClick={() => setExpandedId(open ? null : question.id)}
                    >
                      {open ? t('common.hide') : t('common.view')}
                    </button>
                    <button
                      type="button"
                      className="btn btn-ghost btn-sm"
                      onClick={() => openEdit(question)}
                    >
                      {t('common.edit')}
                    </button>
                    <button
                      type="button"
                      className="btn btn-danger btn-sm"
                      onClick={() => void removeQuestion(question.id)}
                    >
                      {t('common.delete')}
                    </button>
                  </div>
                </article>
              )
            })}
          </div>
        )}
      </section>

      {editor.kind !== 'closed' && (
        <div
          className="drawer-backdrop"
          role="presentation"
          onClick={() => !busyQuestion && setEditor({ kind: 'closed' })}
        >
          <aside
            className="drawer-panel"
            role="dialog"
            aria-modal="true"
            aria-labelledby="question-form-title"
            onClick={(e) => e.stopPropagation()}
          >
            <QuestionForm
              title={
                editor.kind === 'create'
                  ? t('quizEdit.createTitle')
                  : t('quizEdit.editTitle')
              }
              initial={editor.draft}
              busy={busyQuestion}
              extraThemes={themesInQuiz}
              onCancel={() => setEditor({ kind: 'closed' })}
              onSubmit={submitQuestion}
            />
          </aside>
        </div>
      )}
    </div>
  )
}
