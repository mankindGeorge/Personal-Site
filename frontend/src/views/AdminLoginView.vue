<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-header">
        <svg class="login-icon" width="48" height="48" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="8" fill="#00FFCC"/>
          <circle cx="25" cy="30" r="5" fill="#B026FF"/>
          <circle cx="75" cy="30" r="5" fill="#B026FF"/>
          <line x1="50" y1="50" x2="25" y2="30" stroke="#00FFCC" stroke-width="2"/>
          <line x1="50" y1="50" x2="75" y2="30" stroke="#00FFCC" stroke-width="2"/>
        </svg>
        <h1 class="login-title">管理员登录</h1>
        <p class="login-desc">请输入访问密码</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <div class="input-wrapper">
            <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <input 
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="输入密码..."
              class="password-input"
              :class="{ error: error }"
              autocomplete="current-password"
            />
            <button 
              type="button"
              class="toggle-password"
              @click="showPassword = !showPassword"
            >
              <svg v-if="!showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </button>
          </div>
          <p v-if="error" class="error-message">{{ error }}</p>
        </div>

        <button 
          type="submit" 
          class="login-btn"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner"></span>
          <span v-else>登录</span>
        </button>
      </form>

      <div class="login-footer">
        <router-link to="/" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          返回首页
        </router-link>
      </div>
    </div>

    <div class="login-bg">
      <div class="bg-grid"></div>
      <div class="bg-glow glow-1"></div>
      <div class="bg-glow glow-2"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!password.value) {
    error.value = '请输入密码'
    return
  }

  loading.value = true
  error.value = ''

  const result = await authStore.login(password.value)

  if (result.success) {
    router.push('/admin')
  } else {
    error.value = result.error
    password.value = ''
  }

  loading.value = false
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.login-container {
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 2;
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.login-icon {
  margin-bottom: 1.5rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.login-title {
  font-family: 'Fira Code', monospace;
  font-size: 1.75rem;
  color: #E6EDF3;
  margin-bottom: 0.5rem;
}

.login-desc {
  color: #8B949E;
  font-size: 0.9375rem;
}

.login-form {
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 10, 0.95));
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 16px;
  padding: 2rem;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #8B949E;
  pointer-events: none;
}

.password-input {
  width: 100%;
  padding: 1rem 3rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #E6EDF3;
  font-family: 'Fira Code', monospace;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s ease;
}

.password-input:focus {
  border-color: #00FFCC;
  box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
}

.password-input.error {
  border-color: #FF4757;
}

.password-input::placeholder {
  color: #8B949E;
}

.toggle-password {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: #8B949E;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.3s ease;
}

.toggle-password:hover {
  color: #00FFCC;
}

.error-message {
  color: #FF4757;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.login-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  border: none;
  border-radius: 8px;
  color: #0A0A0A;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 255, 204, 0.4);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top-color: #0A0A0A;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #8B949E;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: #00FFCC;
}

.login-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.bg-glow {
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.3;
}

.glow-1 {
  top: 10%;
  left: 20%;
  background: #00FFCC;
  animation: glowPulse 4s ease-in-out infinite;
}

.glow-2 {
  bottom: 10%;
  right: 20%;
  background: #B026FF;
  animation: glowPulse 4s ease-in-out infinite 2s;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.1); }
}
</style>
