<template>
  <div class="chat-layout">
    <!-- 左侧会话列表 -->
    <ConversationSidebar
      :conversations="conversations"
      :active-id="activeConvId"
      @select="selectConversation"
      @refresh="loadConversations"
    />

    <!-- 中间聊天区域 -->
    <div class="chat-main" v-if="activeConvId">
      <!-- 消息流 -->
      <div class="message-list" ref="msgListRef">
        <div v-if="loading" class="chat-loading">
          <el-icon class="is-loading" :size="32"><Loading /></el-icon>
          <p>加载消息中...</p>
        </div>
        <div v-for="msg in messages" :key="msg.id" :ref="el => setMsgRef(msg.id, el)">
          <MessageBubble
            :message="msg"
            :is-favorited="favIds.has(msg.id)"
            @favorite="handleFavorite(msg)"
            @feedback="showFeedback(msg)"
            @detail="showDetail(msg)"
          />
        </div>
        <div v-if="sending" class="typing-indicator">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          <span class="typing-text">AI 正在思考...</span>
        </div>
      </div>

      <!-- 底部输入框 -->
      <MessageInput :disabled="sending" @send="handleSend" />
    </div>

    <!-- 未选择会话 -->
    <div class="chat-empty" v-else>
      <el-icon :size="64" color="#c0c4cc"><ChatDotRound /></el-icon>
      <h3>选择一个会话开始聊天</h3>
      <p>或前往 <el-button text type="primary" @click="$router.push('/characters')">AI 角色</el-button> 创建新会话</p>
    </div>

    <!-- 详情弹窗 -->
    <MessageDetailDialog
      v-model:visible="detailVisible"
      :message-id="detailMsgId"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ChatDotRound, Loading } from '@element-plus/icons-vue'
import { conversationsApi } from '@/api/conversations'
import { messagesApi } from '@/api/messages'
import { favoritesApi } from '@/api/favorites'
import { feedbacksApi } from '@/api/feedbacks'
import ConversationSidebar from '@/components/chat/ConversationSidebar.vue'
import MessageBubble from '@/components/chat/MessageBubble.vue'
import MessageInput from '@/components/chat/MessageInput.vue'
import MessageDetailDialog from '@/components/chat/MessageDetailDialog.vue'
import type { Conversation, Message } from '@/types'

const route = useRoute()

// 会话列表
const conversations = ref<Conversation[]>([])
const activeConvId = ref<number | null>(null)

// 消息
const messages = ref<Message[]>([])
const loading = ref(false)
const sending = ref(false)
const favIds = ref(new Set<number>())

// 详情弹窗
const detailVisible = ref(false)
const detailMsgId = ref<number | null>(null)

const msgListRef = ref<HTMLElement>()
const msgRefs: Record<number, HTMLElement | null> = {}

function setMsgRef(id: number, el: any) {
  if (el) msgRefs[id] = el
}

// 加载会话列表
async function loadConversations() {
  const res = await conversationsApi.list()
  conversations.value = res.data
}

// 选择会话
async function selectConversation(convId: number) {
  activeConvId.value = convId
  await loadMessages()
}

// 加载消息
async function loadMessages() {
  if (!activeConvId.value) return
  loading.value = true
  try {
    const res = await messagesApi.list(activeConvId.value)
    messages.value = res.data.items
    favIds.value = new Set(
      messages.value
        .filter((msg) => msg.is_favorited)
        .map((msg) => msg.id)
    )
    await nextTick()
    scrollToBottom()
  } finally {
    loading.value = false
  }
}

// 发送消息
async function handleSend(content: string) {
  if (!activeConvId.value || !content.trim()) return

  // 1. 乐观更新 — 用户消息立即显示
  const tempId = -Date.now()
  const optimisticMsg: Message = {
    id: tempId,
    conversation_id: activeConvId.value,
    parent_message_id: null,
    sender_type: 'user',
    role: 'user',
    status: 'normal',
    sequence_number: messages.value.length + 1,
    created_at: new Date().toISOString(),
    contents: [{ id: tempId, content_type: 'text', content, sort_order: 0 }],
  }
  messages.value.push(optimisticMsg)
  await nextTick()
  scrollToBottom()

  // 2. 发送到后端，等待 AI 回复
  sending.value = true
  try {
    const res = await messagesApi.send(activeConvId.value, content)
    // 替换临时用户消息为真实数据，追加 AI 回复
    const idx = messages.value.findIndex(m => m.id === tempId)
    if (idx >= 0) messages.value.splice(idx, 1, res.data.user_message)
    messages.value.push(res.data.ai_message)
    await nextTick()
    scrollToBottom()
    await loadConversations()
  } catch {
    ElMessage.error('发送失败')
    // 移除失败的临时消息
    messages.value = messages.value.filter(m => m.id !== tempId)
  } finally {
    sending.value = false
  }
}

// 收藏/取消收藏
async function handleFavorite(msg: Message) {
  const res = await favoritesApi.toggle(msg.id)
  if (res.data.favorited) {
    favIds.value = new Set([...favIds.value, msg.id])
    ElMessage.success('已收藏')
  } else {
    favIds.value = new Set([...favIds.value].filter((id) => id !== msg.id))
    ElMessage.success('已取消收藏')
  }
}

// 反馈
function showFeedback(msg: Message) {
  ElMessage.info('反馈功能 — 点赞/点踩')
}

// 查看详情
function showDetail(msg: Message) {
  detailMsgId.value = msg.id
  detailVisible.value = true
}

function scrollToBottom() {
  // requestAnimationFrame + nextTick 确保内容完全渲染
  nextTick(() => {
    requestAnimationFrame(() => {
      if (msgListRef.value) {
        msgListRef.value.scrollTop = msgListRef.value.scrollHeight
      }
    })
  })
}

onMounted(async () => {
  await loadConversations()
  // 如果路由带 id，自动选中
  const routeId = Number(route.params.id)
  if (routeId) {
    activeConvId.value = routeId
    await loadMessages()
  }
})

// 路由变化时切换会话
watch(() => route.params.id, async (newId) => {
  const id = Number(newId)
  if (id && id !== activeConvId.value) {
    activeConvId.value = id
    await loadMessages()
  }
})
</script>

<style scoped>
.chat-layout { display: flex; height: calc(100vh - 108px); background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.chat-main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.chat-empty { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #909399; gap: 12px; }
.message-list { flex: 1; overflow-y: auto; padding: 20px; background: #fafafa; }
.chat-loading { text-align: center; padding: 40px; color: #909399; }
.typing-indicator { display: flex; align-items: center; gap: 4px; padding: 12px 20px; }
.typing-indicator .dot { width: 8px; height: 8px; border-radius: 50%; background: #c0c4cc; animation: bounce 1.4s infinite both; }
.typing-indicator .dot:nth-child(2) { animation-delay: .16s; }
.typing-indicator .dot:nth-child(3) { animation-delay: .32s; }
.typing-text { font-size: 13px; color: #909399; margin-left: 8px; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
</style>
