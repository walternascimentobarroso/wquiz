import { useEffect, useRef, useState } from 'react'
import { DEFAULT_TIME_LIMIT_SECONDS, formatDuration } from '../utils/time'

type UseCountdownOptions = {
  /** Segundos restantes no momento em que a âncora foi definida */
  initialRemaining?: number | null
  limitSeconds?: number
  running?: boolean
  onExpire?: () => void
}

/**
 * Contagem regressiva. Padrão: 120 minutos.
 */
export function useSessionTimer({
  initialRemaining,
  limitSeconds = DEFAULT_TIME_LIMIT_SECONDS,
  running = true,
  onExpire,
}: UseCountdownOptions) {
  const [secondsLeft, setSecondsLeft] = useState(
    () => initialRemaining ?? limitSeconds,
  )
  const anchorRef = useRef<{ atMs: number; remaining: number } | null>(null)
  const expiredRef = useRef(false)

  useEffect(() => {
    const remaining = initialRemaining ?? limitSeconds
    anchorRef.current = { atMs: Date.now(), remaining }
    expiredRef.current = false
    setSecondsLeft(Math.max(0, remaining))
  }, [initialRemaining, limitSeconds])

  useEffect(() => {
    const tick = () => {
      const anchor = anchorRef.current
      if (!anchor) {
        setSecondsLeft(limitSeconds)
        return
      }
      const elapsed = Math.floor((Date.now() - anchor.atMs) / 1000)
      const left = Math.max(0, anchor.remaining - elapsed)
      setSecondsLeft(left)
      if (left <= 0 && !expiredRef.current) {
        expiredRef.current = true
        onExpire?.()
      }
    }

    tick()
    if (!running) return

    const id = window.setInterval(tick, 250)
    return () => window.clearInterval(id)
  }, [limitSeconds, running, onExpire, initialRemaining])

  return {
    secondsLeft,
    label: formatDuration(secondsLeft),
    isExpired: secondsLeft <= 0,
    isLow: secondsLeft > 0 && secondsLeft <= 5 * 60,
  }
}
