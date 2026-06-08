<template>
  <el-dialog
    v-model="visible"
    title="消息详情"
    width="750px"
    top="5vh"
    destroy-on-close
    @open="loadDetail"
  >
    <div v-if="detail" class="detail-body">
      <!-- 消息基本信息 -->
      <div class="detail-section">
        <h4 class="section-title">
          <el-icon><InfoFilled /></el-icon> 基本信息
        </h4>
        <el-descriptions :column="3" border size="small">
          <el-descriptions-item label="消息 ID">{{ detail.message.id }}</el-descriptions-item>
          <el-descriptions-item label="发送者">{{ senderLabel }}</el-descriptions-item>
          <el-descriptions-item label="角色">{{ detail.message.role }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ statusLabel }}</el-descriptions-item>
          <el-descriptions-item label="序号">{{ detail.message.sequence_number }}</el-descriptions-item>
          <el-descriptions-item label="时间">{{ formatTime(detail.message.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 正式回复内容 -->
      <div class="detail-section">
        <h4 class="section-title">
          <el-icon><ChatLineSquare /></el-icon> 正式回复 (Content)
        </h4>
        <div v-for="block in detail.contents" :key="block.id" class="content-display">
          <el-tag size="small" class="content-tag">{{ block.content_type }}</el-tag>
          <div v-if="block.content_type === 'code'" class="detail-code">
            <pre><code>{{ block.content }}</code></pre>
          </div>
          <div v-else class="detail-text" v-html="renderMd(block.content)" />
        </div>
        <el-empty v-if="!detail.contents.length" description="无内容" :image-size="40" />
      </div>

      <!-- 推理过程 -->
      <div class="detail-section">
        <h4 class="section-title">
          <el-icon><View /></el-icon> 推理过程 (Reasoning)
          <el-tag v-if="detail.reasoning" size="small" :type="visibilityType">{{ detail.reasoning.visibility }}</el-tag>
        </h4>
        <div v-if="detail.reasoning" class="reasoning-box">
          {{ detail.reasoning.reasoning_content }}
        </div>
        <el-empty v-else description="该消息无推理过程" :image-size="40" />
      </div>

      <!-- 工具调用 -->
      <div class="detail-section">
        <h4 class="section-title">
          <el-icon><Connection /></el-icon> 工具调用 (Tool Calls)
        </h4>
        <div v-if="detail.tool_calls.length">
          <el-collapse>
            <el-collapse-item
              v-for="tc in detail.tool_calls"
              :key="tc.id"
              :title="`${tc.tool_name} (${tc.tool_type})`"
            >
              <!-- 调用参数 -->
              <div class="tool-subsection">
                <strong>调用 ID：</strong> {{ tc.call_id || 'N/A' }}
                &nbsp;
                <el-tag :type="tc.status === 'success' ? 'success' : 'danger'" size="small">{{ tc.status }}</el-tag>
              </div>
              <div class="tool-subsection">
                <strong>参数 (arguments)：</strong>
                <pre class="json-block">{{ JSON.stringify(tc.arguments, null, 2) }}</pre>
              </div>
              <!-- 调用结果 -->
              <div class="tool-subsection" v-if="tc.result">
                <strong>结果 (result)：
                  <el-tag v-if="tc.result.is_error" type="danger" size="small">ERROR</el-tag>
                </strong>
                <pre class="json-block">{{ JSON.stringify(tc.result.result_content, null, 2) }}</pre>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
        <el-empty v-else description="该消息无工具调用" :image-size="40" />
      </div>

      <!-- 模型元数据 -->
      <div class="detail-section">
        <h4 class="section-title">
          <el-icon><DataAnalysis /></el-icon> 模型元数据 (Metadata)
        </h4>
        <div v-if="detail.metadata">
          <el-descriptions :column="3" border size="small">
            <el-descriptions-item label="模型">{{ detail.metadata.model_name || 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="提供商">{{ detail.metadata.provider || 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="结束原因">{{ detail.metadata.finish_reason || 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="Prompt Tokens">{{ detail.metadata.prompt_tokens ?? 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="Completion Tokens">{{ detail.metadata.completion_tokens ?? 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="Total Tokens">{{ detail.metadata.total_tokens ?? 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="耗时(ms)">{{ detail.metadata.duration_ms ?? 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="Temperature">{{ detail.metadata.temperature ?? 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="Top P">{{ detail.metadata.top_p ?? 'N/A' }}</el-descriptions-item>
          </el-descriptions>
        </div>
        <el-empty v-else description="该消息无元数据" :image-size="40" />
      </div>
    </div>

    <div v-else-if="loading" class="detail-loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <p>加载详情中...</p>
    </div>

    <template #footer>
      <el-button @click="visible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { messagesApi } from '@/api/messages'
import { InfoFilled, ChatLineSquare, View, Connection, DataAnalysis, Loading } from '@element-plus/icons-vue'
import type { MessageDetail } from '@/types'

const props = defineProps<{
  visible: boolean
  messageId: number | null
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const visible = computed({
  get: () => props.visible,
  set: (v) => emit('update:visible', v),
})

const detail = ref<MessageDetail | null>(null)
const loading = ref(false)

const senderLabel = computed(() => {
  const map: Record<string, string> = { user: '用户', ai: 'AI', system: '系统', tool: '工具' }
  return map[detail.value?.message.sender_type || ''] || detail.value?.message.sender_type
})

const statusLabel = computed(() => {
  const map: Record<string, string> = { normal: '正常', hidden: '已隐藏', deleted: '已删除' }
  return map[detail.value?.message.status || ''] || detail.value?.message.status
})

const visibilityType = computed(() => {
  const map: Record<string, string> = { owner_visible: 'success', admin_visible: 'warning', hidden: 'info', debug_only: 'danger' }
  return map[detail.value?.reasoning?.visibility || ''] || 'info'
})

async function loadDetail() {
  if (!props.messageId) return
  loading.value = true
  try {
    const res = await messagesApi.getDetail(props.messageId)
    detail.value = res.data
  } catch {
    detail.value = null
  } finally {
    loading.value = false
  }
}

function formatTime(ts: string): string {
  return new Date(ts).toLocaleString('zh-CN')
}

function renderMd(text: string): string {
  return text
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
}
</script>

<style scoped>
.detail-body { max-height: 70vh; overflow-y: auto; }
.detail-loading { text-align: center; padding: 40px; color: #909399; }
.detail-section { margin-bottom: 24px; }
.section-title { display: flex; align-items: center; gap: 8px; margin: 0 0 12px; font-size: 15px; color: #303133; }
.content-display { margin-bottom: 12px; }
.content-tag { margin-bottom: 6px; }
.detail-code { background: #1e1e1e; border-radius: 8px; padding: 12px; overflow-x: auto; }
.detail-code code { color: #d4d4d4; font-size: 13px; }
.detail-text { font-size: 14px; line-height: 1.7; }
.reasoning-box { background: #fdf6ec; border: 1px solid #faecd8; border-radius: 8px; padding: 16px; font-size: 13px; line-height: 1.8; color: #606266; white-space: pre-wrap; }
.tool-subsection { margin: 8px 0; font-size: 13px; }
.json-block { background: #f5f7fa; border-radius: 6px; padding: 10px; margin: 6px 0; font-size: 12px; overflow-x: auto; max-height: 200px; overflow-y: auto; }
</style>
