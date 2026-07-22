import { useI18n } from './I18nContext'
import type { Locale } from './types'

const OPTIONS: { id: Locale; label: string }[] = [
  { id: 'en', label: 'EN' },
  { id: 'pt', label: 'PT' },
]

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useI18n()

  return (
    <div className="lang-switch" role="group" aria-label={t('common.language')}>
      {OPTIONS.map((option) => (
        <button
          key={option.id}
          type="button"
          className={`lang-btn${locale === option.id ? ' lang-btn-active' : ''}`}
          aria-pressed={locale === option.id}
          onClick={() => setLocale(option.id)}
        >
          {option.label}
        </button>
      ))}
    </div>
  )
}
