import { defineStore } from 'pinia'
import { ref } from 'vue'
import { usersApi } from '@/api/users'
import type { UserInfo } from '@/types'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', () => {
  const profile = ref<UserInfo | null>(null)
  const loading = ref(false)

  async function fetchProfile() {
    loading.value = true
    try {
      const res = await usersApi.getMe()
      profile.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(data: Record<string, any>) {
    const res = await usersApi.updateMe(data)
    profile.value = res.data
    ElMessage.success('更新成功')
  }

  return { profile, loading, fetchProfile, updateProfile }
})
