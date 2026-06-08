<template>
  <el-container class="main-layout">
    <el-header class="main-header">
      <div class="header-left">
        <h2 class="logo" @click="$router.push('/')">AIChat Manager</h2>
      </div>
      <div class="header-right">
        <el-button text @click="$router.push('/characters')">AI 角色</el-button>
        <el-button text @click="$router.push('/conversations')">会话</el-button>
        <el-button text @click="$router.push('/favorites')">收藏</el-button>
        <el-dropdown v-if="auth.user" trigger="click">
          <span class="user-info">
            <el-avatar :size="32" :src="auth.user.avatar" />
            <span class="username">{{ auth.user.nickname || auth.user.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/profile')">个人信息</el-dropdown-item>
              <el-dropdown-item v-if="auth.isManager()" @click="$router.push('/characters/manage')">角色管理</el-dropdown-item>
              <el-dropdown-item v-if="auth.isAdmin()" @click="$router.push('/admin')">系统管理</el-dropdown-item>
              <el-dropdown-item divided @click="auth.logout()">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
</script>

<style scoped>
.main-layout { height: 100vh; display: flex; flex-direction: column; }
.main-header { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #e4e7ed; background: #fff; padding: 0 20px; }
.header-left .logo { cursor: pointer; color: #409eff; margin: 0; }
.header-right { display: flex; align-items: center; gap: 8px; }
.user-info { display: flex; align-items: center; gap: 8px; cursor: pointer; }
</style>
