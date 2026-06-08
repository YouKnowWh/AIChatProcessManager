<template>
  <div class="msg-bubble" :class="[message.sender_type, { hidden: message.status !== 'normal' }]">
    <div class="bubble-avatar">
      <el-avatar :size="36" v-if="message.sender_type === 'ai'">
        <el-icon :size="20"><Service /></el-icon>
      </el-avatar>
      <el-avatar :size="36" v-else :icon="UserFilled" />
    </div>
    <div class="bubble-body">
      <div class="bubble-header">
        <span class="bubble-sender">{{ message.sender_type === 'ai' ? 'AI 助手' : '我' }}</span>
        <span class="bubble-time">{{ formatTime(message.created_at) }}</span>
      </div>
      <div class="bubble-content">
        <!-- 多内容块按 sort_order 渲染 -->
        <div v-for="block in sortedContents" :key="block.id" class="content-block">
          <!-- 代码块 -->
          <div v-if="block.content_type === 'code'" class="code-block">
            <div class="code-header">
              <span class="code-lang">代码</span>
              <el-button text size="small" @click="copyCode(block.content)">复制</el-button>
            </div>
            <pre><code>{{ block.content }}</code></pre>
          </div>
          <!-- Markdown / 文本 -->
          <div v-else class="text-block" v-html="renderText(block.content)" />
        </div>
      </div>
      <!-- AI 消息操作栏 -->
      <div v-if="message.sender_type === 'ai' && message.status === 'normal'" class="bubble-actions">
        <el-button text size="small" :type="isFavorited ? 'warning' : 'default'" @click="$emit('favorite')">
          <el-icon><StarFilled v-if="isFavorited" /><Star v-else /></el-icon>
          {{ isFavorited ? '已收藏' : '收藏' }}
        </el-button>
        <el-button text size="small" @click="$emit('feedback')">
          <el-icon><ThumbUp /></el-icon>反馈
        </el-button>
        <el-button text size="small" type="primary" @click="$emit('detail')">
          <el-icon><InfoFilled /></el-icon>详情
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Service, UserFilled, StarFilled, Star, ThumbUp, InfoFilled } from '@element-plus/icons-vue'
import type { Message, ContentBlock } from '@/types'

const props = defineProps<{
  message: Message
  isFavorited?: boolean
}>()

defineEmits<{
  favorite: []
  feedback: []
  detail: []
}>()

const sortedContents = computed(() =>
  [...props.message.contents].sort((a, b) => a.sort_order - b.sort_order)
)

function formatTime(ts: string): string {
  const d = new Date(ts)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${pad(d.getHours())}:${pad(d.getMinutes())}`
}

function renderText(text: string): string {
  // 简单的 Markdown 渲染：代码块、加粗、换行
  return text
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
}

function copyCode(code: string) {
  navigator.clipboard.writeText(code).then(() => ElMessage.success('已复制'))
}
</script>

<style scoped>
.msg-bubble { display: flex; gap: 12px; padding: 16px 0; }
.msg-bubble.user { flex-direction: row-reverse; }
.msg-bubble.hidden { opacity: .4; }
.bubble-body { max-width: 70%; }
.bubble-header { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
.bubble-sender { font-size: 13px; font-weight: 600; color: #303133; }
.bubble-time { font-size: 12px; color: #c0c4cc; }
.user .bubble-header { justify-content: flex-end; }
.bubble-content { background: #fff; border-radius: 12px; padding: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,.06); }
.user .bubble-content { background: #409eff; color: #fff; }
.text-block { font-size: 14px; line-height: 1.7; word-break: break-word; }
.code-block { background: #1e1e1e; border-radius: 8px; overflow: hidden; margin: 8px 0; }
.code-header { display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; background: #2d2d2d; }
.code-lang { color: #ccc; font-size: 12px; }
.code-block pre { margin: 0; padding: 12px; overflow-x: auto; }
.code-block code { color: #d4d4d4; font-size: 13px; font-family: 'Fira Code', 'Cascadia Code', monospace; }
.bubble-actions { display: flex; gap: 4px; margin-top: 6px; opacity: .7; }
.bubble-actions:hover { opacity: 1; }
</style>
