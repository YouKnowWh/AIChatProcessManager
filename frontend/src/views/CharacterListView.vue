<template>
  <div class="page">
    <h3>AI 角色</h3>

    <el-collapse v-model="expandedChars" accordion>
      <el-collapse-item
        v-for="char in characters"
        :key="char.id"
        :name="char.id"
        @change="(visible: boolean) => visible && loadConversations(char)"
      >
        <template #title>
          <div class="char-title">
            <el-avatar :size="32" :src="char.avatar" />
            <span class="char-name">{{ char.name }}</span>
            <el-tag v-if="char.category" size="small">{{ char.category }}</el-tag>
            <span class="char-desc-text">{{ char.description || '暂无简介' }}</span>
          </div>
        </template>

        <!-- 该角色的会话列表 -->
        <div v-loading="convLoading[char.id]" class="conv-sub-list">
          <div v-if="!convMap[char.id]?.length" class="no-conv" style="padding:16px;color:#909399">
            暂无会话 —
            <el-button text type="primary" size="small" @click.stop="createConv(char)">新建</el-button>
          </div>
          <div
            v-for="conv in convMap[char.id]"
            :key="conv.id"
            class="conv-row"
            @click.stop="enterChat(conv.id)"
          >
            <span class="conv-row-title">{{ conv.title }}</span>
            <span class="conv-row-meta">{{ conv.message_count }} 条消息</span>
            <span class="conv-row-time">{{ conv.last_message_at ? fmtTime(conv.last_message_at) : '—' }}</span>
            <el-tag v-if="conv.status === 'archived'" size="small" type="info">已归档</el-tag>
          </div>
          <div style="padding:8px 16px">
            <el-button text type="primary" size="small" @click.stop="createConv(char)">+ 新建会话</el-button>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { charactersApi } from '@/api/characters'
import { conversationsApi } from '@/api/conversations'
import type { CharacterBrief, Conversation } from '@/types'

const router = useRouter()
const characters = ref<CharacterBrief[]>([])
const expandedChars = ref<number[]>([])

const convMap = reactive<Record<number, Conversation[]>>({})
const convLoading = reactive<Record<number, boolean>>({})

charactersApi.list().then(res => characters.value = res.data)

async function loadConversations(char: CharacterBrief) {
  if (convMap[char.id]) return
  convLoading[char.id] = true
  try {
    const res = await conversationsApi.list({ character_id: char.id })
    convMap[char.id] = res.data
  } finally { convLoading[char.id] = false }
}

async function createConv(char: CharacterBrief) {
  const res = await conversationsApi.create({ character_id: char.id, title: `与 ${char.name} 的对话` })
  router.push(`/chat/${res.data.id}`)
}

function enterChat(convId: number) {
  router.push(`/chat/${convId}`)
}

function fmtTime(ts: string) {
  return new Date(ts).toLocaleString('zh-CN')
}
</script>

<style scoped>
.char-title { display: flex; align-items: center; gap: 12px; width: 100%; }
.char-name { font-weight: 600; font-size: 15px; }
.char-desc-text { color: #909399; font-size: 13px; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.conv-sub-list { background: #fafafa; border-top: 1px solid #ebeef5; }
.conv-row { display: flex; align-items: center; gap: 16px; padding: 10px 16px 10px 48px; cursor: pointer; border-bottom: 1px solid #f0f0f0; transition: background .15s; }
.conv-row:hover { background: #ecf5ff; }
.conv-row-title { flex: 1; font-size: 14px; color: #303133; }
.conv-row-meta { font-size: 12px; color: #909399; }
.conv-row-time { font-size: 12px; color: #c0c4cc; min-width: 140px; }
</style>
