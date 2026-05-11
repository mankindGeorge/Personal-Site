<template>
  <section class="hero">
    <canvas ref="canvasRef" class="hero-canvas"></canvas>
    
    <div class="hero-content">
      <div class="hero-text">
        <h1 class="hero-title">
          <span class="title-line animate-in" style="--delay: 0s">
            <span class="gradient-text">数据</span>
            <span class="white-text">驱动</span>
          </span>
          <span class="title-line animate-in" style="--delay: 0.1s">
            <span class="white-text">创造</span>
            <span class="gradient-text">未来</span>
          </span>
        </h1>
        
        <p class="hero-subtitle animate-in" style="--delay: 0.3s">
          <span class="typing-text">{{ currentTypingText }}</span>
          <span class="cursor-blink">|</span>
        </p>

        <div class="hero-tags animate-in" style="--delay: 0.5s">
          <span v-for="tag in tags" :key="tag" class="tag">{{ tag }}</span>
        </div>

        <div class="hero-cta animate-in" style="--delay: 0.7s">
          <router-link to="/docs" class="btn btn-primary">
            <svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            浏览文档
          </router-link>
          <a href="#skills" class="btn btn-secondary">
            了解更多
            <svg class="btn-icon btn-icon-right" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <polyline points="19 12 12 19 5 12"/>
            </svg>
          </a>
        </div>
      </div>

      <div class="hero-visual animate-in" style="--delay: 0.4s">
        <svg class="neural-diagram" width="300" height="300" viewBox="0 0 300 300">
          <defs>
            <linearGradient id="nodeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#00FFCC"/>
              <stop offset="100%" stop-color="#B026FF"/>
            </linearGradient>
            <filter id="nodeGlow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          <g class="neural-layer layer-input">
            <circle v-for="(node, i) in inputNodes" :key="'input-' + i"
              :cx="30" :cy="inputY(i)" r="6" 
              fill="#0D1117" stroke="url(#nodeGrad)" stroke-width="2"
            />
          </g>

          <g class="neural-layer layer-hidden">
            <circle v-for="(node, i) in hiddenNodes" :key="'hidden-' + i"
              :cx="120" :cy="hiddenY(i)" r="8"
              fill="#0D1117" stroke="url(#nodeGrad)" stroke-width="2"
              filter="url(#nodeGlow)"
            />
          </g>

          <g class="neural-layer layer-output">
            <circle v-for="(node, i) in outputNodes" :key="'output-' + i"
              :cx="210" :cy="outputY(i)" r="6"
              fill="#0D1117" stroke="url(#nodeGrad)" stroke-width="2"
            />
          </g>

          <g class="neural-connections">
            <line v-for="(conn, i) in connections" :key="'conn-' + i"
              :x1="conn.x1" :y1="conn.y1" :x2="conn.x2" :y2="conn.y2"
              stroke="url(#nodeGrad)" stroke-width="1" opacity="0.3"
            />
          </g>

          <g class="data-flow">
            <circle v-for="(flow, i) in dataFlows" :key="'flow-' + i"
              :cx="flow.x" :cy="flow.y" r="3" fill="#00FFCC"
              :opacity="flow.opacity"
            >
              <animateMotion :dur="flow.duration" repeatCount="indefinite" :path="flow.path"/>
            </circle>
          </g>
        </svg>
      </div>
    </div>

    <div class="scroll-indicator animate-in" style="--delay: 1s">
      <span class="scroll-text">向下滚动</span>
      <div class="scroll-line">
        <div class="scroll-dot"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const canvasRef = ref(null)
const currentTypingText = ref('')
let typingIndex = 0
let animationFrame = null

const typingTexts = [
  'Python · FastAPI · Vue 3',
  'Data Science & ML',
  'Full-Stack Engineer',
  'Building the future'
]

const tags = ['Vue 3', 'FastAPI', 'Python', 'Data Science', 'Machine Learning']

const inputNodes = computed(() => Array(4).fill(0))
const hiddenNodes = computed(() => Array(5).fill(0))
const outputNodes = computed(() => Array(3).fill(0))

const inputY = (i) => 60 + i * 60
const hiddenY = (i) => 40 + i * 50
const outputY = (i) => 80 + i * 60

const connections = computed(() => {
  const conns = []
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 5; j++) {
      conns.push({
        x1: 30, y1: inputY(i),
        x2: 120, y2: hiddenY(j)
      })
    }
  }
  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 3; j++) {
      conns.push({
        x1: 120, y1: hiddenY(i),
        x2: 210, y2: outputY(j)
      })
    }
  }
  return conns
})

const dataFlows = computed(() => {
  const flows = []
  for (let i = 0; i < 4; i++) {
    flows.push({
      x: 30, y: inputY(i),
      path: `M 30 ${inputY(i)} Q 75 ${(inputY(i) + hiddenY(0)) / 2} 120 ${hiddenY(0)}`,
      duration: (2 + Math.random()).toFixed(1) + 's',
      opacity: 0.8
    })
  }
  return flows
})

const typewriterEffect = () => {
  const currentText = typingTexts[typingIndex % typingTexts.length]
  let charIndex = 0
  
  const type = () => {
    if (charIndex <= currentText.length) {
      currentTypingText.value = currentText.slice(0, charIndex)
      charIndex++
      setTimeout(type, 80)
    } else {
      setTimeout(() => {
        typingIndex++
        typewriterEffect()
      }, 2000)
    }
  }
  type()
}

class NeuralCanvas {
  constructor(canvas) {
    this.canvas = canvas
    this.ctx = canvas.getContext('2d')
    this.nodes = []
    this.particles = []
    this.mouse = { x: 0, y: 0 }
    this.resizeTimer = null
    this.resize()
    this.initNodes()
    this.bindEvents()
  }

  resize() {
    const dpr = window.devicePixelRatio || 1
    this.canvas.width = window.innerWidth * dpr
    this.canvas.height = window.innerHeight * dpr
    this.canvas.style.width = window.innerWidth + 'px'
    this.canvas.style.height = window.innerHeight + 'px'
    this.ctx.scale(dpr, dpr)
  }

  debouncedResize() {
    clearTimeout(this.resizeTimer)
    this.resizeTimer = setTimeout(() => {
      this.resize()
      this.initNodes()
    }, 100)
  }

  initNodes() {
    this.nodes = []
    const count = Math.floor((window.innerWidth * window.innerHeight) / 25000)
    
    for (let i = 0; i < count; i++) {
      this.nodes.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 2 + 1,
        color: Math.random() > 0.5 ? '#00FFCC' : '#B026FF'
      })
    }

    this.particles = []
    for (let i = 0; i < count / 2; i++) {
      const startNode = this.nodes[Math.floor(Math.random() * this.nodes.length)]
      const endNode = this.nodes[Math.floor(Math.random() * this.nodes.length)]
      this.particles.push({
        startNode,
        endNode,
        progress: Math.random(),
        speed: 0.002 + Math.random() * 0.003
      })
    }
  }

  bindEvents() {
    window.addEventListener('resize', () => {
      this.debouncedResize()
    })
    
    this.canvas.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX
      this.mouse.y = e.clientY
    })
  }

  draw() {
    this.ctx.fillStyle = 'rgba(10, 10, 10, 0.1)'
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height)

    this.drawConnections()
    this.drawParticles()
    this.drawNodes()
    
    animationFrame = requestAnimationFrame(() => this.draw())
  }

  drawConnections() {
    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const dx = this.nodes[i].x - this.nodes[j].x
        const dy = this.nodes[i].y - this.nodes[j].y
        const distance = Math.sqrt(dx * dx + dy * dy)
        
        if (distance < 150) {
          const opacity = (150 - distance) / 150 * 0.3
          this.ctx.beginPath()
          this.ctx.strokeStyle = `rgba(0, 255, 204, ${opacity})`
          this.ctx.lineWidth = 0.5
          this.ctx.moveTo(this.nodes[i].x, this.nodes[i].y)
          this.ctx.lineTo(this.nodes[j].x, this.nodes[j].y)
          this.ctx.stroke()
        }
      }
    }
  }

  drawParticles() {
    this.particles.forEach(particle => {
      const dx = particle.endNode.x - particle.startNode.x
      const dy = particle.endNode.y - particle.startNode.y
      
      particle.progress += particle.speed
      if (particle.progress > 1) {
        particle.progress = 0
        particle.startNode = particle.endNode
        particle.endNode = this.nodes[Math.floor(Math.random() * this.nodes.length)]
      }

      const x = particle.startNode.x + dx * particle.progress
      const y = particle.startNode.y + dy * particle.progress

      this.ctx.beginPath()
      this.ctx.arc(x, y, 2, 0, Math.PI * 2)
      this.ctx.fillStyle = '#00FFCC'
      this.ctx.fill()
      
      this.ctx.beginPath()
      this.ctx.arc(x, y, 4, 0, Math.PI * 2)
      this.ctx.fillStyle = 'rgba(0, 255, 204, 0.3)'
      this.ctx.fill()
    })
  }

  drawNodes() {
    this.nodes.forEach(node => {
      const dx = this.mouse.x - node.x
      const dy = this.mouse.y - node.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      
      if (distance < 100) {
        node.vx += dx * 0.00005
        node.vy += dy * 0.00005
      }

      node.x += node.vx
      node.y += node.vy

      if (node.x < 0 || node.x > this.canvas.width) node.vx *= -1
      if (node.y < 0 || node.y > this.canvas.height) node.vy *= -1

      this.ctx.beginPath()
      this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
      this.ctx.fillStyle = node.color
      this.ctx.fill()
    })
  }
}

onMounted(() => {
  if (canvasRef.value) {
    const neuralCanvas = new NeuralCanvas(canvasRef.value)
    neuralCanvas.draw()
  }
  typewriterEffect()
})

onUnmounted(() => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }
})
</script>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 6rem 2rem 4rem;
  overflow: hidden;
}

.hero-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  opacity: 0.6;
}

.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  width: 100%;
  gap: 4rem;
}

.hero-text {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.title-line {
  display: block;
}

.white-text {
  color: #E6EDF3;
}

.gradient-text {
  background: linear-gradient(135deg, #00FFCC, #B026FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.animate-in {
  opacity: 0;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: var(--delay, 0s);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-subtitle {
  font-family: 'Fira Code', monospace;
  font-size: 1.25rem;
  color: #8B949E;
  margin-bottom: 1.5rem;
  min-height: 2rem;
}

.cursor-blink {
  animation: blink 0.8s infinite;
  color: #B026FF;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.tag {
  padding: 0.5rem 1rem;
  background: rgba(0, 255, 204, 0.1);
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 20px;
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
  color: #00FFCC;
  transition: all 0.3s ease;
}

.tag:hover {
  background: rgba(0, 255, 204, 0.2);
  box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
}

.hero-cta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  color: #0A0A0A;
  box-shadow: 0 4px 20px rgba(0, 255, 204, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(0, 255, 204, 0.4);
}

.btn-secondary {
  background: transparent;
  color: #E6EDF3;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  border-color: #00FFCC;
  color: #00FFCC;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.btn-icon-right {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(3px); }
}

.hero-visual {
  flex-shrink: 0;
}

.neural-diagram {
  filter: drop-shadow(0 0 30px rgba(0, 255, 204, 0.3));
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  align-self: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.scroll-text {
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  color: #8B949E;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.scroll-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, #00FFCC, transparent);
  position: relative;
}

.scroll-dot {
  width: 6px;
  height: 6px;
  background: #00FFCC;
  border-radius: 50%;
  position: absolute;
  left: -2.5px;
  animation: scrollDown 2s infinite;
}

@keyframes scrollDown {
  0% { top: 0; opacity: 1; }
  100% { top: 100%; opacity: 0; }
}

@media (max-width: 968px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
  }

  .hero-visual {
    order: -1;
  }

  .hero-visual svg {
    width: 200px;
    height: 200px;
  }

  .hero-tags {
    justify-content: center;
  }

  .hero-cta {
    justify-content: center;
  }
}
</style>
