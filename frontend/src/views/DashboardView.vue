<template>
  <div class="dashboard">
    <h3>数据概览</h3>
    <el-row :gutter="20">
      <el-col :span="6" v-for="card in cards" :key="card.label">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ card.value }}</div>
          <div class="stat-label">{{ card.label }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { statsApi } from '@/api/stats'

const cards = ref([
  { label: '会话数', value: 0 },
  { label: '消息数', value: 0 },
  { label: '收藏数', value: 0 },
  { label: '反馈数', value: 0 },
])

onMounted(async () => {
  try {
    const res = await statsApi.getMyStats()
    const d = res.data
    cards.value[0].value = d.conversation_count
    cards.value[1].value = d.message_count
    cards.value[2].value = d.favorite_count
    cards.value[3].value = d.feedback_count
  } catch { /* ignore */ }
})
</script>

<style scoped>
.stat-card { text-align: center; padding: 16px; }
.stat-value { font-size: 36px; font-weight: bold; color: #409eff; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
</style>
