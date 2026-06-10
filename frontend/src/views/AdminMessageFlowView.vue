<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h3>消息过程日志</h3>
        <p>展示一次消息发送过程中各个消息块写入的数据表与顺序</p>
      </div>
      <div class="actions">
        <el-switch v-model="autoRefresh" active-text="自动刷新" />
        <el-button type="primary" @click="load">刷新</el-button>
      </div>
    </div>

    <el-empty v-if="!loading && !flows.length" description="暂无过程日志" />

    <div v-loading="loading" class="flow-list">
      <el-card v-for="flow in flows" :key="flow.traceId" class="flow-card" shadow="hover">
        <template #header>
          <div class="flow-header">
            <div>
              <div class="flow-title">Trace {{ flow.traceId }}</div>
              <div class="flow-meta">
                会话 {{ flow.conversationId }} / 角色 {{ flow.characterName || '-' }}
                <span v-if="flow.model"> / {{ flow.model }} {{ flow.totalTokens }}tokens {{ flow.duration }}ms</span>
              </div>
            </div>
            <div v-if="flow.userContent" class="flow-context">
              <div class="context-label">用户：</div><div class="context-text">{{ flow.userContent }}</div>
            </div>
            <div v-if="flow.aiPreview" class="flow-context">
              <div class="context-label">AI：</div><div class="context-text">{{ flow.aiPreview }}</div>
            </div>
            <div class="flow-time">{{ formatTime(flow.createdAt) }}</div>
          </div>
        </template>

        <el-timeline>
          <el-timeline-item
            v-for="(step, index) in flow.steps"
            :key="flow.traceId + '-' + index"
            :timestamp="step.table"
            placement="top"
            type="primary"
          >
            <div class="step-title">{{ step.summary }}</div>
            <pre class="step-extra">{{ formatExtra(step.extra) }}</pre>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { adminApi } from '@/api/admin'

type FlowStep = {
  stage: string
  table: string
  summary: string
  extra?: Record<string, unknown>
}

type FlowItem = {
  traceId: string
  conversationId: number
  userMessageId: number
  aiMessageId: number
  createdAt: string
  steps: FlowStep[]
}

const loading = ref(false)
const flows = ref<FlowItem[]>([])
const autoRefresh = ref(true)

let timer: number | null = null

onMounted(() => {
  load()
  timer = window.setInterval(() => {
    if (autoRefresh.value) load()
  }, 3000)
})

onBeforeUnmount(() => {
  if (timer) window.clearInterval(timer)
})

async function load() {
  loading.value = true
  try {
    const res = await adminApi.getLogs({ page: 1, page_size: 10, action: 'message_flow_trace' })
    flows.value = (res.data.items || []).map((item: any) => {
      const detail = safeJson(item.detail)
      return {
        traceId: detail.trace_id || `log-${item.id}`,
        conversationId: detail.conversation_id,
        userMessageId: detail.user_message_id,
        aiMessageId: detail.ai_message_id,
        characterName: detail.character_name || '',
        userContent: detail.user_content || '',
        aiPreview: detail.ai_content_preview || '',
        model: detail.model || '',
        totalTokens: detail.total_tokens || '',
        duration: detail.duration_ms || '',
        createdAt: item.created_at,
        steps: detail.steps || [],
      }
    })
  } finally {
    loading.value = false
  }
}

function safeJson(value: string) {
  try {
    return JSON.parse(value || '{}')
  } catch {
    return {}
  }
}

function formatTime(ts: string) {
  return new Date(ts).toLocaleString('zh-CN')
}

function formatExtra(extra?: Record<string, unknown>) {
  return JSON.stringify(extra || {}, null, 2)
}
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
  gap: 16px;
}

.page-header h3 {
  margin: 0 0 6px;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 13px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.flow-list {
  display: grid;
  gap: 16px;
}

.flow-card {
  border-radius: 8px;
}

.flow-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: baseline;
}

.flow-title {
  font-weight: 600;
  color: #111827;
}

.flow-meta,
.flow-time {
  font-size: 13px;
  color: #6b7280;
}

.flow-context {
  display: flex; gap: 8px; margin-top: 8px; padding: 8px 12px;
  background: #f0f9ff; border-radius: 6px; font-size: 13px;
}
.context-label { color: #909399; flex-shrink: 0; font-weight: 600; }
.context-text { color: #303133; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.step-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.step-extra {
  margin: 0;
  padding: 10px 12px;
  background: #0f172a;
  color: #dbeafe;
  border-radius: 8px;
  font-size: 12px;
  overflow: auto;
}
</style>
