<template>
  <div 
    ref="cardRef"
    class="info-card-container"
    :style="cardStyle"
  >
    <div class="card-inner" :class="{ 'is-flipped': isFlipped }">
      <div class="card-face card-front">
        <div class="card-icon">
          <component :is="iconComponent" />
        </div>
        <h3 class="card-title">{{ title }}</h3>
        <p class="card-desc">{{ description }}</p>
        <div class="card-arrow">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </div>
      </div>
      
      <div class="card-face card-back">
        <div class="card-back-content">
          <h4 class="back-title">了解更多</h4>
          <ul class="back-list">
            <li v-for="(item, i) in details" :key="i">{{ item }}</li>
          </ul>
        </div>
        <router-link v-if="link" :to="link" class="back-link">
          访问 →
        </router-link>
      </div>
    </div>
    
    <div class="card-glow"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { useIntersectionObserver } from '@/composables/useIntersectionObserver'

const props = defineProps({
  title: String,
  description: String,
  icon: String,
  details: Array,
  link: String,
  delay: {
    type: Number,
    default: 0
  }
})

const { isVisible, elementRef } = useIntersectionObserver({
  threshold: 0.3,
  once: true
})

const isFlipped = ref(false)

const cardStyle = computed(() => ({
  '--delay': `${props.delay}s`
}))

const iconComponent = computed(() => {
  const icons = {
    blog: () => h('svg', { width: 48, height: 48, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.5 }, [
      h('path', { d: 'M12 19l7-7 3 3-7 7-3-3z' }),
      h('path', { d: 'M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z' }),
      h('path', { d: 'M2 2l7.586 7.586' }),
      h('circle', { cx: 11, cy: 11, r: 2 })
    ]),
    docs: () => h('svg', { width: 48, height: 48, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.5 }, [
      h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
      h('polyline', { points: '14 2 14 8 20 8' }),
      h('line', { x1: 16, y1: 13, x2: 8, y2: 13 }),
      h('line', { x1: 16, y1: 17, x2: 8, y2: 17 }),
      h('line', { x1: 10, y1: 9, x2: 8, y2: 9 })
    ]),
    api: () => h('svg', { width: 48, height: 48, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.5 }, [
      h('polyline', { points: '16 18 22 12 16 6' }),
      h('polyline', { points: '8 6 2 12 8 18' })
    ]),
    about: () => h('svg', { width: 48, height: 48, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.5 }, [
      h('circle', { cx: 12, cy: 8, r: 5 }),
      h('path', { d: 'M20 21a8 8 0 1 0-16 0' })
    ])
  }
  return icons[props.icon] || icons.blog
})

onMounted(() => {
  if (elementRef.value) {
    elementRef.value.addEventListener('mouseenter', () => {
      isFlipped.value = true
    })
    elementRef.value.addEventListener('mouseleave', () => {
      isFlipped.value = false
    })
  }
})
</script>

<style scoped>
.info-card-container {
  perspective: 1000px;
  width: 100%;
  height: 320px;
  cursor: pointer;
  opacity: 0;
  transform: translateY(50px) rotateX(10deg);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transition-delay: var(--delay);
}

.info-card-container.visible {
  opacity: 1;
  transform: translateY(0) rotateX(0);
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-inner.is-flipped {
  transform: rotateY(180deg);
}

.card-face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: 16px;
  border: 1px solid rgba(0, 255, 204, 0.15);
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 10, 0.95));
  padding: 2rem;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-front {
  z-index: 2;
}

.card-back {
  transform: rotateY(180deg);
  background: linear-gradient(145deg, rgba(0, 255, 204, 0.05), rgba(176, 38, 255, 0.05));
  justify-content: space-between;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(0, 255, 204, 0.15), rgba(176, 38, 255, 0.15));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: #00FFCC;
  transition: all 0.3s ease;
}

.info-card-container:hover .card-icon {
  transform: scale(1.1);
  box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
}

.card-title {
  font-family: 'Fira Code', monospace;
  font-size: 1.25rem;
  font-weight: 600;
  color: #E6EDF3;
  margin-bottom: 0.75rem;
}

.card-desc {
  color: #8B949E;
  font-size: 0.9375rem;
  line-height: 1.6;
  flex: 1;
}

.card-arrow {
  color: #00FFCC;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.info-card-container:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

.card-glow {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(176, 38, 255, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  z-index: -1;
}

.info-card-container:hover .card-glow {
  opacity: 1;
}

.back-title {
  font-family: 'Fira Code', monospace;
  font-size: 1rem;
  color: #00FFCC;
  margin-bottom: 1rem;
}

.back-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.back-list li {
  color: #8B949E;
  font-size: 0.875rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.back-list li::before {
  content: '→';
  color: #B026FF;
}

.back-link {
  color: #00FFCC;
  text-decoration: none;
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  align-self: flex-end;
}

.back-link:hover {
  color: #B026FF;
  transform: translateX(5px);
}
</style>
