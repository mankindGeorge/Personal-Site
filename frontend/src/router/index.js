import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/docs',
    name: 'Docs',
    component: () => import('../views/DocsView.vue')
  },
  {
    path: '/docs/:slug',
    name: 'DocDetail',
    component: () => import('../views/DocsView.vue')
  },
  {
    path: '/announcements',
    name: 'Announcements',
    component: () => import('../views/AnnouncementsView.vue')
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/AdminLoginView.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/AdminDashboardView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const isAuthenticated = localStorage.getItem('adminToken')
    if (!isAuthenticated) {
      next({ name: 'AdminLogin' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
