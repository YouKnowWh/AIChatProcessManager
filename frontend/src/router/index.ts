import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: () => import('@/views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterView.vue'), meta: { guest: true } },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'chat/:id?', name: 'Chat', component: () => import('@/views/ChatView.vue'), props: true },
      { path: 'search', name: 'MessageSearch', component: () => import('@/views/MessageSearchView.vue') },
      { path: 'favorites', name: 'Favorites', component: () => import('@/views/FavoriteView.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/ProfileView.vue') },
    ],
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { role: 'admin' },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('@/views/AdminDashboardView.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('@/views/AdminUserView.vue') },
      { path: 'messages', name: 'AdminMessages', component: () => import('@/views/AdminMessageView.vue') },
      { path: 'feedbacks', name: 'AdminFeedbacks', component: () => import('@/views/AdminFeedbackView.vue') },
      { path: 'logs', name: 'AdminLogs', component: () => import('@/views/AdminLogView.vue') },
      { path: 'message-flows', name: 'AdminMessageFlows', component: () => import('@/views/AdminMessageFlowView.vue') },
      { path: 'stats', name: 'AdminStats', component: () => import('@/views/AdminStatsView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null

  if (to.meta.guest) {
    if (token) return next(user?.role === 'admin' ? '/admin' : '/')
    return next()
  }
  if (!token) return next('/login')
  if (user?.role === 'admin' && !to.path.startsWith('/admin')) return next('/admin')
  const requiredRole = to.meta.role as string | undefined
  if (requiredRole && user?.role !== requiredRole && user?.role !== 'admin') return next('/')
  next()
})

export default router
