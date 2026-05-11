<template>
  <div class="docs-view">
    <aside class="docs-sidebar" :class="{ 'sidebar-open': sidebarOpen }">
      <div class="sidebar-header">
        <h2 class="sidebar-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          文档中心
        </h2>
        <button class="sidebar-close" @click="sidebarOpen = false">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="sidebar-search">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="搜索文档..."
          class="search-input"
        />
      </div>

      <nav class="sidebar-nav">
        <div v-for="category in filteredDocs" :key="category.name" class="nav-category">
          <button 
            class="category-btn"
            @click="toggleCategory(category.name)"
          >
            <span>{{ category.name }}</span>
            <svg 
              class="category-arrow" 
              :class="{ expanded: expandedCategories.includes(category.name) }"
              width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            >
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </button>
          
          <div 
            v-show="expandedCategories.includes(category.name)"
            class="category-items"
          >
            <router-link
              v-for="doc in category.docs"
              :key="doc.slug"
              :to="`/docs/${doc.slug}`"
              class="doc-link"
              :class="{ active: currentSlug === doc.slug }"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              {{ doc.title }}
            </router-link>
          </div>
        </div>
      </nav>
    </aside>

    <main class="docs-main">
      <button class="mobile-sidebar-btn" @click="sidebarOpen = true">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <article v-else-if="currentDoc" class="doc-content">
        <header class="doc-header">
          <div class="doc-breadcrumb">
            <router-link to="/docs">文档</router-link>
            <span class="separator">/</span>
            <span class="current">{{ currentDoc.title }}</span>
          </div>
          <h1 class="doc-title">{{ currentDoc.title }}</h1>
          <div class="doc-meta">
            <span v-if="currentDoc.category" class="meta-tag">{{ currentDoc.category }}</span>
            <span class="meta-date">{{ formatDate(currentDoc.updated_at) }}</span>
          </div>
          <div v-if="currentDoc.tags?.length" class="doc-tags">
            <span v-for="tag in currentDoc.tags" :key="tag" class="doc-tag">{{ tag }}</span>
          </div>
        </header>

        <div 
          class="markdown-body"
          v-html="renderedContent"
        ></div>

        <footer class="doc-footer">
          <div class="footer-nav">
            <router-link v-if="prevDoc" :to="`/docs/${prevDoc.slug}`" class="nav-btn prev">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="19" y1="12" x2="5" y2="12"/>
                <polyline points="12 19 5 12 12 5"/>
              </svg>
              <span>{{ prevDoc.title }}</span>
            </router-link>
            <router-link v-if="nextDoc" :to="`/docs/${nextDoc.slug}`" class="nav-btn next">
              <span>{{ nextDoc.title }}</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </router-link>
          </div>
        </footer>
      </article>

      <div v-else class="empty-state">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
        <h3>选择一个文档开始阅读</h3>
        <p>从左侧边栏选择文档，或使用搜索功能</p>
      </div>
    </main>

    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay" 
      @click="sidebarOpen = false"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDocsStore } from '@/stores/docs'
import { useMarkdown } from '@/composables/useMarkdown'

const route = useRoute()
const docsStore = useDocsStore()
const { renderedContent, render } = useMarkdown()

const sidebarOpen = ref(false)
const searchQuery = ref('')
const expandedCategories = ref(['博客', '文档'])
const loading = computed(() => docsStore.loading)

const currentSlug = computed(() => route.params.slug)

const currentDoc = computed(() => {
  if (!currentSlug.value) return null
  return docsStore.documents.find(d => d.slug === currentSlug.value)
})

const filteredDocs = computed(() => {
  const categories = {}
  docsStore.documents.forEach(doc => {
    const cat = doc.category || '未分类'
    if (!categories[cat]) categories[cat] = { name: cat, docs: [] }
    
    if (!searchQuery.value || 
        doc.title.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      categories[cat].docs.push(doc)
    }
  })
  return Object.values(categories)
})

const prevDoc = computed(() => {
  if (!currentDoc.value) return null
  const docs = docsStore.documents
  const idx = docs.findIndex(d => d.slug === currentSlug.value)
  return idx > 0 ? docs[idx - 1] : null
})

const nextDoc = computed(() => {
  if (!currentDoc.value) return null
  const docs = docsStore.documents
  const idx = docs.findIndex(d => d.slug === currentSlug.value)
  return idx < docs.length - 1 ? docs[idx + 1] : null
})

const toggleCategory = (name) => {
  const idx = expandedCategories.value.indexOf(name)
  if (idx === -1) {
    expandedCategories.value.push(name)
  } else {
    expandedCategories.value.splice(idx, 1)
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

watch(() => currentDoc.value, (doc) => {
  if (doc) {
    render(doc.content)
    docsStore.currentDoc = doc
  }
}, { immediate: true })

onMounted(async () => {
  await docsStore.fetchAllDocs()
})
</script>

<style scoped>
.docs-view {
  display: flex;
  min-height: 100vh;
  padding-top: 60px;
}

.docs-sidebar {
  width: 280px;
  height: calc(100vh - 60px);
  position: fixed;
  left: 0;
  top: 60px;
  background: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(12px);
  border-right: 1px solid rgba(0, 255, 204, 0.1);
  overflow-y: auto;
  z-index: 100;
  transition: transform 0.3s ease;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Fira Code', monospace;
  font-size: 1rem;
  color: #E6EDF3;
}

.sidebar-close {
  display: none;
  background: none;
  border: none;
  color: #8B949E;
  cursor: pointer;
}

.sidebar-search {
  padding: 1rem 1.5rem;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 2.5rem;
  top: 50%;
  transform: translateY(-50%);
  color: #8B949E;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #E6EDF3;
  font-size: 0.875rem;
  outline: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #00FFCC;
  box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
}

.search-input::placeholder {
  color: #8B949E;
}

.sidebar-nav {
  padding: 0.5rem 0;
}

.nav-category {
  margin-bottom: 0.25rem;
}

.category-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  color: #8B949E;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-btn:hover {
  color: #E6EDF3;
  background: rgba(0, 255, 204, 0.05);
}

.category-arrow {
  transition: transform 0.3s ease;
}

.category-arrow.expanded {
  transform: rotate(180deg);
}

.category-items {
  padding: 0.25rem 0;
}

.doc-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.5rem 0.625rem 2.5rem;
  color: #8B949E;
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.doc-link:hover {
  color: #E6EDF3;
  background: rgba(0, 255, 204, 0.05);
}

.doc-link.active {
  color: #00FFCC;
  background: rgba(0, 255, 204, 0.1);
  border-right: 2px solid #00FFCC;
}

.docs-main {
  flex: 1;
  margin-left: 280px;
  padding: 3rem;
  min-height: calc(100vh - 60px);
}

.mobile-sidebar-btn {
  display: none;
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00FFCC, #B026FF);
  border: none;
  color: #0A0A0A;
  cursor: pointer;
  z-index: 101;
  box-shadow: 0 4px 20px rgba(0, 255, 204, 0.3);
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: #8B949E;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 255, 204, 0.1);
  border-top-color: #00FFCC;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state svg {
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.empty-state h3 {
  color: #E6EDF3;
  margin-bottom: 0.5rem;
}

.doc-content {
  max-width: 800px;
  margin: 0 auto;
}

.doc-header {
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
}

.doc-breadcrumb {
  font-size: 0.875rem;
  color: #8B949E;
  margin-bottom: 1rem;
}

.doc-breadcrumb a {
  color: #00FFCC;
  text-decoration: none;
}

.doc-breadcrumb a:hover {
  text-decoration: underline;
}

.separator {
  margin: 0 0.5rem;
}

.doc-title {
  font-family: 'Fira Code', monospace;
  font-size: 2.5rem;
  color: #E6EDF3;
  margin-bottom: 1rem;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.meta-tag {
  padding: 0.25rem 0.75rem;
  background: rgba(0, 255, 204, 0.1);
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 4px;
  color: #00FFCC;
  font-size: 0.75rem;
  font-family: 'Fira Code', monospace;
}

.meta-date {
  color: #8B949E;
  font-size: 0.875rem;
}

.doc-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.doc-tag {
  padding: 0.25rem 0.5rem;
  background: rgba(176, 38, 255, 0.1);
  border-radius: 4px;
  color: #B026FF;
  font-size: 0.75rem;
}

.doc-footer {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 255, 204, 0.1);
}

.footer-nav {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #E6EDF3;
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  border-color: #00FFCC;
  background: rgba(0, 255, 204, 0.1);
}

.nav-btn.prev {
  flex: 0 0 auto;
}

.nav-btn.next {
  flex: 0 0 auto;
  margin-left: auto;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
}

@media (max-width: 968px) {
  .docs-sidebar {
    transform: translateX(-100%);
  }

  .docs-sidebar.sidebar-open {
    transform: translateX(0);
  }

  .sidebar-close {
    display: block;
  }

  .docs-main {
    margin-left: 0;
    padding: 2rem;
  }

  .mobile-sidebar-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .sidebar-overlay {
    display: block;
  }
}
</style>
