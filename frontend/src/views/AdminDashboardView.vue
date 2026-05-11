<template>
  <div class="admin-view">
    <header class="admin-header">
      <div class="header-left">
        <router-link to="/" class="logo">
          <svg width="32" height="32" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="8" fill="#00FFCC"/>
            <circle cx="25" cy="30" r="5" fill="#B026FF"/>
            <circle cx="75" cy="30" r="5" fill="#B026FF"/>
            <line x1="50" y1="50" x2="25" y2="30" stroke="#00FFCC" stroke-width="2"/>
            <line x1="50" y1="50" x2="75" y2="30" stroke="#00FFCC" stroke-width="2"/>
          </svg>
          <span>Admin</span>
        </router-link>
        <span class="header-divider">/</span>
        <span class="current-page">{{ activeTab }}</span>
      </div>
      
      <div class="header-right">
        <router-link to="/" class="preview-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15 3 21 3 21 9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
          查看站点
        </router-link>
        <button @click="handleLogout" class="logout-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          退出
        </button>
      </div>
    </header>

    <div class="admin-container">
      <nav class="admin-tabs">
        <button 
          v-for="tab in tabs"
          :key="tab.id"
          class="tab-btn"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          <component :is="tab.icon" />
          <span>{{ tab.label }}</span>
        </button>
      </nav>

      <main class="admin-content">
        <component :is="currentComponent" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DocManager from '@/components/admin/DocManager.vue'
import AnnouncementManager from '@/components/admin/AnnouncementManager.vue'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('docs')

const DocsIcon = () => h('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
  h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
  h('polyline', { points: '14 2 14 8 20 8' })
])

const BellIcon = () => h('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
  h('path', { d: 'M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9' }),
  h('path', { d: 'M13.73 21a2 2 0 0 1-3.46 0' })
])

const tabs = [
  { id: 'docs', label: '文档管理', icon: DocsIcon },
  { id: 'announcements', label: '公告管理', icon: BellIcon }
]

const currentComponent = computed(() => {
  const components = {
    docs: DocManager,
    announcements: AnnouncementManager
  }
  return components[activeTab.value]
})

const handleLogout = () => {
  authStore.logout()
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-view {
  min-height: 100vh;
  background: #0A0A0A;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(13, 17, 23, 0.95);
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #E6EDF3;
  font-family: 'Fira Code', monospace;
  font-weight: 600;
}

.header-divider {
  color: #8B949E;
}

.current-page {
  color: #00FFCC;
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.preview-btn,
.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 6px;
  color: #8B949E;
  font-size: 0.875rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preview-btn:hover {
  color: #00FFCC;
  border-color: #00FFCC;
}

.logout-btn:hover {
  color: #FF4757;
  border-color: #FF4757;
}

.admin-container {
  display: flex;
  min-height: calc(100vh - 60px);
}

.admin-tabs {
  width: 220px;
  padding: 1.5rem;
  border-right: 1px solid rgba(0, 255, 204, 0.1);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: #8B949E;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.tab-btn:hover {
  color: #E6EDF3;
  background: rgba(0, 255, 204, 0.05);
}

.tab-btn.active {
  color: #00FFCC;
  background: rgba(0, 255, 204, 0.1);
}

.admin-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .admin-container {
    flex-direction: column;
  }

  .admin-tabs {
    width: 100%;
    flex-direction: row;
    border-right: none;
    border-bottom: 1px solid rgba(0, 255, 204, 0.1);
    overflow-x: auto;
  }

  .tab-btn {
    flex-shrink: 0;
  }
}
</style>
