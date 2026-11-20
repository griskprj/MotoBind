import { marked } from 'marked'

export function useMarkdown() {
  marked.use({
    breaks: true,
    gfm: true,
  })

  function render(text: string | null | undefined): string {
    if (!text) return ''
    return marked.parse(text, { async: false }) as string
  }

  return { render }
}
