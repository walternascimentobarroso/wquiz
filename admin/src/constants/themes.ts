/** Official Zend PHP Certification Exam topics. */
export const ZEND_THEMES = [
  'PHP Basics',
  'Functions',
  'Data Format and Types',
  'Web Features',
  'Object-Oriented Programming',
  'Security',
  'I/O',
  'Strings and Patterns',
  'Databases and SQLs',
  'Arrays',
  'Error Handling',
  'Other PHP Concepts',
] as const

export type ZendTheme = (typeof ZEND_THEMES)[number]
