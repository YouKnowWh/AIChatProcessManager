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
    ElMessage.success('登录成功')
    router.push('/')
  }

  async function register(data: RegisterRequest) {
    const res = await authApi.register(data)
    const { access_token, user: userInfo } = res.data
    token.value = access_token
    user.value = userInfo
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(userInfo))
    ElMessage.success('注册成功')
    router.push('/')
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  return { user, token, isLoggedIn, isAdmin, isManager, login, register, logout }
})
