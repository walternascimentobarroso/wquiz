import { useEffect, useMemo, useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, clearToken, getToken, type Quiz } from '../api'
import { LanguageSwitcher, useI18n } from '../i18n'

export function DashboardPage() {
  const { t } = useI18n()
  const navigate = useNavigate()
  const [quizzes, setQuizzes] = useState<Quiz[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [search, setSearch] = useState('')
  const [createOpen, setCreateOpen] = useState(false)
  const [busy, setBusy] = useState(false)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('Zend PHP')

  async function load() {
    setLoading(true)
    try {
      const data = await api.listQuizzes()
      setQuizzes(data.items)
      setError('')
    } catch (err) {
      const msg = err instanceof Error ? err.message : t('dashboard.listFailed')
      setError(msg)
      if (/401|credenciais|Unauthorized/i.test(msg)) {
        clearToken()
        navigate('/login')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!getToken()) {
      navigate('/login')
      return
    }
    void load()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- boot once on mount
  }, [navigate])

  useEffect(() => {
    if (!message) return
    const timer = window.setTimeout(() => setMessage(''), 2800)
    return () => window.clearTimeout(timer)
  }, [message])

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase()
    if (!q) return quizzes
    return quizzes.filter(
      (quiz) =>
        quiz.title.toLowerCase().includes(q) ||
        quiz.category.toLowerCase().includes(q) ||
        quiz.description.toLowerCase().includes(q),
    )
  }, [quizzes, search])

  async function createQuiz(event: FormEvent) {
    event.preventDefault()
    setError('')
    setBusy(true)
    try {
      const quiz = await api.createQuiz({
        title,
        description,
        category,
        is_published: false,
      })
      setTitle('')
      setDescription('')
      setCategory('Zend PHP')
      setCreateOpen(false)
      navigate(`/quizzes/${quiz.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : t('dashboard.createFailed'))
    } finally {
      setBusy(false)
    }
  }

  async function removeQuiz(id: number) {
    if (!confirm(t('dashboard.confirmDelete'))) return
    try {
      await api.deleteQuiz(id)
      setMessage(t('dashboard.deleted'))
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : t('dashboard.deleteFailed'))
    }
  }

  function logout() {
    clearToken()
    navigate('/login')
  }

  return (
    <div className="shell shell-wide">
      <header className="topbar">
        <div className="brand">
          W<span>Quiz</span> Admin
        </div>
        <div className="topbar-actions">
          <LanguageSwitcher />
          <button type="button" className="btn btn-ghost" onClick={logout}>
            {t('common.logout')}
          </button>
        </div>
      </header>

      {error && <p className="error">{error}</p>}
      {message && <p className="toast">{message}</p>}

      <section className="panel">
        <div className="section-head">
          <div>
            <h1>{t('dashboard.title')}</h1>
            <p className="muted">
              {loading
                ? t('dashboard.loadingList')
                : t('dashboard.quizCount', { count: quizzes.length })}
            </p>
          </div>
          <button type="button" className="btn" onClick={() => setCreateOpen(true)}>
            {t('dashboard.newQuiz')}
          </button>
        </div>

        <div className="filters filters-single">
          <div className="field">
            <label htmlFor="quiz-search">{t('common.search')}</label>
            <input
              id="quiz-search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={t('dashboard.searchPlaceholder')}
            />
          </div>
        </div>

        {!loading && filtered.length === 0 ? (
          <p className="muted empty-state">
            {quizzes.length === 0
              ? t('dashboard.emptyNone')
              : t('dashboard.emptyFilter')}
          </p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>{t('dashboard.colTitle')}</th>
                <th>{t('dashboard.colStatus')}</th>
                <th>{t('dashboard.colQuestions')}</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {filtered.map((quiz) => (
                <tr key={quiz.id}>
                  <td>
                    <Link className="table-link" to={`/quizzes/${quiz.id}`}>
                      {quiz.title}
                    </Link>
                    <div className="muted">{quiz.category}</div>
                  </td>
                  <td>
                    <span className={`badge ${quiz.is_published ? '' : 'off'}`}>
                      {quiz.is_published
                        ? t('dashboard.published')
                        : t('dashboard.draft')}
                    </span>
                  </td>
                  <td>{quiz.question_count}</td>
                  <td>
                    <div className="actions">
                      <Link className="btn btn-ghost btn-sm" to={`/quizzes/${quiz.id}`}>
                        {t('dashboard.manage')}
                      </Link>
                      <button
                        type="button"
                        className="btn btn-danger btn-sm"
                        onClick={() => void removeQuiz(quiz.id)}
                      >
                        {t('common.delete')}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {createOpen && (
        <div
          className="drawer-backdrop"
          role="presentation"
          onClick={() => !busy && setCreateOpen(false)}
        >
          <aside
            className="drawer-panel drawer-panel-sm"
            role="dialog"
            aria-modal="true"
            aria-labelledby="create-quiz-title"
            onClick={(e) => e.stopPropagation()}
          >
            <form onSubmit={(e) => void createQuiz(e)}>
              <div className="drawer-header">
                <h2 id="create-quiz-title">{t('dashboard.newQuiz')}</h2>
                <button
                  type="button"
                  className="btn btn-ghost"
                  disabled={busy}
                  onClick={() => setCreateOpen(false)}
                >
                  {t('common.close')}
                </button>
              </div>
              <div className="field">
                <label htmlFor="new-title">{t('dashboard.fieldTitle')}</label>
                <input
                  id="new-title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  disabled={busy}
                />
              </div>
              <div className="field">
                <label htmlFor="new-category">{t('dashboard.fieldCategory')}</label>
                <input
                  id="new-category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  disabled={busy}
                />
              </div>
              <div className="field">
                <label htmlFor="new-description">{t('dashboard.fieldDescription')}</label>
                <textarea
                  id="new-description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  disabled={busy}
                />
              </div>
              <div className="actions drawer-actions">
                <button
                  type="button"
                  className="btn btn-ghost"
                  disabled={busy}
                  onClick={() => setCreateOpen(false)}
                >
                  {t('common.cancel')}
                </button>
                <button className="btn" type="submit" disabled={busy}>
                  {busy ? t('common.creating') : t('dashboard.createSubmit')}
                </button>
              </div>
            </form>
          </aside>
        </div>
      )}
    </div>
  )
}
