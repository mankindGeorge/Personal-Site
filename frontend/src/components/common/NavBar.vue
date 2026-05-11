<template>
  <header 
    class="navbar"
    :class="{ 'navbar-scrolled': isScrolled }"
  >
    <div class="navbar-container">
      <router-link to="/" class="logo">
        <svg class="logo-icon" width="32" height="32" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="8" fill="#00FFCC"/>
          <circle cx="25" cy="30" r="5" fill="#B026FF"/>
          <circle cx="75" cy="30" r="5" fill="#B026FF"/>
          <line x1="50" y1="50" x2="25" y2="30" stroke="#00FFCC" stroke-width="2"/>
          <line x1="50" y1="50" x2="75" y2="30" stroke="#00FFCC" stroke-width="2"/>
        </svg>
        <span class="logo-text">George's<span class="highlight"> Personal Site</span></span>
      </router-link>

      <nav class="nav-links" :class="{ 'nav-active': mobileMenuOpen }">
        <router-link 
          v-for="link in navLinks" 
          :key="link.path"
          :to="link.path"
          class="nav-link"
          @click="closeMobileMenu"
        >
          <component :is="link.icon" class="nav-icon" />
          <span>{{ link.name }}</span>
        </router-link>
      </nav>

      <button class="mobile-menu-btn" @click="toggleMobileMenu">
        <span class="menu-line" :class="{ 'line-1-open': mobileMenuOpen }"></span>
        <span class="menu-line" :class="{ 'line-2-open': mobileMenuOpen }"></span>
        <span class="menu-line" :class="{ 'line-3-open': mobileMenuOpen }"></span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, h } from 'vue'

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const HomeIcon = () => h('svg', { 
  width: 18, 
  height: 18, 
  viewBox: '0 0 24 24', 
  fill: 'none', 
  stroke: 'currentColor', 
  strokeWidth: 2 
}, [
  h('path', { d: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }),
  h('polyline', { points: '9 22 9 12 15 12 15 22' })
])

const DocsIcon = () => h('svg', { 
  width: 18, 
  height: 18, 
  viewBox: '0 0 24 24', 
  fill: 'none', 
  stroke: 'currentColor', 
  strokeWidth: 2 
}, [
  h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
  h('polyline', { points: '14 2 14 8 20 8' }),
  h('line', { x1: '16', y1: '13', x2: '8', y2: '13' }),
  h('line', { x1: '16', y1: '17', x2: '8', y2: '17' })
])

const BellIcon = () => h('svg', { 
  width: 18, 
  height: 18, 
  viewBox: '0 0 24 24', 
  fill: 'none', 
  stroke: 'currentColor', 
  strokeWidth: 2 
}, [
  h('path', { d: 'M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9' }),
  h('path', { d: 'M13.73 21a2 2 0 0 1-3.46 0' })
])

const navLinks = [
  { path: '/', name: '首页', icon: HomeIcon },
  { path: '/docs', name: '文档', icon: DocsIcon },
  { path: '/announcements', name: '动态', icon: BellIcon }
]

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 1rem 2rem;
  transition: all 0.3s ease;
}

.navbar-scrolled {
  background: rgba(13, 17, 23, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: #E6EDF3;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.02);
}

.logo-icon {
  transition: all 0.3s ease;
  animation: logo-pulse 3s ease-in-out infinite;
}

.logo:hover .logo-icon {
  filter: drop-shadow(0 0 8px rgba(0, 255, 204, 0.6));
  animation: logo-glow 0.8s ease-in-out;
}

@keyframes logo-pulse {
  0%, 100% { filter: drop-shadow(0 0 2px rgba(0, 255, 204, 0.3)); }
  50% { filter: drop-shadow(0 0 8px rgba(0, 255, 204, 0.6)); }
}

@keyframes logo-glow {
  0% { filter: drop-shadow(0 0 2px rgba(0, 255, 204, 0.3)); }
  50% { filter: drop-shadow(0 0 20px rgba(0, 255, 204, 0.8)); }
  100% { filter: drop-shadow(0 0 8px rgba(0, 255, 204, 0.6)); }
}

.logo-text {
  font-family: 'Fira Code', monospace;
  font-size: 1.25rem;
  font-weight: 600;
}

.highlight {
  color: #00FFCC;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  color: #8B949E;
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(176, 38, 255, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-link:hover {
  color: #E6EDF3;
}

.nav-link:hover::before {
  opacity: 1;
}

.nav-link.router-link-active {
  color: #00FFCC;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #00FFCC, #B026FF);
  border-radius: 1px;
  box-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
  transform: translateX(-50%);
  transition: width 0.3s ease;
}

.nav-link:hover::after,
.nav-link.router-link-active::after {
  width: 60%;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.menu-line {
  display: block;
  width: 24px;
  height: 2px;
  background: #E6EDF3;
  border-radius: 1px;
  transition: all 0.3s ease;
}

.line-1-open {
  transform: translateY(7px) rotate(45deg);
  background: #00FFCC;
}

.line-2-open {
  opacity: 0;
}

.line-3-open {
  transform: translateY(-7px) rotate(-45deg);
  background: #00FFCC;
}

@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .nav-links {
    position: fixed;
    top: 0;
    right: -100%;
    width: 280px;
    height: 100vh;
    background: rgba(13, 17, 23, 0.98);
    backdrop-filter: blur(20px);
    flex-direction: column;
    justify-content: center;
    padding: 2rem;
    transition: right 0.3s ease;
    border-left: 1px solid rgba(0, 255, 204, 0.1);
  }

  .nav-active {
    right: 0;
  }

  .nav-link {
    width: 100%;
    justify-content: center;
    padding: 1rem;
    font-size: 1.125rem;
  }
}
</style>
