import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  // 公共
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guest: true },
  },
  // 用户端（MainLayout）
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'characters', name: 'Characters', component: () => import('@/views/CharacterListView.vue') },
      { path: 'conversations', name: 'Conversations', component: () => import('@/views/ConversationListView.vue') },
      { path: 'chat/:id', name: 'Chat', component: () => import('@/views/ChatView.vue'), props: true },
      { path: 'search', name: 'MessageSearch', component: () => import('@/views/MessageSearchView.vue') },
      { path: 'favorites', name: 'Favorites', component: () => import('@/views/FavoriteView.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/ProfileView.vue') },
      // 知识库
      { path: 'knowledge', name: 'Knowledge', component: () => import('@/views/KnowledgeView.vue') },
      // 角色管理（弹窗模式）
      { path: 'characters/manage', name: 'CharacterManage', component: () => import('@/views/CharacterManageView.vue') },
    ],
  },
  // 管理端（AdminLayout）
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { role: 'admin' },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('@/views/AdminDashboardView.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('@/views/AdminUserView.vue') },
      { path: 'characters', name: 'AdminCharacters', component: () => import('@/views/AdminCharacterView.vue') },
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

// 路由守卫 — JWT 鉴权 + 角色控制
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null

  if (to.meta.guest) {
    // 已登录用户访问登录/注册页 → 管理员跳转后台，普通用户跳首页
    if (token) return next(user?.role === 'admin' ? '/admin' : '/')
    return next()
  }

  // 需要登录
  if (!token) return next('/login')

  // 管理员强制进入系统管理界面
  if (user?.role === 'admin' && !to.path.startsWith('/admin')) {
    return next('/admin')
  }

  // 角色控制：admin 进入管理端，普通用户进入前台功能
  const requiredRole = to.meta.role as string | undefined
  if (requiredRole && !hasRole(user?.role, requiredRole)) {
    return next('/')
  }

  next()
})

function hasRole(userRole: string | undefined, requiredRole: string): boolean {
  if (!userRole) return false
  if (userRole === 'admin') return true
  return userRole === requiredRole
}

export default router
