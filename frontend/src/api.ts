const API_BASE = import.meta.env.VITE_API_URL ?? ''

export type HateoasLink = {
  href: string
  method?: string
}

export type QuizSummary = {
  id: number
  title: string
  description: string
  category: string
  question_count: number
  themes?: { name: string; question_count: number }[]
  modes?: string[]
  _links?: Record<string, HateoasLink>
}

export type Session = {
  id: number
  quiz_id: number
  mode: 'practice' | 'study' | 'flashcard'
  status: string
  current_index: number
  score: number
  total_questions: number
  created_at?: string | null
  completed_at?: string | null
  time_limit_seconds?: number
  expires_at?: string | null
  remaining_seconds?: number
  _links?: Record<string, HateoasLink>
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Erro na requisição' }))
    throw new Error(err.detail ?? 'Erro na requisição')
  }
  return response.json() as Promise<T>
}

export const api = {
  listQuizzes: () =>
    request<{ items: QuizSummary[]; count: number }>('/api/quizzes'),
  getQuiz: (id: number) => request<QuizSummary>(`/api/quizzes/${id}`),
  startSession: (
    quizId: number,
    mode: Session['mode'],
    options?: { questionCount?: number; timeLimitMinutes?: number; theme?: string },
  ) =>
    request<Session>('/api/sessions', {
      method: 'POST',
      body: JSON.stringify({
        quiz_id: quizId,
        mode,
        question_count: options?.questionCount,
        time_limit_minutes: options?.timeLimitMinutes,
        theme: options?.theme,
      }),
    }),
  getSession: (id: number) => request<Session>(`/api/sessions/${id}`),
  getCurrent: (sessionId: number) =>
    request<Record<string, unknown>>(`/api/sessions/${sessionId}/current`),
  submitAnswer: (sessionId: number, questionId: number, optionIds: number[]) =>
    request<Record<string, unknown>>(`/api/sessions/${sessionId}/answers`, {
      method: 'POST',
      body: JSON.stringify({
        question_id: questionId,
        option_ids: optionIds,
        option_id: optionIds[0],
      }),
    }),
  revealFlashcard: (sessionId: number, flashcardId: number) =>
    request<{
      id: number
      front: string
      back: string
      references?: { id: number; url: string; label: string; position: number }[]
    }>(`/api/sessions/${sessionId}/flashcards/${flashcardId}`),
  reviewFlashcard: (
    sessionId: number,
    flashcardId: number,
    rating: 'again' | 'hard' | 'good' | 'easy',
  ) =>
    request<Record<string, unknown>>(`/api/sessions/${sessionId}/flashcard-reviews`, {
      method: 'POST',
      body: JSON.stringify({ flashcard_id: flashcardId, rating }),
    }),
  getResult: (sessionId: number) =>
    request<Record<string, unknown>>(`/api/sessions/${sessionId}/result`),
  goPrevious: (sessionId: number) =>
    request<Session>(`/api/sessions/${sessionId}/previous`, { method: 'POST' }),
  goNext: (sessionId: number) =>
    request<Session>(`/api/sessions/${sessionId}/next`, { method: 'POST' }),
  finishSession: (sessionId: number, force = false) =>
    request<{
      session_completed: boolean
      needs_confirmation: boolean
      remaining: number
      answered?: number
      total_questions?: number
    }>(`/api/sessions/${sessionId}/finish`, {
      method: 'POST',
      body: JSON.stringify({ force }),
    }),
}
