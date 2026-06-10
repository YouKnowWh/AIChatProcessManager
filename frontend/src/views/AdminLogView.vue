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
        <el-option label="知识库调用" value="knowledge_call" />
        <el-option label="消息过程链路" value="message_flow_trace" />
        <el-option label="隐藏消息" value="hide_message" />
      </el-select>
    </div>
    <el-table :data="logs" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户" width="100" />
      <el-table-column prop="action" label="操作" width="150">
        <template #default="{ row }">
          <el-tag :type="actionTag(row.action)" size="small">{{ actionLabel(row.action) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="target_type" label="对象类型" width="110" />
      <el-table-column prop="target_id" label="对象ID" width="70" />
      <el-table-column label="详情" min-width="200">
        <template #default="{ row }">
          <span class="detail-preview" @click="showDetail(row)">{{ (row.detail || '').substring(0, 80) }}{{ (row.detail || '').length > 80 ? '...' : '' }}</span>
          <el-button v-if="(row.detail || '').length > 80" text size="small" type="primary" @click="showDetail(row)">展开</el-button>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="时间" width="170">
        <template #default="{ row }">{{ fmt(row.created_at) }}</template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="page" :page-size="pageSize" :total="total" layout="prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="load" />

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="日志详情" width="750px" top="5vh">
      <div v-if="detailRow">
        <el-descriptions :column="2" border size="small" style="margin-bottom:16px">
          <el-descriptions-item label="日志ID">{{ detailRow.id }}</el-descriptions-item>
          <el-descriptions-item label="用户">{{ detailRow.username }}</el-descriptions-item>
          <el-descriptions-item label="操作">{{ actionLabel(detailRow.action) }}</el-descriptions-item>
          <el-descriptions-item label="时间">{{ fmt(detailRow.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="对象类型">{{ detailRow.target_type || '-' }}</el-descriptions-item>
          <el-descriptions-item label="对象ID">{{ detailRow.target_id ?? '-' }}</el-descriptions-item>
        </el-descriptions>
        <h4>完整内容</h4>
        <template v-if="isFlowTrace">
          <div v-for="(step, i) in flowSteps" :key="i" class="flow-step">
            <div class="flow-step-header">
              <el-tag size="small" type="primary">Step {{ i + 1 }}</el-tag>
              <strong>{{ step.stage }}</strong>
              <span class="flow-table">{{ step.table }}</span>
            </div>
            <div class="flow-step-summary">{{ step.summary }}</div>
            <div v-if="step.extra" class="flow-step-extra">
              <div v-for="(v, k) in step.extra" :key="k" class="flow-kv">
                <span class="flow-key">{{ k }}</span>: <span class="flow-val">{{ v }}</span>
              </div>
            </div>
          </div>
        </template>
        <pre v-else class="detail-json">{{ formattedDetail }}</pre>
      </div>
      <template #footer><el-button @click="detailVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const logs = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterUserId = ref('')
const filterAction = ref('')

const detailVisible = ref(false)
const detailRow = ref<any>(null)

const isFlowTrace = computed(() => detailRow.value?.action === 'message_flow_trace')
const flowSteps = computed(() => {
  if (!detailRow.value?.detail) return []
  try { return JSON.parse(detailRow.value.detail).steps || [] } catch { return [] }
})
const formattedDetail = computed(() => {
  if (!detailRow.value?.detail) return ''
  try { return JSON.stringify(JSON.parse(detailRow.value.detail), null, 2) } catch { return detailRow.value.detail }
})

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
function showDetail(row: any) { detailRow.value = row; detailVisible.value = true }
function fmt(ts: string) { return new Date(ts).toLocaleString('zh-CN') }
function actionLabel(a: string) {
  const m: Record<string,string> = { login:'登录', create_conversation:'创建会话', send_message:'发送消息', hide_message:'隐藏消息', tool_call:'工具调用', knowledge_call:'知识库调用', message_flow_trace:'消息过程链路' }
  return m[a] || a
}
function actionTag(a: string) {
  const m: Record<string,string> = { login:'', create_conversation:'success', send_message:'info', hide_message:'warning', tool_call:'', knowledge_call:'success', message_flow_trace:'primary' }
  return m[a] || ''
}
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
.detail-preview { cursor: pointer; color: #606266; font-size: 12px; }
.detail-preview:hover { color: #409eff; }
.detail-json { background: #f5f7fa; border-radius: 6px; padding: 12px; font-size: 12px; overflow-x: auto; max-height: 500px; overflow-y: auto; white-space: pre-wrap; word-break: break-all; }
.flow-step { background: #fafafa; border: 1px solid #ebeef5; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.flow-step-header { display: flex; gap: 10px; align-items: center; margin-bottom: 6px; }
.flow-table { color: #909399; font-size: 12px; }
.flow-step-summary { font-size: 13px; color: #303133; margin-bottom: 6px; }
.flow-step-extra { display: flex; flex-wrap: wrap; gap: 4px 16px; font-size: 12px; }
.flow-kv { color: #606266; }
.flow-key { color: #909399; }
.flow-val { color: #303133; font-weight: 500; }
</style>
