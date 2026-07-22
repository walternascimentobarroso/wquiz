import type { MessageTree, TranslateParams } from './types'

function lookup(tree: MessageTree, path: string): string | undefined {
  const parts = path.split('.')
  let current: string | MessageTree | undefined = tree
  for (const part of parts) {
    if (current == null || typeof current === 'string') return undefined
    current = current[part]
  }
  return typeof current === 'string' ? current : undefined
}

export function translate(
  tree: MessageTree,
  path: string,
  params?: TranslateParams,
): string {
  const template = lookup(tree, path) ?? path
  if (!params) return template
  return template.replace(/\{(\w+)\}/g, (_, key: string) =>
    Object.prototype.hasOwnProperty.call(params, key) ? String(params[key]) : `{${key}}`,
  )
}
