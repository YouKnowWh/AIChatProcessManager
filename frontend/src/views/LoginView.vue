<template>
  <div class="login-page">
    <div class="login-bg"></div>
    <el-card class="login-card" shadow="always">
      <div class="login-header">
        <el-icon :size="48" color="#409eff"><ChatDotRound /></el-icon>
        <h2>AIChatProcessManager</h2>
        <p class="subtitle">AI 会话过程管理系统</p>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" :prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" @click="handleLogin">
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="quick-login">
        <p class="quick-title">快速体验（点击切换角色）</p>
        <el-space wrap>
          <el-tag v-for="acc in testAccounts" :key="acc.role"
            :type="form.username === acc.username ? 'primary' : 'info'"
            class="quick-tag"
            @click="switchAccount(acc)">
            {{ acc.label }}
          </el-tag>
        </el-space>
      </div>

      <div class="login-footer">
        <el-button text type="primary" @click="$router.push('/register')">没有账号？去注册</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, shallowRef } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock, ChatDotRound } from '@element-plus/icons-vue'

const auth = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({ username: 'user1', password: 'user123' })

const testAccounts = [
  { label: '👤 普通用户 (user1)', username: 'user1', password: 'user123', role: 'user' },
  { label: '👤 普通用户 (user2)', username: 'user2', password: 'user456', role: 'user' },
  { label: '🔧 角色维护者 (manager)', username: 'manager', password: 'manager123', role: 'manager' },
  { label: '🛡️ 管理员 (admin)', username: 'admin', password: 'admin123', role: 'admin' },
]

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

function switchAccount(acc: typeof testAccounts[0]) {
  form.username = acc.username
  form.password = acc.password
}

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.login(form)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex; justify-content: center; align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}
.login-bg {
  position: absolute; inset: 0;
  background: radial-gradient(circle at 20% 50%, rgba(255,255,255,.08) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(255,255,255,.06) 0%, transparent 50%);
}
.login-card {
  width: 440px; position: relative; z-index: 1;
  border-radius: 12px;
}
.login-header { text-align: center; margin-bottom: 28px; }
.login-header h2 { margin: 12px 0 4px; color: #303133; font-size: 22px; }
.login-header .subtitle { margin: 0; color: #909399; font-size: 13px; }
.quick-login { margin: 16px 0; padding-top: 16px; border-top: 1px dashed #dcdfe6; }
.quick-title { margin: 0 0 10px; font-size: 12px; color: #909399; text-align: center; }
.quick-tag { cursor: pointer; }
.quick-tag:hover { opacity: .8; }
.login-footer { text-align: center; margin-top: 8px; }
</style>
