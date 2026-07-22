import { useI18n } from '../i18n'

export type QuestionReferenceLink = {
  id?: number
  url: string
  label?: string
  position?: number
}

type ReferenceLinksProps = {
  references?: QuestionReferenceLink[] | null
  className?: string
}

function fallbackLabel(url: string): string {
  try {
    const host = new URL(url).hostname.replace(/^www\./, '')
    return host || url
  } catch {
    return url
  }
}

export function ReferenceLinks({ references, className = '' }: ReferenceLinksProps) {
  const { t } = useI18n()
  const items = (references ?? [])
    .filter((ref) => Boolean(ref?.url?.trim()))
    .slice()
    .sort((a, b) => (a.position ?? 0) - (b.position ?? 0))

  if (items.length === 0) return null

  return (
    <div className={`reference-links ${className}`.trim()}>
      <p className="reference-links-title">{t('session.references')}</p>
      <ul>
        {items.map((ref) => {
          const label = ref.label?.trim() || fallbackLabel(ref.url)
          return (
            <li key={ref.id ?? ref.url}>
              <a href={ref.url} target="_blank" rel="noopener noreferrer">
                {label}
              </a>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
