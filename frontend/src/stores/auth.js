import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('adminToken') || null)
  const isAuthenticated = ref(!!token.value)

  const login = async (password) => {
    try {
      const response = await authAPI.login(password)
      token.value = response.access_token
      localStorage.setItem('adminToken', response.access_token)
      isAuthenticated.value = true
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || '登录失败' }
    }
  }

  const logout = () => {
    token.value = null
    isAuthenticated.value = false
    authAPI.logout()
  }

  return {
    token,
    isAuthenticated,
    login,
    logout
  }
})
