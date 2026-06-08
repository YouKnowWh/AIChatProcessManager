<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="admin-sidebar">
      <h3 class="admin-title" @click="$router.push('/admin')">管理后台</h3>
      <el-menu :default-active="route.path" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409eff">
        <el-menu-item index="/admin">
          <el-icon><DataAnalysis /></el-icon>
          <span>管理首页</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/characters">
          <el-icon><Service /></el-icon>
          <span>角色管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/messages">
          <el-icon><ChatLineSquare /></el-icon>
          <span>消息管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/feedbacks">
          <el-icon><Star /></el-icon>
          <span>反馈管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/logs">
          <el-icon><Document /></el-icon>
          <span>系统日志</span>
        </el-menu-item>
        <el-menu-item index="/admin/stats">
          <el-icon><TrendCharts /></el-icon>
          <span>系统统计</span>
        </el-menu-item>
        <el-menu-item index="/">
          <el-icon><Back /></el-icon>
          <span>返回前台</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="admin-header">
        <span class="admin-breadcrumb">管理后台</span>
        <el-button text @click="auth.logout()">退出</el-button>
      </el-header>
      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const route = useRoute()
const auth = useAuthStore()
</script>

<style scoped>
.admin-layout { height: 100vh; }
.admin-sidebar { background: #304156; overflow-y: auto; }
.admin-title { color: #fff; text-align: center; padding: 16px 0; margin: 0; cursor: pointer; font-size: 16px; border-bottom: 1px solid #4a5a6a; }
.admin-header { display: flex; align-items: center; justify-content: space-between; background: #fff; border-bottom: 1px solid #e4e7ed; }
.admin-main { background: #f0f2f5; min-height: calc(100vh - 60px); }
</style>
