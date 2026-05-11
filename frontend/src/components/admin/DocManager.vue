<template>
  <div class="doc-manager">
    <div class="manager-header">
      <h2 class="manager-title">文档列表</h2>
      <button @click="openEditor()" class="add-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        新建文档
      </button>
    </div>

    <div class="filter-bar">
      <select v-model="categoryFilter" class="filter-select">
        <option value="">全部分类</option>
        <option value="blog">博客</option>
        <option value="docs">文档</option>
      </select>
      <input 
        v-model="searchQuery"
        type="text" 
        placeholder="搜索文档..."
        class="search-input"
      />
    </div>

    <div class="doc-list">
      <div 
        v-for="doc in filteredDocs" 
        :key="doc.id"
        class="doc-item"
        @click="openEditor(doc)"
      >
        <div class="doc-info">
          <h3 class="doc-title">{{ doc.title }}</h3>
          <div class="doc-meta">
            <span class="doc-category">{{ doc.category }}</span>
            <span class="doc-date">{{ formatDate(doc.updated_at) }}</span>
          </div>
          <div v-if="doc.tags?.length" class="doc-tags">
            <span v-for="tag in doc.tags.slice(0, 3)" :key="tag" class="doc-tag">{{ tag }}</span>
          </div>
        </div>
        <div class="doc-actions">
          <button @click.stop="openEditor(doc)" class="action-btn edit">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button @click.stop="deleteDoc(doc.id)" class="action-btn delete">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>

      <div v-if="filteredDocs.length === 0" class="empty-state">
        <p>暂无文档</p>
      </div>
    </div>

    <MarkdownEditor
      v-if="editorOpen"
      :doc="currentDoc"
      @close="closeEditor"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDocsStore } from '@/stores/docs'
import MarkdownEditor from './MarkdownEditor.vue'

const docsStore = useDocsStore()

const categoryFilter = ref('')
const searchQuery = ref('')
const editorOpen = ref(false)
const currentDoc = ref(null)

const filteredDocs = computed(() => {
  return docsStore.documents.filter(doc => {
    const matchCategory = !categoryFilter.value || doc.category === categoryFilter.value
    const matchSearch = !searchQuery.value || 
      doc.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchCategory && matchSearch
  })
})

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const openEditor = (doc = null) => {
  currentDoc.value = doc
  editorOpen.value = true
}

const closeEditor = () => {
  editorOpen.value = false
  currentDoc.value = null
}

const handleSave = async (data) => {
  if (currentDoc.value) {
    await docsStore.updateDoc(currentDoc.value.id, data)
  } else {
    await docsStore.createDoc(data)
  }
  closeEditor()
}

const deleteDoc = async (id) => {
  if (confirm('确定要删除这篇文档吗？')) {
    await docsStore.deleteDoc(id)
  }
}

onMounted(() => {
  docsStore.fetchAllDocs()
})
</script>

<style scoped>
.doc-manager {
  max-width: 1000px;
}

.manager-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.manager-title {
  font-family: 'Fira Code', monospace;
  font-size: 1.25rem;
  color: #E6EDF3;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  border: none;
  border-radius: 8px;
  color: #0A0A0A;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
}

.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #E6EDF3;
  font-size: 0.875rem;
  outline: none;
  cursor: pointer;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #E6EDF3;
  font-size: 0.875rem;
  outline: none;
}

.search-input:focus,
.filter-select:focus {
  border-color: #00FFCC;
}

.doc-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.doc-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem;
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.8), rgba(10, 10, 10, 0.9));
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.doc-item:hover {
  border-color: rgba(0, 255, 204, 0.3);
  transform: translateX(5px);
}

.doc-info {
  flex: 1;
}

.doc-title {
  font-family: 'Fira Code', monospace;
  font-size: 1rem;
  color: #E6EDF3;
  margin-bottom: 0.5rem;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.doc-category {
  padding: 0.25rem 0.5rem;
  background: rgba(0, 255, 204, 0.1);
  border-radius: 4px;
  color: #00FFCC;
  font-size: 0.75rem;
  font-family: 'Fira Code', monospace;
}

.doc-date {
  color: #8B949E;
  font-size: 0.75rem;
}

.doc-tags {
  display: flex;
  gap: 0.5rem;
}

.doc-tag {
  padding: 0.125rem 0.375rem;
  background: rgba(176, 38, 255, 0.1);
  border-radius: 4px;
  color: #B026FF;
  font-size: 0.625rem;
}

.doc-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #8B949E;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.edit:hover {
  color: #00FFCC;
  border-color: #00FFCC;
}

.action-btn.delete:hover {
  color: #FF4757;
  border-color: #FF4757;
}

.empty-state {
  padding: 3rem;
  text-align: center;
  color: #8B949E;
}
</style>
