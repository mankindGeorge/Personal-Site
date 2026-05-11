<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-brand">
          <span class="brand-text">George's<span class="highlight"> Personal Site</span></span>
          <p class="brand-desc">数据科学 & Web 开发</p>
        </div>

        <div class="footer-links">
          <div class="link-group">
            <h4 class="link-title">导航</h4>
            <router-link to="/" class="footer-link">首页</router-link>
            <router-link to="/docs" class="footer-link">文档</router-link>
            <router-link to="/announcements" class="footer-link">动态</router-link>
          </div>

          <div class="link-group">
            <h4 class="link-title">社交</h4>
            <a href="https://github.com/mankindGeorge" target="_blank" class="footer-link">GitHub</a>
            <div class="email-wrapper" @mouseenter="startTyping" @mouseleave="hideTooltip">
              <span class="footer-link email-link">邮箱</span>
              <transition name="tooltip">
                <div v-if="showTooltip" class="email-tooltip">
                  <div class="tooltip-content">
                    <span class="tooltip-label">邮箱</span>
                    <span class="tooltip-email">{{ displayedEmail }}</span>
                    <span v-if="isTyping" class="cursor-blink">|</span>
                  </div>
                  <button v-if="typingComplete" @click.stop="copyEmail" class="copy-btn">
                    点击复制
                  </button>
                </div>
              </transition>
            </div>
          </div>
        </div>

        <div class="footer-status">
          <div class="status-indicator">
            <span class="status-dot"></span>
            <span class="status-text">所有系统正常运行</span>
          </div>
          <p class="copyright">
            © {{ currentYear }} George. Built with
            <svg class="heart-icon" width="14" height="14" viewBox="0 0 24 24" fill="#00FFCC">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </p>
        </div>
      </div>

      <div class="footer-decoration">
        <svg width="100%" height="60" viewBox="0 0 1200 60" preserveAspectRatio="none">
          <path 
            d="M0,30 Q300,60 600,30 T1200,30" 
            fill="none" 
            stroke="url(#footerGrad)" 
            stroke-width="1"
            opacity="0.3"
          />
          <defs>
            <linearGradient id="footerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#00FFCC" />
              <stop offset="100%" stop-color="#B026FF" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
const EMAIL = 'mankindgeorge06@gmail.com'

const showTooltip = ref(false)
const displayedEmail = ref('')
const isTyping = ref(false)
const typingComplete = ref(false)
let typingInterval = null

const startTyping = () => {
  showTooltip.value = true
  displayedEmail.value = ''
  isTyping.value = true
  typingComplete.value = false
  
  let index = 0
  typingInterval = setInterval(() => {
    if (index < EMAIL.length) {
      displayedEmail.value += EMAIL[index]
      index++
    } else {
      clearInterval(typingInterval)
      isTyping.value = false
      typingComplete.value = true
    }
  }, 80)
}

const hideTooltip = () => {
  showTooltip.value = false
  if (typingInterval) {
    clearInterval(typingInterval)
  }
}

const copyEmail = () => {
  const textarea = document.createElement('textarea')
  textarea.value = EMAIL
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  textarea.style.top = '0'
  document.body.appendChild(textarea)
  textarea.focus()
  textarea.select()
  
  try {
    document.execCommand('copy')
  } catch (err) {
    console.warn('复制失败')
  }
  
  document.body.removeChild(textarea)
}
</script>

<style scoped>
.footer {
  background: #0A0A0A;
  border-top: 1px solid rgba(0, 255, 204, 0.1);
  padding: 4rem 2rem 2rem;
  position: relative;
  overflow: hidden;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.brand-text {
  font-family: 'Fira Code', monospace;
  font-size: 1.5rem;
  font-weight: 600;
  color: #E6EDF3;
}

.highlight {
  color: #00FFCC;
}

.brand-desc {
  color: #8B949E;
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  gap: 4rem;
  justify-content: center;
}

.link-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.link-title {
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  color: #00FFCC;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}

.footer-link {
  color: #8B949E;
  text-decoration: none;
  font-size: 0.9375rem;
  transition: all 0.3s ease;
}

.footer-link:hover {
  color: #E6EDF3;
}

.email-wrapper {
  position: relative;
  display: inline-block;
}

.email-link {
  cursor: pointer;
}

.email-tooltip {
  position: absolute;
  bottom: calc(100% + 10px);
  left: 50%;
  transform: translateX(-50%);
  background: rgba(13, 17, 23, 0.98);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 12px;
  padding: 1rem;
  min-width: 280px;
  z-index: 100;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.email-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 8px solid transparent;
  border-top-color: rgba(0, 255, 204, 0.2);
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.tooltip-label {
  font-family: 'Fira Code', monospace;
  font-size: 0.625rem;
  color: #00FFCC;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.tooltip-email {
  font-family: 'Fira Code', monospace;
  font-size: 0.9375rem;
  color: #E6EDF3;
  word-break: break-all;
}

.cursor-blink {
  color: #B026FF;
  animation: blink 0.8s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.copy-btn {
  width: 100%;
  padding: 0.5rem;
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  border: none;
  border-radius: 6px;
  color: #0A0A0A;
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.copy-btn:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
}

.tooltip-enter-active,
.tooltip-leave-active {
  transition: all 0.3s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(10px);
}

.footer-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #00FFCC;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  color: #8B949E;
}

.copyright {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: #8B949E;
}

.heart-icon {
  animation: heartbeat 1.5s ease-in-out infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.footer-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  pointer-events: none;
}

@media (max-width: 768px) {
  .footer {
    padding: 3rem 1.5rem 1.5rem;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }

  .footer-links {
    flex-direction: column;
    gap: 2rem;
  }

  .footer-status {
    align-items: center;
  }

  .email-tooltip {
    left: 0;
    transform: translateX(0);
  }

  .tooltip-enter-from,
  .tooltip-leave-to {
    transform: translateY(10px);
  }
}
</style>
