<template>
  <div class="page">
    <h3>个人信息</h3>
    <el-card style="max-width: 600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名"><el-input v-model="form.username" disabled /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" disabled /></el-form-item>
        <el-form-item label="昵称"><el-input v-model="form.nickname" /></el-form-item>
        <el-form-item label="手机号"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="简介"><el-input v-model="form.bio" type="textarea" /></el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const form = reactive({ username: '', email: '', nickname: '', phone: '', bio: '' })

onMounted(async () => {
  await userStore.fetchProfile()
  if (userStore.profile) {
    Object.assign(form, userStore.profile)
  }
})

async function handleSave() {
  await userStore.updateProfile({ nickname: form.nickname, phone: form.phone, bio: form.bio })
}
</script>
