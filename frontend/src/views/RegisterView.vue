<template>
  <div class="register-page">
    <div class="register-bg"></div>
    <el-card class="register-card" shadow="always">
      <div class="register-header">
        <el-icon :size="40" color="#409eff"><UserFilled /></el-icon>
        <h2>注册账号</h2>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名（3-50 字符）" :prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱地址" :prefix-icon="Message" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码（至少 6 位）" :prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" :prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="nickname">
          <el-input v-model="form.nickname" placeholder="昵称（选填）" :prefix-icon="Edit" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" @click="handleRegister">
            {{ loading ? '注册中...' : '注 册' }}
          </el-button>
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
import { User, Lock, Message, Edit, UserFilled } from '@element-plus/icons-vue'

const auth = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  nickname: '',
})

const validateConfirm = (_rule: any, value: string, cb: any) => {
  if (value !== form.password) cb(new Error('两次密码输入不一致'))
  else cb()
}

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '长度 3-50 字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' },
  ],
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
.register-page {
  display: flex; justify-content: center; align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  position: relative; overflow: hidden;
}
.register-bg {
  position: absolute; inset: 0;
  background: radial-gradient(circle at 80% 20%, rgba(255,255,255,.1) 0%, transparent 50%);
}
.register-card { width: 440px; position: relative; z-index: 1; border-radius: 12px; }
.register-header { text-align: center; margin-bottom: 24px; }
.register-header h2 { margin: 8px 0 0; color: #303133; }
.register-footer { text-align: center; margin-top: 8px; }
</style>
