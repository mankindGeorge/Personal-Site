import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('adminToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('adminToken')
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

export const docsAPI = {
  getAll: () => api.get('/api/docs'),
  getBySlug: (slug) => api.get(`/api/docs/${slug}`),
  create: (data) => api.post('/api/docs', data),
  update: (id, data) => api.put(`/api/docs/${id}`, data),
  delete: (id) => api.delete(`/api/docs/${id}`)
}

export const announcementsAPI = {
  getAll: () => api.get('/api/announcements'),
  create: (data) => api.post('/api/announcements', data),
  update: (id, data) => api.put(`/api/announcements/${id}`, data),
  delete: (id) => api.delete(`/api/announcements/${id}`)
}

export const authAPI = {
  login: (password) => api.post('/api/auth/login', { password }),
  logout: () => {
    localStorage.removeItem('adminToken')
  }
}

export default api
