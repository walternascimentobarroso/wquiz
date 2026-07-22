export type PromptSegment =
  | { type: 'text'; content: string }
  | { type: 'code'; content: string; lang?: string }

const CODE_LINE =
  /^(<\?php|<\?xml|namespace\s|class\s|function\s|enum\s|\$[a-zA-Z_]|declare\s*\(|\/\/|\/\*|public\s|private\s|protected\s|var_dump\s*\(|echo\s|print(?:f|_r)?\s*\(|include\s|require\s|return\s|new\s|try\s*\{|catch\s*\(|if\s*\(|for(?:each)?\s*\(|while\s*\(|switch\s*\(|array\s*\(|use\s+|move_uploaded_file\s*\(|simplexml_|preg_|str_|file_|json_|unset\s*\(|print_r\s*\()/

const HTML_OR_XML_LINE = /^<\/?[a-zA-Z!][\s\S]*>/

/** Opening ``` or ```lang; closing ``` — optional leading indent. */
const FENCE_LINE = /^\s*```([\w+-]*)\s*$/

function looksLikeCode(block: string): boolean {
  const lines = block
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
  if (lines.length === 0) return false
  if (CODE_LINE.test(lines[0]) || HTML_OR_XML_LINE.test(lines[0])) return true
  const hits = lines.filter(
    (line) => CODE_LINE.test(line) || HTML_OR_XML_LINE.test(line),
  ).length
  return hits >= 2
}

/** Drop leftover Markdown fence marker lines from displayed content. */
function stripFenceMarkers(content: string): string {
  return content
    .split('\n')
    .filter((line) => !FENCE_LINE.test(line))
    .join('\n')
    .replace(/^\n+/, '')
    .replace(/\n+$/, '')
    .trim()
}

function sanitizeSegments(segments: PromptSegment[]): PromptSegment[] {
  const cleaned: PromptSegment[] = []
  for (const segment of segments) {
    const content = stripFenceMarkers(segment.content)
    if (!content) continue
    if (segment.type === 'text') {
      cleaned.push({ type: 'text', content })
    } else {
      cleaned.push(
        segment.lang
          ? { type: 'code', content, lang: segment.lang }
          : { type: 'code', content },
      )
    }
  }
  return cleaned
}

export function parseFencedSegments(prompt: string): PromptSegment[] | null {
  const normalized = prompt.replace(/\r\n/g, '\n')
  if (!normalized.includes('```')) return null

  const lines = normalized.split('\n')
  const segments: PromptSegment[] = []
  let textBuf: string[] = []
  let codeBuf: string[] | null = null
  let lang: string | undefined

  const flushText = () => {
    const content = textBuf.join('\n').trim()
    textBuf = []
    if (content) segments.push({ type: 'text', content })
  }

  const flushCode = () => {
    if (codeBuf == null) return
    const content = codeBuf.join('\n').replace(/^\n+/, '').replace(/\n+$/, '')
    codeBuf = null
    if (content) {
      segments.push(lang ? { type: 'code', content, lang } : { type: 'code', content })
    }
    lang = undefined
  }

  for (const line of lines) {
    const fence = line.match(FENCE_LINE)
    if (codeBuf == null) {
      if (fence) {
        flushText()
        codeBuf = []
        lang = fence[1] || undefined
        continue
      }
      textBuf.push(line)
      continue
    }

    if (fence) {
      flushCode()
      if (fence[1]) {
        codeBuf = []
        lang = fence[1]
      }
      continue
    }
    codeBuf.push(line)
  }

  flushCode()
  flushText()

  return segments.length > 0 ? segments : null
}

export function splitPromptAndCode(prompt: string): {
  text: string
  code: string | null
} {
  const normalized = stripFenceMarkers(prompt.replace(/\r\n/g, '\n')).trim()
  if (!normalized) return { text: '', code: null }

  if (!normalized.includes('\n')) {
    const phpIdx = normalized.search(/<\?php\b/)
    if (phpIdx > 0) {
      return {
        text: normalized.slice(0, phpIdx).trim(),
        code: normalized.slice(phpIdx).trim(),
      }
    }
    return { text: normalized, code: null }
  }

  const lines = normalized.split('\n')
  let codeStart = -1
  for (let i = 0; i < lines.length; i += 1) {
    const trimmed = lines[i].trim()
    if (!trimmed) continue
    if (CODE_LINE.test(trimmed) || HTML_OR_XML_LINE.test(trimmed)) {
      codeStart = i
      break
    }
  }

  if (codeStart < 0) return { text: normalized, code: null }
  if (codeStart === 0) {
    return looksLikeCode(normalized)
      ? { text: '', code: normalized }
      : { text: normalized, code: null }
  }

  const text = lines.slice(0, codeStart).join('\n').trim()
  const code = lines.slice(codeStart).join('\n').replace(/^\n+/, '')
  if (!looksLikeCode(code)) return { text: normalized, code: null }
  return { text, code }
}

export function parsePromptSegments(prompt: string): PromptSegment[] {
  const fenced = parseFencedSegments(prompt)
  if (fenced) return sanitizeSegments(fenced)

  const { text, code } = splitPromptAndCode(prompt)
  const segments: PromptSegment[] = []
  if (text) segments.push({ type: 'text', content: text })
  if (code) segments.push({ type: 'code', content: code })
  if (segments.length === 0 && prompt.trim()) {
    segments.push({ type: 'text', content: stripFenceMarkers(prompt) })
  }
  return sanitizeSegments(segments)
}

export function promptPreview(prompt: string, max = 120): string {
  const segments = parsePromptSegments(prompt)
  const base =
    segments
      .map((s) => s.content)
      .join(' ')
      .replace(/\s+/g, ' ')
      .trim() || prompt
  if (base.length <= max) return base
  return `${base.slice(0, max - 1)}…`
}
