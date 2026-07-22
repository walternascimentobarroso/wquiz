import { parsePromptSegments } from '../utils/promptCode'

type PromptPreviewProps = {
  prompt: string
  compact?: boolean
}

export function PromptPreview({ prompt, compact = false }: PromptPreviewProps) {
  const segments = parsePromptSegments(prompt)

  return (
    <div className={`prompt-preview${compact ? ' prompt-preview-compact' : ''}`}>
      {segments.map((segment, index) =>
        segment.type === 'text' ? (
          <p key={`t-${index}`} className="prompt-preview-text">
            {segment.content}
          </p>
        ) : (
          <pre key={`c-${index}`} className="prompt-preview-code">
            <code>{segment.content}</code>
          </pre>
        ),
      )}
    </div>
  )
}
