<template>
  <div class="announcements-view">
    <header class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3zm-8.27 4a2 2 0 0 1-3.46 0"/>
          </svg>
          动态通知
        </h1>
        <p class="page-desc">网站更新、项目进展与技术分享</p>
      </div>
      <div class="sse-indicator" :class="sseStatus">
        <span class="sse-dot"></span>
        <span class="sse-text">{{ sseStatusText }}</span>
      </div>
    </header>

    <div class="timeline-container">
      <div class="timeline-line"></div>
      
      <div 
        v-for="(announcement, i) in announcements" 
        :key="announcement.id"
        class="timeline-item"
        :class="{ visible: visibleItems.includes(i) }"
        :style="{ '--delay': `${i * 0.1}s` }"
        @mouseenter="hoveredItem = i"
        @mouseleave="hoveredItem = -1"
      >
        <div class="timeline-dot" :class="announcement.type">
          <svg v-if="announcement.type === 'success'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else-if="announcement.type === 'warning'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <circle cx="12" cy="12" r="4"/>
          </svg>
        </div>

        <div class="timeline-card" :class="{ hovered: hoveredItem === i }">
          <div class="card-header">
            <span class="card-date">{{ formatDate(announcement.created_at) }}</span>
            <span class="card-type" :class="announcement.type">{{ announcement.type }}</span>
          </div>
          <h3 class="card-title">{{ announcement.title }}</h3>
          <p class="card-content">{{ announcement.content }}</p>
          
          <div v-if="announcement.tags?.length" class="card-tags">
            <span v-for="tag in announcement.tags" :key="tag" class="card-tag">{{ tag }}</span>
          </div>
        </div>
      </div>

      <div v-if="announcements.length === 0" class="empty-state">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
          <path d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3zm-8.27 4a2 2 0 0 1-3.46 0"/>
        </svg>
        <p>暂无动态通知</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSSE } from '@/composables/useSSE'

const announcements = ref([])
const visibleItems = ref([])
const hoveredItem = ref(-1)

const { status: sseStatus, data: sseData } = useSSE('/api/announcements/stream', {
  autoConnect: false
})

const sseStatusText = computed(() => {
  const statusMap = {
    connected: '实时同步中',
    connecting: '连接中...',
    error: '连接失败',
    disconnected: '未连接'
  }
  return statusMap[sseStatus.value] || '未知状态'
})

const fetchAnnouncements = async () => {
  try {
    const response = await fetch('/api/announcements')
    const data = await response.json()
    announcements.value = data
    
    data.forEach((_, i) => {
      setTimeout(() => {
        visibleItems.value.push(i)
      }, i * 100)
    })
  } catch (error) {
    console.error('获取公告失败:', error)
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchAnnouncements()
})
</script>

<style scoped>
.announcements-view {
  min-height: 100vh;
  padding: 120px 2rem 4rem;
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-family: 'Fira Code', monospace;
  font-size: 2rem;
  color: #E6EDF3;
  margin-bottom: 0.5rem;
}

.page-title svg {
  color: #00FFCC;
}

.page-desc {
  color: #8B949E;
  font-size: 1rem;
}

.sse-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 20px;
  font-size: 0.75rem;
}

.sse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #8B949E;
}

.sse-indicator.connected .sse-dot {
  background: #00FFCC;
  box-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
  animation: pulse 2s infinite;
}

.sse-indicator.connecting .sse-dot {
  background: #B026FF;
  animation: pulse 1s infinite;
}

.sse-indicator.error .sse-dot {
  background: #FF4757;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.sse-text {
  color: #8B949E;
  font-family: 'Fira Code', monospace;
}

.timeline-container {
  position: relative;
  padding-left: 3rem;
}

.timeline-line {
  position: absolute;
  left: 11px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #00FFCC, #B026FF, transparent);
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateX(-30px);
  transition: all 0.6s ease;
  transition-delay: var(--delay);
}

.timeline-item.visible {
  opacity: 1;
  transform: translateX(0);
}

.timeline-dot {
  position: absolute;
  left: -3rem;
  top: 1rem;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #0D1117;
  border: 2px solid #00FFCC;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00FFCC;
  z-index: 1;
}

.timeline-dot.success {
  border-color: #00FFCC;
  color: #00FFCC;
}

.timeline-dot.warning {
  border-color: #FFB800;
  color: #FFB800;
}

.timeline-dot.info {
  border-color: #B026FF;
  color: #B026FF;
}

.timeline-card {
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.8), rgba(10, 10, 10, 0.9));
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.timeline-card.hovered {
  border-color: rgba(0, 255, 204, 0.3);
  transform: translateX(10px);
  box-shadow: 0 0 30px rgba(0, 255, 204, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.card-date {
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  color: #8B949E;
}

.card-type {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-type.success {
  background: rgba(0, 255, 204, 0.1);
  color: #00FFCC;
  border: 1px solid rgba(0, 255, 204, 0.2);
}

.card-type.warning {
  background: rgba(255, 184, 0, 0.1);
  color: #FFB800;
  border: 1px solid rgba(255, 184, 0, 0.2);
}

.card-type.info {
  background: rgba(176, 38, 255, 0.1);
  color: #B026FF;
  border: 1px solid rgba(176, 38, 255, 0.2);
}

.card-title {
  font-family: 'Fira Code', monospace;
  font-size: 1.125rem;
  color: #E6EDF3;
  margin-bottom: 0.75rem;
}

.card-content {
  color: #8B949E;
  font-size: 0.9375rem;
  line-height: 1.7;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 255, 204, 0.1);
}

.card-tag {
  padding: 0.25rem 0.5rem;
  background: rgba(0, 255, 204, 0.05);
  border-radius: 4px;
  color: #00FFCC;
  font-size: 0.75rem;
  font-family: 'Fira Code', monospace;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #8B949E;
}

.empty-state svg {
  margin-bottom: 1rem;
  opacity: 0.5;
}

@media (max-width: 768px) {
  .announcements-view {
    padding: 100px 1.5rem 3rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
  }

  .timeline-container {
    padding-left: 2.5rem;
  }

  .timeline-dot {
    left: -2.5rem;
    width: 24px;
    height: 24px;
  }
}
</style>
