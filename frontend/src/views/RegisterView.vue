<template>
  <div class="register-page">
    <el-card class="register-card">
      <h2 class="register-title">注册账号</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" show-password />
        </el-form-item>
        <el-form-item prop="nickname">
          <el-input v-model="form.nickname" placeholder="昵称（选填）" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" @click="handleRegister">注册</el-button>
        </el-form-item>
      </el-form>
      <div class="register-footer">
        <el-button text type="primary" @click="$router.push('/login')">已有账号？去登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, FormRules } from 'element-plus'

const auth = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({ username: '', email: '', password: '', nickname: '' })
const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }, { min: 3, max: 50, message: '长度 3-50', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少 6 位', trigger: 'blur' }],
}

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.register(form)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page { display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; }
.register-card { width: 420px; }
.register-title { text-align: center; margin-bottom: 24px; color: #409eff; }
.register-footer { text-align: center; }
</style>
