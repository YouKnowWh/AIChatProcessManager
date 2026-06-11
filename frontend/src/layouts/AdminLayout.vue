<template>
  <el-container class="admin-layout">
    <el-aside :width="collapsed ? '64px' : '220px'" class="admin-sidebar" :class="{ collapsed }">
      <div class="admin-logo" @click="$router.push('/admin')">
        <el-icon :size="22" color="#fff"><Monitor /></el-icon>
        <span v-show="!collapsed" class="logo-text">管理后台</span>
      </div>
      <el-menu
        :default-active="route.path"
        router
        :collapse="collapsed"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
        class="sidebar-menu"
      >
        <el-menu-item index="/admin">
          <el-icon><HomeFilled /></el-icon>
          <span>管理首页</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/messages">
          <el-icon><ChatDotRound /></el-icon>
          <span>消息管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/feedbacks">
          <el-icon><StarFilled /></el-icon>
          <span>反馈管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/logs">
          <el-icon><Document /></el-icon>
          <span>系统日志</span>
        </el-menu-item>
        <el-menu-item index="/admin/message-flows">
          <el-icon><Connection /></el-icon>
          <span>消息过程日志</span>
        </el-menu-item>
        <el-menu-item index="/admin/stats">
          <el-icon><DataAnalysis /></el-icon>
          <span>系统统计</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="admin-header">
        <div class="header-left">
          <el-button :icon="collapsed ? Expand : Fold" text @click="collapsed = !collapsed" />
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin' }">管理后台</el-breadcrumb-item>
            <el-breadcrumb-item v-if="route.meta.title">{{ route.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-tag>{{ roleLabel(auth.user?.role || '') }}</el-tag>
          <el-button text @click="auth.logout()">退出</el-button>
        </div>
      </el-header>
      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  Monitor, HomeFilled, User, ChatDotRound, StarFilled,
  Document, DataAnalysis, Expand, Fold, Connection,
} from '@element-plus/icons-vue'

const route = useRoute()
const auth = useAuthStore()
const collapsed = ref(false)

function roleLabel(role: string): string {
  const map: Record<string, string> = { admin: '管理员', user: '普通用户' }
  return map[role] || role
}
</script>

<style scoped>
.admin-layout { height: 100vh; }
.admin-sidebar {
  background: #304156; overflow-y: auto; overflow-x: hidden;
  transition: width .3s;
  display: flex; flex-direction: column;
}
.admin-sidebar.collapsed { width: 64px !important; }
.sidebar-menu { border-right: none; flex: 1; }
.admin-logo {
  display: flex; align-items: center; gap: 8px; padding: 16px;
  cursor: pointer; border-bottom: 1px solid #4a5a6a;
  white-space: nowrap;
}
.logo-text { color: #fff; font-size: 15px; font-weight: 600; }
.admin-header {
  display: flex; align-items: center; justify-content: space-between;
  background: #fff; border-bottom: 1px solid #e4e7ed; padding: 0 20px;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.header-right { display: flex; align-items: center; gap: 12px; }
.admin-main { background: #f0f2f5; min-height: calc(100vh - 60px); padding: 20px; }
</style>
