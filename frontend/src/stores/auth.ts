import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/api/auth'
import router from '@/router'
import type { UserBrief, LoginRequest, RegisterRequest } from '@/types'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserBrief | null>(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref<string | null>(localStorage.getItem('token'))

  const isLoggedIn = () => !!token.value
  const isAdmin = () => user.value?.role === 'admin'
  const isManager = () => user.value?.role === 'character_manager' || user.value?.role === 'admin'

  async function login(data: LoginRequest) {
    const res = await authApi.login(data)
    const { access_token, user: userInfo } = res.data
    token.value = access_token
    user.value = userInfo
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(userInfo))
    ElMessage.closeAll()
    ElMessage.success({ message: '登录成功', duration: 1000, showClose: false })
    router.push(userInfo.role === 'admin' ? '/admin' : '/')
  }

  async function register(data: RegisterRequest) {
    const res = await authApi.register(data)
    const { access_token, user: userInfo } = res.data
    token.value = access_token
    user.value = userInfo
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(userInfo))
    ElMessage.closeAll()
    ElMessage.success({ message: '注册成功', duration: 1000, showClose: false })
    router.push('/')
  }

  async function refreshCurrentUser() {
    if (!token.value) return
    const res = await authApi.me()
    user.value = res.data
    localStorage.setItem('user', JSON.stringify(res.data))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  return { user, token, isLoggedIn, isAdmin, isManager, login, register, refreshCurrentUser, logout }
})
