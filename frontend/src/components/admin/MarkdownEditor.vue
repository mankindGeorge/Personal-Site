<template>
  <div class="editor-overlay" @click.self="$emit('close')">
    <div class="editor-container">
      <div class="editor-header">
        <h3>{{ doc ? '编辑文档' : '新建文档' }}</h3>
        <button @click="$emit('close')" class="close-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="editor-body">
        <div class="editor-settings">
          <div class="form-group">
            <label>标题</label>
            <input v-model="formData.title" type="text" placeholder="文档标题" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Slug</label>
              <input v-model="formData.slug" type="text" placeholder="url-slug" />
            </div>
            <div class="form-group">
              <label>分类</label>
              <select v-model="formData.category">
                <option value="blog">博客</option>
                <option value="docs">文档</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>标签 (逗号分隔)</label>
            <input v-model="tagsInput" type="text" placeholder="Python, API, 教程" />
          </div>
        </div>

        <div class="editor-content">
          <div class="editor-panes">
            <div class="editor-pane">
              <div class="pane-header">
                <span>Markdown</span>
                <button @click="insertTemplate" class="template-btn">插入模板</button>
              </div>
              <textarea 
                v-model="formData.content"
                class="markdown-input"
                placeholder="# 标题&#10;&#10;内容..."
              ></textarea>
            </div>

            <div class="editor-pane">
              <div class="pane-header">
                <span>预览</span>
              </div>
              <div 
                class="markdown-preview markdown-body"
                v-html="previewContent"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div class="editor-footer">
        <button @click="$emit('close')" class="cancel-btn">取消</button>
        <button @click="handleSave" class="save-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
            <polyline points="17 21 17 13 7 13 7 21"/>
            <polyline points="7 3 7 8 15 8"/>
          </svg>
          保存
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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

const props = defineProps({
  doc: Object
})

const emit = defineEmits(['close', 'save'])

const formData = ref({
  title: '',
  slug: '',
  category: 'blog',
  content: '',
  tags: []
})

const tagsInput = ref('')

const previewContent = computed(() => {
  if (!formData.value.content) return '<p style="color: #8B949E;">预览区域</p>'
  return marked.parse(formData.value.content)
})

watch(() => props.doc, (doc) => {
  if (doc) {
    formData.value = { ...doc }
    tagsInput.value = doc.tags?.join(', ') || ''
  }
}, { immediate: true })

const generateSlug = (title) => {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
    .replace(/^-|-$/g, '')
}

watch(() => formData.value.title, (title) => {
  if (!props.doc && title) {
    formData.value.slug = generateSlug(title)
  }
})

const insertTemplate = () => {
  const template = `## 概述

简要介绍本文档的内容。

## 前置条件

- 条件 1
- 条件 2

## 步骤

### 第一步

详细说明...

### 第二步

详细说明...

## 代码示例

\`\`\`python
def example():
    print("Hello, World!")
\`\`\`

## 总结

总结内容...
`
  formData.value.content = template
}

const handleSave = () => {
  const tags = tagsInput.value
    .split(',')
    .map(t => t.trim())
    .filter(t => t)

  emit('save', {
    ...formData.value,
    tags
  })
}
</script>

<style scoped>
.editor-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.editor-container {
  width: 100%;
  max-width: 1200px;
  height: 90vh;
  background: #0D1117;
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
}

.editor-header h3 {
  font-family: 'Fira Code', monospace;
  color: #E6EDF3;
}

.close-btn {
  background: none;
  border: none;
  color: #8B949E;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #E6EDF3;
}

.editor-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-settings {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #8B949E;
  font-size: 0.875rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #E6EDF3;
  font-size: 0.9375rem;
  outline: none;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #00FFCC;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.editor-content {
  flex: 1;
  padding: 1.5rem;
  overflow: hidden;
}

.editor-panes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  height: 100%;
}

.editor-pane {
  display: flex;
  flex-direction: column;
  background: rgba(10, 10, 10, 0.5);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 12px;
  overflow: hidden;
}

.pane-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: rgba(0, 255, 204, 0.05);
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  color: #8B949E;
}

.template-btn {
  padding: 0.25rem 0.75rem;
  background: rgba(0, 255, 204, 0.1);
  border: none;
  border-radius: 4px;
  color: #00FFCC;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.template-btn:hover {
  background: rgba(0, 255, 204, 0.2);
}

.markdown-input {
  flex: 1;
  padding: 1rem;
  background: transparent;
  border: none;
  color: #E6EDF3;
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
  line-height: 1.7;
  resize: none;
  outline: none;
}

.markdown-preview {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.editor-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid rgba(0, 255, 204, 0.1);
}

.cancel-btn,
.save-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: transparent;
  border: 1px solid rgba(0, 255, 204, 0.2);
  color: #8B949E;
}

.cancel-btn:hover {
  border-color: #E6EDF3;
  color: #E6EDF3;
}

.save-btn {
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  border: none;
  color: #0A0A0A;
}

.save-btn:hover {
  box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
}

@media (max-width: 968px) {
  .editor-panes {
    grid-template-columns: 1fr;
  }
}
</style>
