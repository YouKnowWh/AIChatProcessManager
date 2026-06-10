<template>
  <div class="page">
    <h3>系统统计</h3>
    <div v-loading="loading">
      <!-- 概览卡片 -->
      <el-row :gutter="20">
        <el-col :span="6" v-for="card in overviewCards" :key="card.label">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-value">{{ card.value }}</div>
            <div class="stat-label">{{ card.label }}</div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 排行 -->
      <el-row :gutter="20" style="margin-top: 24px">
        <el-col :span="12">
          <el-card>
            <template #header><strong>🏆 最受欢迎角色 Top 5</strong></template>
            <el-table :data="stats.top_characters || []" size="small">
              <el-table-column type="index" label="#" width="40" />
              <el-table-column prop="name" label="角色名" />
              <el-table-column prop="usage_count" label="使用次数" width="90" />
            </el-table>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header><strong>💬 最活跃用户 Top 5</strong></template>
            <el-table :data="stats.top_users || []" size="small">
              <el-table-column type="index" label="#" width="40" />
              <el-table-column prop="username" label="用户名" />
              <el-table-column prop="message_count" label="消息数" width="90" />
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import request from '@/api/request'

const stats = ref<Record<string, any>>({})
const loading = ref(false)

const overviewCards = computed(() => [
  { label: '活跃用户', value: stats.value.users?.total_active ?? 0 },
  { label: '禁用用户', value: stats.value.users?.total_disabled ?? 0 },
  { label: '角色 (启用/禁用)', value: `${stats.value.characters?.active ?? 0} / ${stats.value.characters?.disabled ?? 0}` },
  { label: '会话 (活跃/归档)', value: `${stats.value.conversations?.total_active ?? 0} / ${stats.value.conversations?.archived ?? 0}` },
  { label: '正常消息', value: stats.value.messages?.total_normal ?? 0 },
  { label: '隐藏消息', value: stats.value.messages?.hidden ?? 0 },
  { label: '收藏 / 点赞 / 点踩', value: `${stats.value.interactions?.total_favorites ?? 0} / ${stats.value.interactions?.total_likes ?? 0} / ${stats.value.interactions?.total_dislikes ?? 0}` },
  { label: '文字反馈', value: stats.value.interactions?.total_text_feedbacks ?? 0 },
])

onMounted(async () => {
  loading.value = true
  try {
    const res = await adminApi.getStats()
    stats.value = res.data
  } finally { loading.value = false }
})
})
</script>

<style scoped>
.stat-card { text-align: center; padding: 16px; }
.stat-value { font-size: 28px; font-weight: bold; color: #409eff; }
.stat-label { font-size: 13px; color: #909399; margin-top: 6px; }
</style>
