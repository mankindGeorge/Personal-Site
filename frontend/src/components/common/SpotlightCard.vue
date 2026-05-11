<template>
  <div class="spotlight-card"
    ref="cardRef"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <div class="spotlight" :style="spotlightStyle"></div>
    <div class="card-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'

const cardRef = ref(null)
const spotlightStyle = reactive({
  background: 'radial-gradient(circle 150px at var(--x, 50%) var(--y, 50%), rgba(0, 255, 204, 0.15), transparent 60%)'
})

const handleMouseMove = (e) => {
  if (!cardRef.value) return
  const rect = cardRef.value.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100
  
  cardRef.value.style.setProperty('--x', `${x}%`)
  cardRef.value.style.setProperty('--y', `${y}%`)
}

const handleMouseLeave = () => {
  if (!cardRef.value) return
  cardRef.value.style.setProperty('--x', '50%')
  cardRef.value.style.setProperty('--y', '50%')
}
</script>

<style scoped>
.spotlight-card {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 10, 0.95));
  border: 1px solid rgba(0, 255, 204, 0.1);
  transition: border-color 0.3s ease, transform 0.3s ease;
}

.spotlight-card:hover {
  border-color: rgba(0, 255, 204, 0.3);
  transform: translateY(-2px);
}

.spotlight {
  position: absolute;
  inset: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.card-content {
  position: relative;
  z-index: 2;
}
</style>