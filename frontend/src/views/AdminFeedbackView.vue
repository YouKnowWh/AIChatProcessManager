<template>
  <div class="page">
    <h3>反馈管理</h3>
    <div class="filter-bar">
      <el-select v-model="filterType" placeholder="反馈类型" clearable @change="load" style="width: 130px">
        <el-option label="点赞" value="like" />
        <el-option label="点踩" value="dislike" />
        <el-option label="文字" value="text" />
      </el-select>
    </div>
    <el-table :data="feedbacks" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="user_id" label="用户ID" width="70" />
      <el-table-column prop="message_id" label="消息ID" width="70" />
      <el-table-column prop="character_id" label="角色ID" width="70" />
      <el-table-column prop="feedback_type" label="类型" width="80">
        <template #default="{ row }">
          <el-tag :type="row.feedback_type === 'like' ? 'success' : row.feedback_type === 'dislike' ? 'danger' : 'info'" size="small">{{ row.feedback_type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="内容" show-overflow-tooltip />
      <el-table-column prop="tags" label="标签" width="100" />
      <el-table-column prop="created_at" label="时间" width="170">
        <template #default="{ row }">{{ fmt(row.created_at) }}</template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="page" :page-size="pageSize" :total="total" layout="prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="load" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const feedbacks = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterType = ref('')

onMounted(load)
async function load() {
  loading.value = true
  try {
    const params: any = { page: page.value, page_size: pageSize.value }
    if (filterType.value) params.feedback_type = filterType.value
    const res = await adminApi.getFeedbacks(params)
    feedbacks.value = res.data.items
    total.value = res.data.total
  } finally { loading.value = false }
}
function fmt(ts: string) { return new Date(ts).toLocaleString('zh-CN') }
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
</style>
