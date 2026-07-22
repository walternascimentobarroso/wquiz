import { useI18n } from '../i18n'

type FinishModalProps = {
  remaining: number
  total: number
  busy?: boolean
  onCancel: () => void
  onConfirm: () => void
}

export function FinishModal({
  remaining,
  total,
  busy = false,
  onCancel,
  onConfirm,
}: FinishModalProps) {
  const { t } = useI18n()
  const answered = Math.max(0, total - remaining)

  return (
    <div className="modal-backdrop" role="presentation" onClick={onCancel}>
      <div
        className="modal-panel"
        role="dialog"
        aria-modal="true"
        aria-labelledby="finish-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 id="finish-modal-title">{t('finishModal.title')}</h2>
        <p>{t('finishModal.body', { answered, total, remaining })}</p>
        <p className="muted">{t('finishModal.ask')}</p>
        <div className="actions">
          <button type="button" className="btn btn-ghost" disabled={busy} onClick={onCancel}>
            {t('finishModal.continue')}
          </button>
          <button type="button" className="btn btn-danger" disabled={busy} onClick={onConfirm}>
            {t('finishModal.finishAnyway')}
          </button>
        </div>
      </div>
    </div>
  )
}
