export type Locale = 'en' | 'pt'

export type TranslateParams = Record<string, string | number>

export type MessageTree = {
  [key: string]: string | MessageTree
}
