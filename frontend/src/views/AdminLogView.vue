<template>
  <div class="page">
    <h3>系统日志</h3>
    <div class="filter-bar">
      <el-input v-model="filterUserId" placeholder="用户ID" clearable style="width:120px" @change="load" />
      <el-select v-model="filterAction" placeholder="操作类型" clearable @change="load" style="width: 160px">
        <el-option label="登录" value="login" />
        <el-option label="创建会话" value="create_conversation" />
        <el-option label="发送消息" value="send_message" />
        <el-option label="工具调用" value="tool_call" />
        <el-option label="消息过程链路" value="message_flow_trace" />
        <el-option label="隐藏消息" value="hide_message" />
      </el-select>
    </div>
    <el-table :data="logs" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户" width="100" />
      <el-table-column prop="action" label="操作" width="140">
        <template #default="{ row }">
          <el-tag :type="actionTag(row.action)" size="small">{{ actionLabel(row.action) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="target_type" label="对象类型" width="100" />
      <el-table-column prop="target_id" label="对象ID" width="70" />
      <el-table-column prop="detail" label="详情" show-overflow-tooltip min-width="200" />
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

const logs = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterUserId = ref('')
const filterAction = ref('')

onMounted(load)
async function load() {
  loading.value = true
  try {
    const params: any = { page: page.value, page_size: pageSize.value }
    if (filterAction.value) params.action = filterAction.value
    if (filterUserId.value) params.user_id = Number(filterUserId.value)
    const res = await adminApi.getLogs(params)
    logs.value = res.data.items
    total.value = res.data.total
  } finally { loading.value = false }
}
function fmt(ts: string) { return new Date(ts).toLocaleString('zh-CN') }
function actionLabel(a: string) {
  const m: Record<string,string> = { login:'登录', create_conversation:'创建会话', send_message:'发送消息', hide_message:'隐藏消息', tool_call:'工具调用', message_flow_trace:'消息过程链路' }
  return m[a] || a
}
function actionTag(a: string) {
  const m: Record<string,string> = { login:'', create_conversation:'success', send_message:'info', hide_message:'warning', tool_call:'', message_flow_trace:'primary' }
  return m[a] || ''
}
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
</style>
