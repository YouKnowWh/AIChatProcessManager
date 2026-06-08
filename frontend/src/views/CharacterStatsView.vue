<template>
  <div class="page">
    <div class="page-header">
      <h3>角色统计 — {{ stats.character_name || '加载中...' }}</h3>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" v-loading="loading">
      <el-col :span="6" v-for="card in statCards" :key="card.label">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ card.value }}</div>
          <div class="stat-label">{{ card.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 反馈列表 -->
    <h4 style="margin-top: 32px;">用户反馈</h4>
    <el-table :data="feedbacks" stripe v-loading="fbLoading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="feedback_type" label="类型" width="80">
        <template #default="{ row }">
          <el-tag :type="row.feedback_type === 'like' ? 'success' : row.feedback_type === 'dislike' ? 'danger' : 'info'" size="small">
            {{ row.feedback_type === 'like' ? '👍 点赞' : row.feedback_type === 'dislike' ? '👎 点踩' : '💬 文字' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="内容" show-overflow-tooltip />
      <el-table-column prop="tags" label="标签" width="120" />
      <el-table-column prop="created_at" label="时间" width="170">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-if="fbTotal > 0"
      v-model:current-page="fbPage"
      :page-size="fbPageSize"
      :total="fbTotal"
      layout="prev, pager, next"
      style="margin-top: 16px; justify-content: flex-end"
      @current-change="loadFeedbacks"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { charactersApi } from '@/api/characters'

const route = useRoute()
const characterId = computed(() => Number(route.params.id))
const loading = ref(false)
const fbLoading = ref(false)

const stats = ref<Record<string, any>>({})

const statCards = computed(() => [
  { label: '使用次数', value: stats.value.usage_count ?? 0 },
  { label: '会话数', value: stats.value.conversation_count ?? 0 },
  { label: '消息数', value: stats.value.message_count ?? 0 },
  { label: '点赞 / 点踩', value: `${stats.value.like_count ?? 0} / ${stats.value.dislike_count ?? 0}` },
])

const feedbacks = ref<any[]>([])
const fbPage = ref(1)
const fbPageSize = ref(20)
const fbTotal = ref(0)

onMounted(async () => {
  loading.value = true
  try {
    const res = await charactersApi.getStats(characterId.value)
    stats.value = res.data
  } finally {
    loading.value = false
  }
  loadFeedbacks()
})

async function loadFeedbacks() {
  fbLoading.value = true
  try {
    const res = await charactersApi.getFeedbacks(characterId.value, { page: fbPage.value, page_size: fbPageSize.value })
    feedbacks.value = res.data.items
    fbTotal.value = res.data.total
  } finally {
    fbLoading.value = false
  }
}

function formatTime(ts: string) {
  return new Date(ts).toLocaleString('zh-CN')
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h3 { margin: 0; }
.stat-card { text-align: center; padding: 16px; }
.stat-value { font-size: 32px; font-weight: bold; color: #409eff; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
</style>
