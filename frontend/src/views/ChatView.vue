<template>
  <div class="chat-layout">
    <ConversationSidebar
      :conversations="conversations"
      :active-id="activeConvId"
      @select="setActiveConversation"
      @refresh="loadConversations"
    />
    <div class="chat-main" v-if="activeConvId">
      <div class="message-list" ref="msgListRef">
        <div v-if="loading" class="chat-loading">
          <el-icon class="is-loading" :size="32"><Loading /></el-icon>
          <p>加载消息中...</p>
        </div>
        <MessageBubble
          v-for="msg in messages" :key="msg.id"
          :message="msg" :is-favorited="favIds.has(msg.id)"
          @favorite="handleFavorite(msg)" @feedback="showFeedback(msg)" @detail="showDetail(msg)"
        />
        <div v-if="sending" class="typing-indicator">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          <span class="typing-text">AI 正在思考...</span>
        </div>
      </div>
      <MessageInput :disabled="sending" @send="handleSend" />
    </div>
    <div class="chat-empty" v-else>
      <el-icon :size="64" color="#c0c4cc"><ChatDotRound /></el-icon>
      <h3>开始新的聊天</h3>
      <el-button type="primary" @click="createConversation">新建会话</el-button>
    </div>
    <MessageDetailDialog v-model:visible="detailVisible" :message-id="detailMsgId" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ChatDotRound, Loading } from '@element-plus/icons-vue'
import { conversationsApi } from '@/api/conversations'
import { messagesApi } from '@/api/messages'
import { favoritesApi } from '@/api/favorites'
import ConversationSidebar from '@/components/chat/ConversationSidebar.vue'
import MessageBubble from '@/components/chat/MessageBubble.vue'
import MessageInput from '@/components/chat/MessageInput.vue'
import MessageDetailDialog from '@/components/chat/MessageDetailDialog.vue'
import type { Conversation, Message } from '@/types'

const route = useRoute()
const router = useRouter()
const conversations = ref<Conversation[]>([])
const activeConvId = ref<number | null>(null)
const messages = ref<Message[]>([])
const loading = ref(false)
const sending = ref(false)
const favIds = ref(new Set<number>())
const detailVisible = ref(false)
const detailMsgId = ref<number | null>(null)
const msgListRef = ref<HTMLElement>()

async function loadConversations() {
  const res = await conversationsApi.list()
  conversations.value = res.data
}
async function createConversation() {
  const res = await conversationsApi.create({ title: '新的聊天' })
  router.push(`/chat/${res.data.id}`)
}
async function setActiveConversation(convId: number) {
  activeConvId.value = convId
  await loadMessages()
}
async function loadMessages() {
  if (!activeConvId.value) return
  loading.value = true
  try {
    const res = await messagesApi.list(activeConvId.value)
    messages.value = res.data.items
    favIds.value = new Set(messages.value.filter((m: any) => m.is_favorited).map((m: Message) => m.id))
    await nextTick(); scrollToBottom()
  } finally { loading.value = false }
}
async function handleSend(content: string) {
  if (!activeConvId.value || !content.trim()) return
  const tempId = -Date.now()
  messages.value.push({
    id: tempId, conversation_id: activeConvId.value, parent_message_id: null,
    sender_type: 'user', role: 'user', status: 'normal',
    sequence_number: messages.value.length + 1,
    created_at: new Date().toISOString(),
    contents: [{ id: tempId, content_type: 'text', content, sort_order: 0 }],
  } as Message)
  await nextTick(); scrollToBottom()
  sending.value = true
  try {
    const res = await messagesApi.send(activeConvId.value, content)
    const idx = messages.value.findIndex(m => m.id === tempId)
    if (idx >= 0) messages.value.splice(idx, 1, res.data.user_message)
    messages.value.push(res.data.ai_message)
    await nextTick(); scrollToBottom()
    await loadConversations()
  } catch { ElMessage.error('发送失败'); messages.value = messages.value.filter(m => m.id !== tempId) }
  finally { sending.value = false }
}
async function handleFavorite(msg: Message) {
  const res = await favoritesApi.toggle(msg.id)
  if (res.data.favorited) { favIds.value = new Set([...favIds.value, msg.id]); ElMessage.success('已收藏') }
  else { favIds.value = new Set([...favIds.value].filter(id => id !== msg.id)); ElMessage.success('已取消收藏') }
}
function showFeedback(_msg: Message) { ElMessage.info('反馈功能') }
function showDetail(msg: Message) { detailMsgId.value = msg.id; detailVisible.value = true }
function scrollToBottom() { nextTick(() => { requestAnimationFrame(() => { if (msgListRef.value) msgListRef.value.scrollTop = msgListRef.value.scrollHeight }) }) }

onMounted(async () => {
  await loadConversations()
  const routeId = Number(route.params.id)
  if (routeId) { activeConvId.value = routeId; await loadMessages() }
})
watch(() => route.params.id, async (newId) => {
  const id = Number(newId)
  if (id && id !== activeConvId.value) { activeConvId.value = id; await loadMessages() }
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
