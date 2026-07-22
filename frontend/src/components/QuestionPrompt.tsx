import { parsePromptSegments } from '../utils/promptCode'

type QuestionPromptProps = {
  prompt: string
  compact?: boolean
}

export function QuestionPrompt({ prompt, compact = false }: QuestionPromptProps) {
  const segments = parsePromptSegments(prompt)

  // Always a div: prompts mix <p> and <pre>, which must not nest inside <h1>.
  return (
    <div
      className={`question-prompt${compact ? ' question-prompt-compact' : ''}`}
      role="group"
    >
      {segments.map((segment, index) =>
        segment.type === 'text' ? (
          <p key={`t-${index}`} className="prompt-text">
            {segment.content}
          </p>
        ) : (
          <pre
            key={`c-${index}`}
            className="prompt-code"
            tabIndex={0}
            data-lang={segment.lang || undefined}
          >
            <code>{segment.content}</code>
          </pre>
        ),
      )}
    </div>
  )
}
