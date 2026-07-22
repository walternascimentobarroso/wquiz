import type { Locale } from './types'

export const LOCALE_STORAGE_KEY = 'wquiz_locale'

export function isLocale(value: string | null | undefined): value is Locale {
  return value === 'en' || value === 'pt'
}

/** Prefer saved choice; otherwise map the browser language to en/pt. */
export function detectLocale(): Locale {
  if (typeof window === 'undefined') return 'en'
  try {
    const stored = window.localStorage.getItem(LOCALE_STORAGE_KEY)
    if (isLocale(stored)) return stored
  } catch {
    // ignore storage failures
  }
  const candidates = [
    navigator.language,
    ...(navigator.languages ?? []),
  ]
  for (const tag of candidates) {
    const lower = tag.toLowerCase()
    if (lower.startsWith('pt')) return 'pt'
    if (lower.startsWith('en')) return 'en'
  }
  return 'en'
}

export function htmlLang(locale: Locale): string {
  return locale === 'pt' ? 'pt-BR' : 'en'
}
