<template>
  <section class="tech-stack" id="about">
    <div class="section-header">
      <h2 class="section-title">
        <span class="title-accent">//</span> Tech Stack
      </h2>
      <p class="section-desc">我使用的技术栈</p>
    </div>

    <div class="tech-grid" ref="gridRef">
      <div 
        v-for="(category, i) in techCategories" 
        :key="category.name"
        class="tech-category"
        :class="{ visible: isVisible }"
        :style="{ '--delay': `${i * 0.1}s` }"
      >
        <div class="category-header">
          <component :is="category.icon" class="category-icon" />
          <h3 class="category-name">{{ category.name }}</h3>
        </div>
        
        <div class="tech-items">
          <div 
            v-for="tech in category.items" 
            :key="tech.name"
            class="tech-item"
          >
            <div class="tech-icon-wrapper">
              <span class="tech-icon">{{ tech.emoji }}</span>
            </div>
            <div class="tech-info">
              <span class="tech-name">{{ tech.name }}</span>
              <div class="tech-bar">
                <div 
                  class="tech-bar-fill" 
                  :style="{ width: isVisible ? tech.level + '%' : '0%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'

const { isVisible, elementRef } = { isVisible: ref(false) }
const gridRef = ref(null)

const FrontendIcon = () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
  h('polyline', { points: '16 18 22 12 16 6' }),
  h('polyline', { points: '8 6 2 12 8 18' })
])

const BackendIcon = () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
  h('rect', { x: 2, y: 3, width: 20, height: 14, rx: 2, ry: 2 }),
  h('line', { x1: 8, y1: 21, x2: 16, y2: 21 }),
  h('line', { x1: 12, y1: 17, x2: 12, y2: 21 })
])

const DataIcon = () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
  h('line', { x1: 18, y1: 20, x2: 18, y2: 10 }),
  h('line', { x1: 12, y1: 20, x2: 12, y2: 4 }),
  h('line', { x1: 6, y1: 20, x2: 6, y2: 14 })
])

const DevOpsIcon = () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
  h('circle', { cx: 12, cy: 12, r: 3 }),
  h('path', { d: 'M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z' })
])

const techCategories = [
  {
    name: 'Frontend',
    icon: FrontendIcon,
    items: [
      { name: 'Vue 3', emoji: '⚡', level: 85 },
      { name: 'TypeScript', emoji: '📘', level: 75 },
      { name: 'CSS/Tailwind', emoji: '🎨', level: 80 }
    ]
  },
  {
    name: 'Backend',
    icon: BackendIcon,
    items: [
      { name: 'Python', emoji: '🐍', level: 90 },
      { name: 'FastAPI', emoji: '🚀', level: 85 },
      { name: 'SQL', emoji: '🗄️', level: 75 }
    ]
  },
  {
    name: 'Data Science',
    icon: DataIcon,
    items: [
      { name: 'Python', emoji: '📊', level: 85 },
      { name: 'Pandas', emoji: '🐼', level: 80 },
      { name: 'Machine Learning', emoji: '🤖', level: 70 }
    ]
  },
  {
    name: 'DevOps',
    icon: DevOpsIcon,
    items: [
      { name: 'Git', emoji: '📦', level: 90 },
      { name: 'Linux', emoji: '🐧', level: 75 },
      { name: 'Docker', emoji: '🐳', level: 70 }
    ]
  }
]

onMounted(() => {
  if (gridRef.value) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            isVisible.value = true
            observer.disconnect()
          }
        })
      },
      { threshold: 0.2 }
    )
    observer.observe(gridRef.value)
  }
})
</script>

<style scoped>
.tech-stack {
  padding: 6rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-family: 'Fira Code', monospace;
  font-size: 2.5rem;
  color: #E6EDF3;
  margin-bottom: 1rem;
}

.title-accent {
  color: #00FFCC;
  margin-right: 0.5rem;
}

.section-desc {
  color: #8B949E;
  font-size: 1.125rem;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.tech-category {
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.8), rgba(10, 10, 10, 0.9));
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
  transition-delay: var(--delay);
}

.tech-category.visible {
  opacity: 1;
  transform: translateY(0);
}

.tech-category:hover {
  border-color: rgba(0, 255, 204, 0.3);
  box-shadow: 0 0 30px rgba(0, 255, 204, 0.1);
}

.category-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
}

.category-icon {
  color: #00FFCC;
}

.category-name {
  font-family: 'Fira Code', monospace;
  font-size: 1rem;
  color: #E6EDF3;
}

.tech-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tech-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.tech-icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: rgba(0, 255, 204, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tech-icon {
  font-size: 1rem;
}

.tech-info {
  flex: 1;
}

.tech-name {
  display: block;
  font-size: 0.875rem;
  color: #E6EDF3;
  margin-bottom: 0.25rem;
}

.tech-bar {
  height: 3px;
  background: rgba(0, 255, 204, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.tech-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #00FFCC, #B026FF);
  border-radius: 2px;
  transition: width 1.5s ease;
  box-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
}

@media (max-width: 1024px) {
  .tech-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .tech-grid {
    grid-template-columns: 1fr;
  }
}
</style>
