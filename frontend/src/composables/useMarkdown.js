import { ref, computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

marked.setOptions({
  highlight: (code, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

export function useMarkdown() {
  const renderedContent = ref('')

  const render = (content) => {
    if (!content) {
      renderedContent.value = ''
      return
    }
    renderedContent.value = marked.parse(content)
  }

  const renderAsync = async (content) => {
    return new Promise((resolve) => {
      const result = marked.parse(content || '')
      renderedContent.value = result
      resolve(result)
    })
  }

  return {
    renderedContent,
    render,
    renderAsync
  }
}

export function highlightCode(code, language) {
  if (language && hljs.getLanguage(language)) {
    return hljs.highlight(code, { language }).value
  }
  return hljs.highlightAuto(code).value
}
