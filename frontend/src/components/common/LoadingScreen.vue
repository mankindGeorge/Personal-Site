<template>
  <div class="loading-screen">
    <div class="loading-content">
      <svg 
        class="neural-network"
        :width="svgSize"
        :height="svgSize"
        viewBox="0 0 200 200"
      >
        <defs>
          <linearGradient id="cyanPurple" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00FFCC" />
            <stop offset="100%" stop-color="#B026FF" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        <g class="connections">
          <path
            v-for="(conn, i) in connections"
            :key="'conn-' + i"
            :d="conn.path"
            fill="none"
            stroke="url(#cyanPurple)"
            stroke-width="1"
            :stroke-dasharray="conn.length"
            :stroke-dashoffset="animated ? conn.length : conn.length"
            :class="{ 'draw-line': animated }"
          />
        </g>

        <g class="nodes">
          <circle
            v-for="(node, i) in nodes"
            :key="'node-' + i"
            :cx="node.x"
            :cy="node.y"
            :r="animated ? node.r : 0"
            fill="#0D1117"
            stroke="url(#cyanPurple)"
            stroke-width="2"
            :class="{ 'pulse-node': animated }"
            :style="{ animationDelay: node.delay + 's' }"
          />
        </g>

        <g class="particles">
          <circle
            v-for="(particle, i) in particles"
            :key="'particle-' + i"
            :cx="particle.x"
            :cy="particle.y"
            r="2"
            fill="#00FFCC"
            :opacity="particle.opacity"
            :class="{ 'float-particle': animated }"
            :style="{ animationDelay: particle.delay + 's' }"
          />
        </g>
      </svg>

      <div class="loading-text">
        <span class="typing-text">{{ displayedText }}</span>
        <span class="cursor">|</span>
      </div>

      <div class="progress-container">
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ width: progress + '%' }"
          ></div>
        </div>
        <span class="progress-text">{{ Math.round(progress) }}%</span>
      </div>
    </div>

    <div class="grid-overlay"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const emit = defineEmits(['complete'])

const progress = ref(0)
const animated = ref(false)
const displayedText = ref('')
const svgSize = ref(280)

const loadingMessages = [
  '初始化神经网络...',
  '加载数据模型...',
  '构建知识图谱...',
  '同步数据流...',
  '准备就绪'
]

const nodes = [
  { x: 100, y: 100, r: 8, delay: 0 },
  { x: 50, y: 50, r: 5, delay: 0.1 },
  { x: 150, y: 50, r: 5, delay: 0.2 },
  { x: 50, y: 150, r: 5, delay: 0.3 },
  { x: 150, y: 150, r: 5, delay: 0.4 },
  { x: 25, y: 100, r: 4, delay: 0.5 },
  { x: 175, y: 100, r: 4, delay: 0.6 },
  { x: 100, y: 25, r: 4, delay: 0.7 },
  { x: 100, y: 175, r: 4, delay: 0.8 }
]

const connections = computed(() => [
  { path: 'M 100 100 L 50 50', length: 72 },
  { path: 'M 100 100 L 150 50', length: 72 },
  { path: 'M 100 100 L 50 150', length: 72 },
  { path: 'M 100 100 L 150 150', length: 72 },
  { path: 'M 50 50 L 25 100', length: 56 },
  { path: 'M 150 50 L 175 100', length: 56 },
  { path: 'M 50 150 L 25 100', length: 56 },
  { path: 'M 150 150 L 175 100', length: 56 },
  { path: 'M 50 50 L 100 25', length: 56 },
  { path: 'M 150 50 L 100 25', length: 56 },
  { path: 'M 50 150 L 100 175', length: 56 },
  { path: 'M 150 150 L 100 175', length: 56 },
  { path: 'M 25 100 L 50 50', length: 56 },
  { path: 'M 175 100 L 150 50', length: 56 }
])

const particles = computed(() => {
  const result = []
  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2
    const radius = 35
    result.push({
      x: 100 + Math.cos(angle) * radius,
      y: 100 + Math.sin(angle) * radius,
      opacity: 0.6 + Math.random() * 0.4,
      delay: Math.random() * 2
    })
  }
  return result
})

const typeText = async (text) => {
  for (let i = 0; i <= text.length; i++) {
    displayedText.value = text.slice(0, i)
    await new Promise(resolve => setTimeout(resolve, 50))
  }
}

const runLoadingSequence = async () => {
  animated.value = true
  
  await new Promise(resolve => setTimeout(resolve, 300))
  
  for (let i = 0; i < loadingMessages.length; i++) {
    await typeText(loadingMessages[i])
    
    const startProgress = (i / loadingMessages.length) * 100
    const endProgress = ((i + 1) / loadingMessages.length) * 100
    
    const animateProgress = () => {
      return new Promise(resolve => {
        const interval = setInterval(() => {
          if (progress.value < endProgress) {
            progress.value += 2
          } else {
            clearInterval(interval)
            resolve()
          }
        }, 30)
      })
    }
    
    await animateProgress()
    
    if (i < loadingMessages.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 300))
    }
  }
  
  await new Promise(resolve => setTimeout(resolve, 500))
  emit('complete')
}

onMounted(() => {
  if (window.innerWidth < 640) {
    svgSize.value = 200
  }
  runLoadingSequence()
})
</script>

<style scoped>
.loading-screen {
  position: fixed;
  inset: 0;
  background: #0A0A0A;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  overflow: hidden;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  z-index: 2;
}

.neural-network {
  filter: drop-shadow(0 0 20px rgba(0, 255, 204, 0.5));
}

.connections path {
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.draw-line {
  animation: drawLine 1s ease-out forwards;
}

@keyframes drawLine {
  to {
    stroke-dashoffset: 0;
  }
}

.nodes circle {
  fill: #0D1117;
  transition: all 0.5s ease;
}

.pulse-node {
  animation: pulseNode 2s ease-in-out infinite;
}

@keyframes pulseNode {
  0%, 100% {
    filter: drop-shadow(0 0 5px #00FFCC);
  }
  50% {
    filter: drop-shadow(0 0 15px #00FFCC);
  }
}

.float-particle {
  animation: floatParticle 3s ease-in-out infinite;
}

@keyframes floatParticle {
  0%, 100% {
    transform: translate(0, 0);
    opacity: 0.6;
  }
  50% {
    transform: translate(5px, -5px);
    opacity: 1;
  }
}

.loading-text {
  font-family: 'Fira Code', monospace;
  font-size: 1.1rem;
  color: #00FFCC;
  min-height: 2rem;
}

.typing-text {
  display: inline-block;
}

.cursor {
  animation: blink 0.8s infinite;
  color: #B026FF;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 280px;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: rgba(0, 255, 204, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00FFCC, #B026FF);
  border-radius: 2px;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
}

.progress-text {
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
  color: #8B949E;
  min-width: 3rem;
  text-align: right;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
}
</style>
