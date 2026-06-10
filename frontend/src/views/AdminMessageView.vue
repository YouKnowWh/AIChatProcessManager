<template>
  <div class="page">
    <h3>消息管理</h3>
    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态" clearable @change="load" style="width: 130px">
        <el-option label="正常" value="normal" />
        <el-option label="已隐藏" value="hidden" />
        <el-option label="已删除" value="deleted" />
      </el-select>
      <el-select v-model="filterSender" placeholder="发送者" clearable @change="load" style="width: 130px">
        <el-option label="用户" value="user" />
        <el-option label="AI" value="ai" />
      </el-select>
    </div>
    <el-table :data="messages" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="conversation_id" label="会话ID" width="70" />
      <el-table-column prop="sender_type" label="发送者" width="70" />
      <el-table-column prop="role" label="角色" width="90">
        <template #default="{ row }">
          <el-tag :type="row.sender_type === 'ai' ? 'success' : ''" size="small">{{ row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'normal' ? 'success' : row.status === 'hidden' ? 'warning' : 'danger'" size="small">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="时间" width="170">
        <template #default="{ row }">{{ fmt(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="160">
        <template #default="{ row }">
          <el-button v-if="row.status === 'normal'" text type="warning" size="small" @click="hideMsg(row)">隐藏</el-button>
          <el-button v-if="row.status === 'hidden'" text type="success" size="small" @click="restoreMsg(row)">恢复</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="page" :page-size="pageSize" :total="total" layout="prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="load" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminApi } from '@/api/admin'

const messages = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterStatus = ref('')
const filterSender = ref('')

onMounted(load)
async function load() {
  loading.value = true
  try {
    const params: any = { page: page.value, page_size: pageSize.value }
    if (filterStatus.value) params.status = filterStatus.value
    if (filterSender.value) params.sender_type = filterSender.value
    const res = await adminApi.getMessages(params)
    messages.value = res.data.items
    total.value = res.data.total
  } finally { loading.value = false }
}
async function hideMsg(row: any) { await adminApi.hideMessage(row.id); ElMessage.success('已隐藏'); load() }
async function restoreMsg(row: any) { await adminApi.restoreMessage(row.id); ElMessage.success('已恢复'); load() }
function fmt(ts: string) { return new Date(ts).toLocaleString('zh-CN') }
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
</style>
