export const DEFAULT_TIME_LIMIT_SECONDS = 120 * 60

export function formatDuration(totalSeconds: number): string {
  const safe = Math.max(0, Math.floor(totalSeconds))
  const hours = Math.floor(safe / 3600)
  const minutes = Math.floor((safe % 3600) / 60)
  const seconds = safe % 60
  const hh = String(hours).padStart(2, '0')
  const mm = String(minutes).padStart(2, '0')
  const ss = String(seconds).padStart(2, '0')
  return `${hh}:${mm}:${ss}`
}

/** @deprecated use formatDuration */
export function formatElapsed(totalSeconds: number): string {
  return formatDuration(totalSeconds)
}

export function remainingSeconds(
  startedAtMs: number,
  limitSeconds: number,
  nowMs = Date.now(),
): number {
  const elapsed = Math.max(0, Math.floor((nowMs - startedAtMs) / 1000))
  return Math.max(0, limitSeconds - elapsed)
}
