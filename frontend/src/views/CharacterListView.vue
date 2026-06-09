<template>
  <div class="page">
    <h3>AI 角色选择</h3>
    <el-row :gutter="20">
      <el-col :span="6" v-for="c in characters" :key="c.id">
        <el-card shadow="hover" class="character-card" @click="startChat(c)">
          <div class="char-avatar">
            <el-avatar :size="64" :src="c.avatar" />
          </div>
          <h4>{{ c.name }}</h4>
          <p class="char-desc">{{ c.description || '暂无简介' }}</p>
          <el-tag v-if="c.category">{{ c.category }}</el-tag>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { charactersApi } from '@/api/characters'
import { conversationsApi } from '@/api/conversations'
import type { CharacterBrief } from '@/types'

const router = useRouter()
const characters = ref<CharacterBrief[]>([])

onMounted(async () => {
  const res = await charactersApi.list()
  characters.value = res.data
})

async function startChat(char: CharacterBrief) {
  // 查该角色已有 active 会话（自动被后端过滤为用户自己的角色）
  const listRes = await conversationsApi.list({ character_id: char.id })
  const existing = listRes.data?.find((c: any) => c.status === 'active')
  if (existing) {
    router.push(`/chat/${existing.id}`)
    return
  }
  const res = await conversationsApi.create({ character_id: char.id, title: `与 ${char.name} 的对话` })
  router.push(`/chat/${res.data.id}`)
}
</script>

<style scoped>
.character-card { cursor: pointer; text-align: center; transition: transform .2s; }
.character-card:hover { transform: translateY(-4px); }
.char-avatar { margin-bottom: 12px; }
.char-desc { color: #909399; font-size: 13px; min-height: 40px; }
</style>
