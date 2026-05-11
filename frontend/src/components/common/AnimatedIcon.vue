<template>
  <div 
    class="icon-wrapper" 
    :style="iconStyle"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div class="icon-container">
      <component 
        :is="iconComponent" 
        class="animated-icon"
        :size="size"
        :stroke-width="strokeWidth"
      />
      <div class="icon-glow" :class="{ active: isHovered }"></div>
    </div>
    <svg class="icon-circuit" :width="size * 1.5" :height="size * 1.5" :viewBox="`0 0 ${size * 1.5} ${size * 1.5}`">
      <circle 
        class="circuit-ring"
        :cx="size * 0.75"
        :cy="size * 0.75"
        :r="size * 0.6"
        fill="none"
        stroke-width="0.5"
      />
      <line 
        v-for="i in 4" 
        :key="i"
        class="circuit-node"
        :x1="size * 0.75 + (i % 2 === 0 ? 1 : -1) * size * 0.6"
        :y1="size * 0.75 + (i <= 2 ? -1 : 1) * size * 0.6"
        :x2="size * 0.75 + (i % 2 === 0 ? 1 : -1) * size * 0.75"
        :y2="size * 0.75 + (i <= 2 ? -1 : 1) * size * 0.75"
        stroke-width="0.5"
      />
    </svg>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  FileText,
  Rocket,
  GraduationCap,
  Sparkles,
  Code2,
  Database,
  Brain,
  Terminal,
  GitBranch,
  Cpu,
  Layers,
  Globe
} from 'lucide-vue-next'

const props = defineProps({
  name: { type: String, required: true },
  size: { type: Number, default: 24 },
  color: { type: String, default: '#00FFCC' },
  strokeWidth: { type: Number, default: 1.5 },
  hoverColor: { type: String, default: '#B026FF' }
})

const isHovered = ref(false)

const iconMap = {
  'file-text': FileText,
  'file': FileText,
  'article': FileText,
  'doc': FileText,
  'rocket': Rocket,
  'project': Rocket,
  'startup': Rocket,
  'graduation-cap': GraduationCap,
  'student': GraduationCap,
  'school': GraduationCap,
  'sparkles': Sparkles,
  'passion': Sparkles,
  'infinity': Sparkles,
  'code': Code2,
  'code2': Code2,
  'frontend': Code2,
  'database': Database,
  'sql': Database,
  'storage': Database,
  'brain': Brain,
  'ml': Brain,
  'machine-learning': Brain,
  'terminal': Terminal,
  'cli': Terminal,
  'command': Terminal,
  'git-branch': GitBranch,
  'git': GitBranch,
  'version': GitBranch,
  'cpu': Cpu,
  'chip': Cpu,
  'processor': Cpu,
  'layers': Layers,
  'stack': Layers,
  'architecture': Layers,
  'globe': Globe,
  'web': Globe,
  'internet': Globe
}

const iconComponent = computed(() => {
  return iconMap[props.name] || iconMap['sparkles']
})

const iconStyle = computed(() => ({
  '--icon-color': props.color,
  '--icon-hover-color': props.hoverColor,
  '--icon-size': props.size + 'px'
}))
</script>

<style scoped>
.icon-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--icon-size);
  height: var(--icon-size);
  cursor: pointer;
}

.icon-container {
  position: relative;
  z-index: 2;
}

.animated-icon {
  color: var(--icon-color);
  transition: color 0.3s ease, transform 0.3s ease;
}

.icon-wrapper:hover .animated-icon {
  color: var(--icon-hover-color);
  transform: scale(1.1);
}

.icon-glow {
  position: absolute;
  inset: -8px;
  background: radial-gradient(
    circle, 
    var(--icon-hover-color) 0%, 
    transparent 70%
  );
  opacity: 0;
  filter: blur(10px);
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.icon-glow.active {
  opacity: 0.5;
  animation: glow-pulse 1.5s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.1); }
}

.icon-circuit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.2;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.icon-wrapper:hover .icon-circuit {
  opacity: 0.6;
}

.circuit-ring {
  stroke: var(--icon-color);
  transition: stroke 0.3s ease;
}

.icon-wrapper:hover .circuit-ring {
  stroke: var(--icon-hover-color);
  stroke-dasharray: 4 2;
  animation: circuit-rotate 4s linear infinite;
  transform-origin: center;
}

.circuit-node {
  stroke: var(--icon-color);
  transition: stroke 0.3s ease, opacity 0.3s ease;
  opacity: 0.5;
}

.icon-wrapper:hover .circuit-node {
  stroke: var(--icon-hover-color);
  opacity: 1;
  animation: node-blink 0.5s ease infinite;
}

.icon-wrapper:hover .circuit-node:nth-child(odd) {
  animation-delay: 0.25s;
}

@keyframes circuit-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes node-blink {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}
</style>