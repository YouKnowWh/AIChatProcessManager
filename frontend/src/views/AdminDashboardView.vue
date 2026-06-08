<template>
  <div class="page">
    <h3>管理首页</h3>
    <el-row :gutter="20" v-loading="loading">
      <el-col :span="6" v-for="card in cards" :key="card.label">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon"><el-icon :size="28"><component :is="card.icon" /></el-icon></div>
          <div class="stat-body">
            <div class="stat-value">{{ card.value }}</div>
            <div class="stat-label">{{ card.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import { User, Service, ChatDotRound, Star, UserFilled } from '@element-plus/icons-vue'

const loading = ref(false)
const cards = ref([
  { label: '活跃用户', value: 0, icon: User },
  { label: 'AI 角色', value: 0, icon: Service },
  { label: '总消息', value: 0, icon: ChatDotRound },
  { label: '总反馈', value: 0, icon: Star },
])

onMounted(async () => {
  loading.value = true
  try {
    const res = await adminApi.getStats()
    const d = res.data
    cards.value[0].value = d.users?.total_active ?? 0
    cards.value[1].value = d.characters?.total ?? 0
    cards.value[2].value = d.messages?.total_normal ?? 0
    cards.value[3].value = (d.interactions?.total_likes ?? 0) + (d.interactions?.total_dislikes ?? 0) + (d.interactions?.total_text_feedbacks ?? 0)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stat-card { display: flex; align-items: center; gap: 16px; padding: 20px; }
.stat-icon { color: #409eff; }
.stat-body { flex: 1; }
.stat-value { font-size: 28px; font-weight: bold; color: #303133; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
</style>
