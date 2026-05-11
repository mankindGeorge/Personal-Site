<template>
  <div class="bg-effects">
    <div class="tech-grid-bg"></div>
    <div class="noise-overlay"></div>
    <div class="ambient-glow ambient-glow--cyan"></div>
    <div class="ambient-glow ambient-glow--purple"></div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.bg-effects {
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

.tech-grid-bg {
  position: absolute;
  inset: 0;
  background: 
    linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 40%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 40%, transparent 100%);
}

.noise-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.035;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  animation: noise-shift 0.5s steps(2) infinite;
}

@keyframes noise-shift {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-2px, 2px); }
}

.ambient-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
}

.ambient-glow--cyan {
  background: #00FFCC;
  top: -200px;
  right: -200px;
  animation: glow-float 8s ease-in-out infinite;
}

.ambient-glow--purple {
  background: #B026FF;
  bottom: -200px;
  left: -200px;
  animation: glow-float 10s ease-in-out infinite reverse;
}

@keyframes glow-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -30px) scale(1.1); }
}
</style>