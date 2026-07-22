const API_BASE = import.meta.env.VITE_API_URL ?? ''

const TOKEN_KEY = 'wquiz_admin_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken()
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers ?? {}),
    },
  })
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Erro na requisição' }))
    const detail = err.detail
    throw new Error(
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((d: { msg?: string }) => d.msg).join(', ')
          : 'Erro na requisição',
    )
  }
  return response.json() as Promise<T>
}

export type Quiz = {
  id: number
  title: string
  description: string
  category: string
  is_published: boolean
  question_count: number
  questions?: Question[]
}

export type QuestionReference = {
  id?: number
  url: string
  label: string
  position: number
}

export type Question = {
  id: number
  prompt: string
  explanation: string
  theme: string
  position: number
  options: { id?: number; text: string; is_correct: boolean; position: number }[]
  references?: QuestionReference[]
}

export type QuestionPayload = {
  prompt: string
  explanation: string
  theme?: string
  position?: number
  options: { text: string; is_correct: boolean; position: number }[]
  references?: { url: string; label: string; position: number }[]
}

export const api = {
  login: async (email: string, password: string) => {
    const data = await request<{ access_token: string }>('/api/auth/token', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    setToken(data.access_token)
    return data
  },
  me: () => request<{ email: string; full_name: string; role: string }>('/api/auth/me'),
  listQuizzes: () => request<{ items: Quiz[]; count: number }>('/api/admin/quizzes'),
  getQuiz: (id: number) => request<Quiz>(`/api/admin/quizzes/${id}`),
  createQuiz: (body: {
    title: string
    description: string
    category: string
    is_published: boolean
  }) =>
    request<Quiz>('/api/admin/quizzes', {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  updateQuiz: (
    id: number,
    body: Partial<{
      title: string
      description: string
      category: string
      is_published: boolean
    }>,
  ) =>
    request<Quiz>(`/api/admin/quizzes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(body),
    }),
  deleteQuiz: (id: number) =>
    request<{ deleted: boolean }>(`/api/admin/quizzes/${id}`, { method: 'DELETE' }),
  addQuestion: (quizId: number, body: QuestionPayload) =>
    request<Question>(`/api/admin/quizzes/${quizId}/questions`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  updateQuestion: (questionId: number, body: Partial<QuestionPayload>) =>
    request<Question>(`/api/admin/questions/${questionId}`, {
      method: 'PUT',
      body: JSON.stringify(body),
    }),
  deleteQuestion: (questionId: number) =>
    request<{ deleted: boolean }>(`/api/admin/questions/${questionId}`, {
      method: 'DELETE',
    }),
}
