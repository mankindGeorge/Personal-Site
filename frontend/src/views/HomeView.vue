<template>
  <div class="home-view">
    <HeroSection />
    
    <!-- 数据统计区 -->
    <section class="stats-section" ref="statsRef">
      <div class="stats-container">
        <div 
          v-for="(stat, i) in stats" 
          :key="stat.label"
          class="stat-card"
          :class="{ visible: statsVisible }"
          :style="{ '--delay': `${i * 0.1}s` }"
        >
          <AnimatedIcon 
            :name="stat.icon"
            :size="32"
            :color="stat.color"
            :hoverColor="stat.hoverColor"
          />
          <div class="stat-content">
            <span class="stat-number">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心技能区 - 横向滚动劫持 -->
    <div class="scene-scroll-wrapper" id="skills" ref="scrollWrapper">
      <section 
        class="scene-section"
        ref="sceneSection"
      >
        <div class="scene-container">
          <div class="scene-header">
            <span class="scene-tag">技能</span>
            <h2 class="scene-title">核心技能</h2>
            <p class="scene-subtitle">我专注的技术领域</p>
          </div>

          <div class="scene-viewport">
            <div class="scene-fade scene-fade--left"></div>
            <div class="scene-fade scene-fade--right"></div>
            
            <div 
              class="scene-track"
              ref="sceneTrack"
              :style="{ transform: `translateX(${trackTranslateX}px)` }"
            >
              <div 
                v-for="(skill, i) in skills"
                :key="skill.name"
                class="scene-item"
                :style="{
                  '--item-index': i,
                  '--item-color': skill.color,
                  '--reveal-delay': `${i * 0.1}s`
                }"
                @click="handleCardClick"
              >
                <div class="scene-item__inner">
                  <div class="scene-item__media">
                    <div class="scene-item__icon" v-html="skill.icon"></div>
                    <div class="scene-item__glow"></div>
                  </div>
                  <div class="scene-item__content">
                    <h3 class="scene-item__title">{{ skill.name }}</h3>
                    <div class="scene-item__tags">
                      <span 
                        v-for="tag in skill.tags" 
                        :key="tag"
                        class="scene-item__tag"
                      >{{ tag }}</span>
                    </div>
                  </div>
                  <div class="scene-item__index">{{ String(i + 1).padStart(2, '0') }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="scene-progress">
            <div class="progress-track">
              <div class="progress-bar" :style="{ width: scrollProgress + '%' }"></div>
              <div class="progress-indicator" :style="{ left: scrollProgress + '%' }"></div>
            </div>
          </div>
          
          <div class="scroll-hint">
            <span class="scroll-hint__text">向下滚动探索</span>
            <div class="scroll-hint__icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M19 12l-7 7-7-7"/>
              </svg>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 最新文章区 - 无限循环滚动 -->
    <section class="articles-section">
      <div class="section-header">
        <span class="section-tag">文章</span>
        <h2 class="section-title">最新文章</h2>
        <router-link to="/docs" class="view-all">
          查看全部
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </router-link>
      </div>

      <div 
        class="articles-carousel"
        @mouseenter="pauseScroll = true"
        @mouseleave="pauseScroll = false"
      >
        <div 
          class="articles-track"
          :class="{ paused: pauseScroll }"
        >
          <article 
            v-for="(article, i) in [...latestArticles, ...latestArticles]"
            :key="'article-' + i"
            class="article-card"
          >
            <div class="article-meta">
              <span class="article-category">{{ article.category }}</span>
              <span class="article-date">{{ article.date }}</span>
            </div>
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-excerpt">{{ article.excerpt }}</p>
            <div class="article-tags">
              <span v-for="tag in article.tags" :key="tag" class="article-tag">{{ tag }}</span>
            </div>
          </article>
        </div>
      </div>
    </section>

    <TechStack />

    <!-- 联系方式区 -->
    <section class="contact-section">
      <div class="contact-container">
        <div class="contact-content">
          <h2 class="contact-title">联系我</h2>
          <p class="contact-desc">有问题或想法？随时联系我！</p>
          <div class="contact-links">
            <a href="mailto:mankindgeorge06@gmail.com" class="contact-btn primary">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              发送邮件
            </a>
            <a href="https://github.com/mankindGeorge" target="_blank" class="contact-btn secondary">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
            </a>
          </div>
        </div>
        <div class="contact-decoration">
          <div class="decoration-ring ring-1"></div>
          <div class="decoration-ring ring-2"></div>
          <div class="decoration-ring ring-3"></div>
        </div>
      </div>
    </section>

    <button 
      class="back-to-top"
      :class="{ 'is-visible': showBackToTop }"
      @click="scrollToTop"
      aria-label="回到顶部"
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 19V5M5 12l7-7 7 7"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import HeroSection from '@/components/home/HeroSection.vue'
import TechStack from '@/components/home/TechStack.vue'
import AnimatedIcon from '@/components/common/AnimatedIcon.vue'

const statsRef = ref(null)
const statsVisible = ref(false)
const scrollWrapper = ref(null)
const sceneSection = ref(null)
const sceneTrack = ref(null)

const trackTranslateX = ref(0)
const targetTranslateX = ref(0)
const scrollProgress = ref(0)
const maxTrackScroll = ref(0)
const wrapperHeight = ref('100vh')
const centerOffset = ref(0)
const lerpFactor = 0.08
const cardWidth = 300
const cardGap = 40
const showBackToTop = ref(false)

const stats = [
  { icon: 'file-text', value: '15+', label: '文章', color: '#00FFCC', hoverColor: '#B026FF' },
  { icon: 'rocket', value: '5+', label: '项目', color: '#B026FF', hoverColor: '#00FFCC' },
  { icon: 'graduation-cap', value: '大二', label: '学生', color: '#00FFCC', hoverColor: '#B026FF' },
  { icon: 'sparkles', value: '∞', label: '热情', color: '#B026FF', hoverColor: '#00FFCC' }
]

const skills = [
  {
    name: '前端开发',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    tags: ['Vue 3', 'React', 'TypeScript'],
    size: 0.85,
    offsetY: 0.8,
    color: '#00FFCC'
  },
  {
    name: '数据科学',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    tags: ['Python', 'ML', 'TensorFlow'],
    size: 1.0,
    offsetY: -0.9,
    color: '#B026FF'
  },
  {
    name: '后端 API',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    tags: ['FastAPI', 'Node.js', 'PostgreSQL'],
    size: 0.75,
    offsetY: 0.6,
    color: '#00FFCC'
  },
  {
    name: 'DevOps',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m8 17 4 4 4-4"/></svg>',
    tags: ['Docker', 'CI/CD', 'Linux'],
    size: 0.9,
    offsetY: -0.7,
    color: '#B026FF'
  },
  {
    name: 'UI/UX 设计',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
    tags: ['Figma', 'Tailwind', 'Motion'],
    size: 0.7,
    offsetY: 0.5,
    color: '#00FFCC'
  },
  {
    name: '开源贡献',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="4"/><line x1="1.05" y1="12" x2="7" y2="12"/><line x1="17.01" y1="12" x2="22.96" y2="12"/></svg>',
    tags: ['GitHub', 'Code Review', 'Docs'],
    size: 0.8,
    offsetY: -0.4,
    color: '#B026FF'
  }
]

const latestArticles = [
  {
    title: 'FastAPI 高性能 Web 开发',
    excerpt: '深入探讨 FastAPI 异步模式与企业级 API 性能优化。',
    category: '后端',
    date: '2024-01-15',
    tags: ['Python', 'FastAPI']
  },
  {
    title: 'Vue 3 Composition API 最佳实践',
    excerpt: '探索高级 Composition API 模式，构建可维护的大型应用。',
    category: '前端',
    date: '2024-01-10',
    tags: ['Vue', 'JavaScript']
  },
  {
    title: 'ML 模型部署完整指南',
    excerpt: '从训练到生产——一步步将 ML 模型部署为 API 服务。',
    category: '数据科学',
    date: '2024-01-05',
    tags: ['ML', 'Docker']
  },
  {
    title: 'FastAPI 与 WebSocket 实时数据',
    excerpt: '使用 FastAPI 的 WebSocket 支持构建实时应用。',
    category: '后端',
    date: '2024-01-01',
    tags: ['WebSocket', 'Python']
  },
  {
    title: '数据科学家的 Docker 指南',
    excerpt: '容器化你的 ML 工作流，实现可复现的实验。',
    category: 'DevOps',
    date: '2023-12-28',
    tags: ['Docker', 'ML']
  }
]

/**
 * 核心: 计算轨道边界和容器高度
 * 
 * 第一张卡片在视口 1/4 到 1/3 位置，最后一张卡片居中
 * 
 * 每个卡片占据一屏的滚动距离
 * 总滚动高度 = 视口高度 + (卡片数 - 1) * 视口高度
 */
const calculateBounds = () => {
  if (!sceneTrack.value || !sceneSection.value || !scrollWrapper.value) return
  
  const viewportWidth = sceneSection.value.offsetWidth
  const viewportHeight = window.innerHeight
  const numCards = skills.length
  
  const cardStep = cardWidth + cardGap
  
  const startOffset = viewportWidth * 0.25
  const endOffset = (viewportWidth - cardWidth) / 2
  
  centerOffset.value = startOffset
  maxTrackScroll.value = (numCards - 1) * cardStep - (endOffset - startOffset)
  
  const totalScrollHeight = viewportHeight * numCards
  wrapperHeight.value = `${totalScrollHeight}px`
  
  targetTranslateX.value = startOffset
  trackTranslateX.value = startOffset
  
  handleScroll()
}

/**
 * Lerp 线性插值函数
 * 用于平滑过渡动画
 */
const lerp = (start, end, factor) => {
  return start + (end - start) * factor
}

/**
 * 动画循环：持续平滑过渡
 */
let animationId = null
const animate = () => {
  const diff = Math.abs(trackTranslateX.value - targetTranslateX.value)
  
  if (diff > 0.5) {
    trackTranslateX.value = lerp(trackTranslateX.value, targetTranslateX.value, lerpFactor)
    animationId = requestAnimationFrame(animate)
  } else {
    trackTranslateX.value = targetTranslateX.value
    animationId = null
  }
}

/**
 * 启动动画循环
 */
const startAnimation = () => {
  if (!animationId) {
    animationId = requestAnimationFrame(animate)
  }
}

/**
 * 核心: 滚动进度映射算法
 * 
 * 纵向滚动进度 → 横向位移
 * 
 * 每滚动一屏视口高度，卡片向左移动一个卡片宽度 + 间距
 * 
 * 数学映射:
 * - progress = 0: 第一张卡片居中
 * - progress = 1/n: 第二张卡片居中
 * - progress = 1: 最后一张卡片居中
 * 
 * 公式:
 *   translateX = centerOffset - progress * maxTrackScroll
 */
const handleScroll = () => {
  if (!scrollWrapper.value) return
  
  const wrapperRect = scrollWrapper.value.getBoundingClientRect()
  const viewportHeight = window.innerHeight
  const wrapperHeightVal = scrollWrapper.value.offsetHeight
  
  const scrollableDistance = wrapperHeightVal - viewportHeight
  
  let progress = 0
  if (scrollableDistance > 0) {
    const scrolledDistance = -wrapperRect.top
    progress = scrolledDistance / scrollableDistance
    progress = Math.max(0, Math.min(1, progress))
  }
  
  const currentMaxScroll = maxTrackScroll.value
  
  if (currentMaxScroll > 0) {
    targetTranslateX.value = centerOffset.value - progress * currentMaxScroll
  } else {
    targetTranslateX.value = centerOffset.value
  }
  
  scrollProgress.value = progress * 100
  
  startAnimation()
}

/**
 * 卡片点击果冻效果
 */
const handleCardClick = (e) => {
  const card = e.currentTarget
  const inner = card.querySelector('.scene-item__inner')
  if (!inner) return
  
  inner.classList.remove('jelly-animate')
  void inner.offsetWidth
  inner.classList.add('jelly-animate')
  
  setTimeout(() => {
    inner.classList.remove('jelly-animate')
  }, 800)
}

/**
 * 回到顶部 - 自定义平滑滚动
 */
const scrollToTop = () => {
  const startY = window.scrollY
  const duration = 1500
  const startTime = performance.now()
  
  const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3)
  
  const animate = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easedProgress = easeOutCubic(progress)
    
    window.scrollTo(0, startY * (1 - easedProgress))
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }
  
  requestAnimationFrame(animate)
}

/**
 * 检查是否显示回到顶部按钮
 */
const checkBackToTop = () => {
  showBackToTop.value = window.scrollY > 300
}

let scrollHandler = null
let resizeObserver = null

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          statsVisible.value = true
          observer.disconnect()
        }
      })
    },
    { threshold: 0.3 }
  )
  
  if (statsRef.value) {
    observer.observe(statsRef.value)
  }
  
  nextTick(() => {
    requestAnimationFrame(() => {
      calculateBounds()
    })
  })
  
  scrollHandler = () => {
    requestAnimationFrame(handleScroll)
    checkBackToTop()
  }
  window.addEventListener('scroll', scrollHandler, { passive: true })
  
  resizeObserver = new ResizeObserver(() => {
    requestAnimationFrame(() => {
      calculateBounds()
    })
  })
  
  if (scrollWrapper.value) {
    resizeObserver.observe(scrollWrapper.value)
  }
  if (sceneTrack.value) {
    resizeObserver.observe(sceneTrack.value)
  }
  
  window.addEventListener('resize', () => {
    requestAnimationFrame(() => {
      calculateBounds()
    })
  })
})

onUnmounted(() => {
  if (scrollHandler) {
    window.removeEventListener('scroll', scrollHandler)
  }
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.home-view {
  min-height: 100vh;
}

/* 统计数据区 */
.stats-section {
  padding: 2rem;
  margin-top: clamp(-3rem, -5vw, -2rem);
  position: relative;
  z-index: 10;
}

.stats-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.stat-card {
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.95), rgba(10, 10, 10, 0.98));
  border: 1px solid rgba(0, 255, 204, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
  transition-delay: var(--delay);
}

.stat-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.stat-card:hover {
  border-color: rgba(0, 255, 204, 0.4);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 255, 204, 0.15);
}

.stat-icon {
  font-size: 2rem;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-family: 'Fira Code', monospace;
  font-size: 1.75rem;
  font-weight: 700;
  color: #00FFCC;
}

.stat-label {
  font-size: 0.875rem;
  color: #8B949E;
}

/* 核心技能区 - 横向滚动劫持 */
.scene-scroll-wrapper {
  height: v-bind(wrapperHeight);
  position: relative;
}

.scene-section {
  position: sticky;
  top: 0;
  height: 100vh;
  height: 100dvh;
  background: linear-gradient(180deg, rgba(0, 255, 204, 0.02), transparent);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scene-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  box-sizing: border-box;
}

.scene-header {
  text-align: center;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.scene-tag {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: rgba(0, 255, 204, 0.1);
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 30px;
  color: #00FFCC;
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  margin-bottom: 1rem;
}

.scene-title {
  font-family: 'Fira Code', monospace;
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 700;
  color: #E6EDF3;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.scene-subtitle {
  color: #8B949E;
  font-size: 1.125rem;
  margin: 0;
}

.scene-viewport {
  position: relative;
  width: 100%;
  overflow: hidden;
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
}

.scene-fade {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 150px;
  z-index: 10;
  pointer-events: none;
}

.scene-fade--left {
  left: 0;
  background: linear-gradient(90deg, 
    rgba(13, 17, 23, 1) 0%,
    rgba(13, 17, 23, 0.8) 40%,
    transparent 100%
  );
}

.scene-fade--right {
  right: 0;
  background: linear-gradient(-90deg, 
    rgba(13, 17, 23, 1) 0%,
    rgba(13, 17, 23, 0.8) 40%,
    transparent 100%
  );
}

.scene-track {
  display: flex;
  gap: 40px;
  will-change: transform;
  width: max-content;
  padding: 40px 0;
}

.scene-item {
  flex-shrink: 0;
  width: 300px;
  opacity: 0;
  animation: revealItem 0.8s ease forwards;
  animation-delay: var(--reveal-delay, 0s);
}

@keyframes revealItem {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scene-item__inner {
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.95), rgba(10, 10, 10, 0.98));
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 2rem;
  height: 340px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.scene-item__inner::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, 
    color-mix(in srgb, var(--item-color, #00FFCC) 8%, transparent),
    color-mix(in srgb, #B026FF 8%, transparent)
  );
  opacity: 0;
  transition: opacity 0.4s ease;
}

.scene-item__inner::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent,
    var(--item-color, #00FFCC),
    transparent
  );
  opacity: 0;
  transition: opacity 0.4s ease;
}

.scene-item:hover .scene-item__inner {
  border-color: color-mix(in srgb, var(--item-color, #00FFCC) 30%, transparent);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.5),
    0 0 80px color-mix(in srgb, var(--item-color, #00FFCC) 10%, transparent);
  transform: scale(1.05);
}

.scene-item:active .scene-item__inner,
.scene-item__inner.jelly-animate {
  animation: jelly 0.8s ease;
}

@keyframes jelly {
  0% { transform: scale(1.05, 1.05); }
  15% { transform: scale(0.85, 1.15); }
  25% { transform: scale(1.12, 0.88); }
  35% { transform: scale(0.92, 1.08); }
  45% { transform: scale(1.05, 0.95); }
  55% { transform: scale(0.97, 1.03); }
  65% { transform: scale(1.02, 0.98); }
  75% { transform: scale(0.99, 1.01); }
  85% { transform: scale(1.01, 0.99); }
  100% { transform: scale(1.05, 1.05); }
}

.scene-item:hover .scene-item__inner::before {
  opacity: 1;
}

.scene-item:hover .scene-item__inner::after {
  opacity: 1;
}

.scene-item__media {
  position: relative;
}

.scene-item__icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: color-mix(in srgb, var(--item-color, #00FFCC) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--item-color, #00FFCC) 20%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--item-color, #00FFCC);
  transition: all 0.4s ease;
  position: relative;
  z-index: 1;
}

.scene-item:hover .scene-item__icon {
  background: color-mix(in srgb, var(--item-color, #00FFCC) 25%, transparent);
  transform: scale(1.1);
}

.scene-item__glow {
  position: absolute;
  top: -20px;
  left: -20px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, var(--item-color, #00FFCC), transparent 70%);
  opacity: 0;
  filter: blur(20px);
  transition: opacity 0.4s ease;
}

.scene-item:hover .scene-item__glow {
  opacity: 0.3;
}

.scene-item__content {
  position: relative;
  z-index: 1;
}

.scene-item__title {
  font-family: 'Fira Code', monospace;
  font-size: 1.5rem;
  color: #E6EDF3;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}

.scene-item:hover .scene-item__title {
  color: var(--item-color, #00FFCC);
}

.scene-item__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.scene-item__tag {
  padding: 0.375rem 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #8B949E;
  font-size: 0.75rem;
  font-family: 'Fira Code', monospace;
  transition: all 0.3s ease;
}

.scene-item:hover .scene-item__tag {
  background: color-mix(in srgb, var(--item-color, #00FFCC) 10%, transparent);
  color: var(--item-color, #00FFCC);
}

.scene-item__index {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.1);
  transition: all 0.4s ease;
}

.scene-item:hover .scene-item__index {
  color: color-mix(in srgb, var(--item-color, #00FFCC) 50%, transparent);
  transform: translateX(-5px);
}

.scene-progress {
  margin-top: 1.5rem;
  padding: 0;
}

.progress-track {
  position: relative;
  height: 3px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: visible;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #00FFCC, #B026FF);
  border-radius: 2px;
  transition: width 0.2s ease-out;
  will-change: width;
}

.progress-indicator {
  position: absolute;
  top: 50%;
  width: 12px;
  height: 12px;
  background: #00FFCC;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
  transition: left 0.2s ease-out;
  will-change: left;
}

.progress-indicator::before {
  content: '';
  position: absolute;
  inset: -4px;
  border: 2px solid rgba(0, 255, 204, 0.3);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: 0.5; }
}

.scroll-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  margin-top: 1rem;
  opacity: 0.5;
  animation: fadeInUp 0.8s ease 1s both;
}

.scroll-hint__text {
  font-size: 0.75rem;
  color: #8B949E;
  font-family: 'Fira Code', monospace;
}

.scroll-hint__icon {
  animation: bounce 2s ease-in-out infinite;
}

.scroll-hint__icon svg {
  width: 18px;
  height: 18px;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 0.6;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(8px); }
}

@media (max-width: 1024px) {
  .scene-title {
    font-size: 3rem;
  }

  .scene-track {
    gap: 1.5rem;
  }

  .scene-item {
    width: 280px;
  }

  .scene-item__inner {
    height: 300px;
  }
}

@media (max-width: 640px) {
  .scene-scroll-wrapper {
    height: auto !important;
  }
  
  .scene-section {
    position: relative;
    height: auto;
    padding: 4rem 0 2rem;
  }

  .scene-title {
    font-size: 2.25rem;
  }

  .scene-track {
    gap: 1rem;
    overflow-x: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  .scene-track::-webkit-scrollbar {
    display: none;
  }

  .scene-fade {
    display: none;
  }
  
  .scroll-hint {
    display: none;
  }

  .scene-item {
    width: 260px;
  }

  .scene-item__inner {
    height: 280px;
    padding: 1.5rem;
  }

  .scene-item__title {
    font-size: 1.25rem;
  }
}

/* 卡片区 */
/* 文章轮播 - 无限滚动 */
.articles-section {
  padding: 6rem 0;
  background: linear-gradient(180deg, transparent, rgba(0, 255, 204, 0.02));
}

.articles-section .section-header {
  max-width: 1400px;
  margin: 0 auto 3rem;
  padding: 0 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-tag {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: rgba(0, 255, 204, 0.1);
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 30px;
  color: #00FFCC;
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  margin-bottom: 1rem;
}

.section-title {
  font-family: 'Fira Code', monospace;
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: #E6EDF3;
  margin: 0 0 1.5rem 0;
  letter-spacing: -0.02em;
}

.view-all {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #00FFCC;
  text-decoration: none;
  font-size: 0.8125rem;
  font-family: 'Fira Code', monospace;
  padding: 0.5rem 1rem;
  background: rgba(0, 255, 204, 0.1);
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 30px;
  transition: all 0.3s ease;
}

.view-all:hover {
  background: rgba(0, 255, 204, 0.2);
  border-color: rgba(0, 255, 204, 0.4);
  transform: translateX(5px);
}

.view-all svg {
  transition: transform 0.3s ease;
}

.view-all:hover svg {
  transform: translateX(3px);
}

.articles-carousel {
  width: 100%;
  overflow: hidden;
  padding: 2rem 0;
}

.articles-track {
  display: flex;
  gap: 2rem;
  animation: scrollArticles 30s linear infinite;
}

.articles-track.paused {
  animation-play-state: paused;
}

@keyframes scrollArticles {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

.article-card {
  flex-shrink: 0;
  width: 380px;
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 10, 0.95));
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.article-card:hover {
  border-color: rgba(0, 255, 204, 0.3);
  transform: scale(1.02);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.article-category {
  padding: 0.25rem 0.75rem;
  background: rgba(0, 255, 204, 0.1);
  border-radius: 12px;
  color: #00FFCC;
  font-size: 0.75rem;
  font-family: 'Fira Code', monospace;
}

.article-date {
  color: #8B949E;
  font-size: 0.75rem;
}

.article-title {
  font-family: 'Fira Code', monospace;
  font-size: 1.125rem;
  color: #E6EDF3;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.article-excerpt {
  color: #8B949E;
  font-size: 0.875rem;
  line-height: 1.7;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-tags {
  display: flex;
  gap: 0.5rem;
}

.article-tag {
  padding: 0.25rem 0.5rem;
  background: rgba(0, 255, 204, 0.05);
  border-radius: 4px;
  color: #00FFCC;
  font-size: 0.75rem;
  font-family: 'Fira Code', monospace;
}

/* 联系方式区 */
.contact-section {
  padding: 6rem 2rem;
}

.contact-container {
  max-width: 800px;
  margin: 0 auto;
  background: linear-gradient(145deg, rgba(0, 255, 204, 0.05), rgba(0, 255, 204, 0.08));
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 24px;
  padding: 4rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.contact-content {
  position: relative;
  z-index: 2;
}

.contact-title {
  font-family: 'Fira Code', monospace;
  font-size: 2.5rem;
  color: #E6EDF3;
  margin-bottom: 0.75rem;
}

.contact-desc {
  color: #8B949E;
  font-size: 1.125rem;
  margin-bottom: 2rem;
}

.contact-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.contact-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.contact-btn.primary {
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  color: #0A0A0A;
}

.contact-btn.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 255, 204, 0.3);
}

.contact-btn.secondary {
  background: transparent;
  border: 1px solid rgba(0, 255, 204, 0.3);
  color: #E6EDF3;
}

.contact-btn.secondary:hover {
  border-color: #00FFCC;
  color: #00FFCC;
}

.contact-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.decoration-ring {
  position: absolute;
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 50%;
}

.ring-1 {
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  animation: pulse-ring 4s ease-in-out infinite;
}

.ring-2 {
  width: 150%;
  height: 150%;
  top: -25%;
  left: -25%;
  animation: pulse-ring 4s ease-in-out infinite 1s;
}

.ring-3 {
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  animation: pulse-ring 4s ease-in-out infinite 2s;
}

@keyframes pulse-ring {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.1; transform: scale(1.05); }
}

/* 响应式 - 1200px 断点 */
@media (max-width: 1200px) {
  .scene-container {
    max-width: 1000px;
  }

  .stats-container {
    gap: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .article-card {
    width: 340px;
  }
}

/* 响应式 */
@media (max-width: 1024px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .features-track {
    padding: 0 5vw;
    gap: 2rem;
  }

  .feature-card {
    width: 300px;
  }
}

@media (max-width: 640px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .contact-links {
    flex-direction: column;
  }

  .contact-container {
    padding: 2rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .contact-title {
    font-size: 1.75rem;
  }

  .feature-card {
    width: 280px;
  }

  .article-card {
    width: 300px;
  }
}

/* 回到顶部按钮 */
.back-to-top {
  position: fixed;
  right: 2rem;
  bottom: 2rem;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(0, 255, 204, 0.1);
  border: 1px solid rgba(0, 255, 204, 0.3);
  color: #00FFCC;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px);
  transition: all 0.3s ease;
  z-index: 1000;
}

.back-to-top.is-visible {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.back-to-top:hover {
  background: rgba(0, 255, 204, 0.2);
  border-color: rgba(0, 255, 204, 0.5);
  box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
  transform: translateY(-3px);
}

.back-to-top:active {
  transform: scale(0.9);
}

.back-to-top svg {
  transition: transform 0.3s ease;
}

.back-to-top:hover svg {
  transform: translateY(-2px);
}

@media (max-width: 640px) {
  .back-to-top {
    right: 1rem;
    bottom: 1rem;
    width: 40px;
    height: 40px;
  }
}
</style>
