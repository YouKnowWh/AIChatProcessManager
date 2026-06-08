<template>
  <el-container class="main-layout">
    <el-header class="main-header">
      <div class="header-left">
        <el-icon :size="24" color="#409eff" class="logo-icon" @click="$router.push('/')"><ChatDotRound /></el-icon>
        <h2 class="logo" @click="$router.push('/')">AIChat Manager</h2>
      </div>

      <div class="header-center">
        <el-menu :default-active="route.path" mode="horizontal" router :ellipsis="false" class="header-menu">
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/characters">
            <el-icon><Service /></el-icon>
            <span>AI 角色</span>
          </el-menu-item>
          <el-menu-item index="/favorites">
            <el-icon><Star /></el-icon>
            <span>收藏</span>
          </el-menu-item>
          <el-menu-item index="/conversations">
            <el-icon><ChatLineSquare /></el-icon>
            <span>会话管理</span>
          </el-menu-item>
          <el-menu-item index="/characters/manage">
            <el-icon><Setting /></el-icon>
            <span>角色管理</span>
          </el-menu-item>
          <el-menu-item v-if="auth.isAdmin()" index="/admin">
            <el-icon><Monitor /></el-icon>
            <span>系统管理</span>
          </el-menu-item>
        </el-menu>
      </div>

      <div class="header-right">
        <el-badge :value="0" :hidden="true">
          <el-button circle :icon="Bell" text />
        </el-badge>

        <el-dropdown v-if="auth.user" trigger="click">
          <span class="user-info">
            <el-avatar :size="34" :src="auth.user.avatar" :icon="UserFilled" />
            <span class="username">{{ auth.user.nickname || auth.user.username }}</span>
            <el-tag size="small" :type="roleTagType(auth.user.role)" effect="light">{{ roleLabel(auth.user.role) }}</el-tag>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>
                <div class="user-dropdown-header">
                  <el-avatar :size="40" :src="auth.user.avatar" :icon="UserFilled" />
                  <div>
                    <div class="drop-name">{{ auth.user.nickname || auth.user.username }}</div>
                    <div class="drop-role">{{ roleLabel(auth.user.role) }}</div>
                  </div>
                </div>
              </el-dropdown-item>
              <el-divider style="margin: 4px 0" />
              <el-dropdown-item @click="$router.push('/profile')">
                <el-icon><User /></el-icon>个人信息
              </el-dropdown-item>
              <el-dropdown-item @click="$router.push('/characters/manage')">
                <el-icon><Setting /></el-icon>角色管理
              </el-dropdown-item>
              <el-dropdown-item v-if="auth.isAdmin()" @click="$router.push('/admin')">
                <el-icon><Monitor /></el-icon>系统管理
              </el-dropdown-item>
              <el-divider style="margin: 4px 0" />
              <el-dropdown-item @click="auth.logout()">
                <el-icon><SwitchButton /></el-icon>退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-main class="main-content">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  ChatDotRound, HomeFilled, Service, ChatLineSquare, Star,
  Bell, UserFilled, ArrowDown, User, Setting, Monitor, SwitchButton,
} from '@element-plus/icons-vue'

const route = useRoute()
const auth = useAuthStore()

onMounted(() => {
  auth.refreshCurrentUser().catch(() => {
    auth.logout()
  })
})

function roleLabel(role: string): string {
  const map: Record<string, string> = { admin: '管理员', character_manager: '角色维护者', user: '普通用户' }
  return map[role] || role
}

function roleTagType(role: string): 'danger' | 'warning' | 'info' {
  if (role === 'admin') return 'danger'
  return 'info'
}
</script>

<style scoped>
.main-layout { height: 100vh; display: flex; flex-direction: column; }
.main-header {
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid #e4e7ed; background: #fff; padding: 0 24px;
  height: 60px; box-shadow: 0 1px 4px rgba(0,0,0,.04);
}
.header-left { display: flex; align-items: center; gap: 10px; }
.logo-icon { cursor: pointer; }
.logo { cursor: pointer; color: #303133; margin: 0; font-size: 18px; white-space: nowrap; }
.header-center { flex: 1; display: flex; justify-content: center; }
.header-menu { border-bottom: none !important; }
.header-menu .el-menu-item { height: 60px; line-height: 60px; }
.header-right { display: flex; align-items: center; gap: 12px; }
.user-info { display: flex; align-items: center; gap: 8px; cursor: pointer; padding: 4px 8px; border-radius: 6px; }
.user-info:hover { background: #f5f7fa; }
.username { font-size: 14px; color: #303133; }
.main-content { background: #f5f7fa; padding: 24px; overflow-y: auto; }
.user-dropdown-header { display: flex; align-items: center; gap: 12px; padding: 4px 0; }
.drop-name { font-size: 14px; font-weight: 600; color: #303133; }
.drop-role { font-size: 12px; color: #909399; }
</style>
