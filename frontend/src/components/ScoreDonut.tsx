import { useEffect, useState } from 'react'

export type ScoreTone = 'high' | 'mid' | 'low'

type ScoreDonutProps = {
  percentage: number
  correct: number
  wrong: number
  tone: ScoreTone
  label: string
}

const SIZE = 180
const STROKE = 14
const RADIUS = (SIZE - STROKE) / 2
const CIRCUMFERENCE = 2 * Math.PI * RADIUS

export function ScoreDonut({
  percentage,
  correct,
  wrong,
  tone,
  label,
}: ScoreDonutProps) {
  const clamped = Math.min(100, Math.max(0, percentage))
  const targetOffset = CIRCUMFERENCE * (1 - clamped / 100)
  const [offset, setOffset] = useState(CIRCUMFERENCE)
  const display = Math.round(clamped)

  useEffect(() => {
    const frame = requestAnimationFrame(() => setOffset(targetOffset))
    return () => cancelAnimationFrame(frame)
  }, [targetOffset])

  return (
    <div
      className={`score-donut score-tone-${tone}`}
      role="img"
      aria-label={label}
    >
      <svg
        className="score-donut-svg"
        width={SIZE}
        height={SIZE}
        viewBox={`0 0 ${SIZE} ${SIZE}`}
        aria-hidden="true"
      >
        <circle
          className="score-donut-track"
          cx={SIZE / 2}
          cy={SIZE / 2}
          r={RADIUS}
          fill="none"
          strokeWidth={STROKE}
        />
        <circle
          className="score-donut-arc"
          cx={SIZE / 2}
          cy={SIZE / 2}
          r={RADIUS}
          fill="none"
          strokeWidth={STROKE}
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${SIZE / 2} ${SIZE / 2})`}
        />
      </svg>
      <div className="score-donut-center">
        <span className="score-donut-percent">{display}%</span>
        <span className="score-donut-legend">
          <span className="ok-dot" />
          {correct}
          <span className="legend-sep">·</span>
          <span className="bad-dot" />
          {wrong}
        </span>
      </div>
    </div>
  )
}
