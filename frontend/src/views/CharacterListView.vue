<template>
  <div class="page">
    <h3>AI 角色</h3>
    <el-row :gutter="20">
      <el-col :span="6" v-for="char in characters" :key="char.id">
        <el-card shadow="hover" class="character-card">
          <div class="char-avatar">
            <el-avatar :size="64" :src="char.avatar" />
          </div>
          <h4>{{ char.name }}</h4>
          <p class="char-desc">{{ char.description || '暂无简介' }}</p>
          <el-tag v-if="char.category" size="small">{{ char.category }}</el-tag>

          <div class="conv-mini-list">
            <div v-if="!convMap[char.id]" style="font-size:12px;color:#c0c4cc;padding:8px 0">加载中...</div>
            <div v-else-if="!convMap[char.id].length" style="padding:8px 0">
              <el-button text type="primary" size="small" @click="createChat(char)">+ 新建会话</el-button>
            </div>
            <div v-for="conv in convMap[char.id]?.slice(0, 3)" :key="conv.id"
              class="conv-link" @click="enterChat(conv.id)">
              <span>{{ conv.title }}</span>
              <span class="conv-msg-count">{{ conv.message_count }} 条</span>
            </div>
            <div v-if="convMap[char.id]?.length > 3" style="padding:4px 0">
              <el-button text size="small" type="primary" @click="enterCharChat(char)">查看全部 →</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { charactersApi } from '@/api/characters'
import { conversationsApi } from '@/api/conversations'
import type { CharacterBrief, Conversation } from '@/types'

const router = useRouter()
const characters = ref<CharacterBrief[]>([])
const convMap = reactive<Record<number, Conversation[]>>({})

onMounted(async () => {
  const res = await charactersApi.list()
  characters.value = res.data
  // 加载每个角色的会话
  for (const char of characters.value) {
    const cr = await conversationsApi.list({ character_id: char.id })
    convMap[char.id] = cr.data
  }
})

async function createChat(char: CharacterBrief) {
  const res = await conversationsApi.create({ character_id: char.id, title: `与 ${char.name} 的对话` })
  router.push(`/chat/${res.data.id}`)
}

function enterChat(convId: number) {
  router.push(`/chat/${convId}`)
}

function enterCharChat(char: CharacterBrief) {
  // 如果有 active 会话则跳转第一个，否则创建新会话
  const active = convMap[char.id]?.find(c => c.status === 'active')
  if (active) {
    router.push(`/chat/${active.id}`)
  } else {
    createChat(char)
  }
}
</script>

<style scoped>
.character-card { text-align: center; transition: transform .2s; }
.character-card:hover { transform: translateY(-2px); }
.char-avatar { margin-bottom: 8px; }
.char-desc { color: #909399; font-size: 13px; min-height: 36px; margin-bottom: 8px; }
.conv-mini-list { margin-top: 12px; padding-top: 12px; border-top: 1px solid #ebeef5; text-align: left; }
.conv-link { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; cursor: pointer; font-size: 13px; color: #606266; border-bottom: 1px solid #f5f5f5; }
.conv-link:hover { color: #409eff; }
.conv-msg-count { font-size: 11px; color: #c0c4cc; }
</style>
