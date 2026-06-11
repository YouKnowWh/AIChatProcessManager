<template>
  <div class="conv-sidebar">
    <div class="sidebar-header">
      <h4>会话列表</h4>
      <el-button :icon="Plus" circle size="small" @click="$emit('refresh'); conversationsApi.create({ title: '新的聊天' }).then(r => $router.push('/chat/' + r.data.id))" title="新建会话" />
    </div>
    <div class="sidebar-list">
      <div v-for="conv in conversations" :key="conv.id" class="conv-item" :class="{ active: conv.id === activeId }" @click="$emit('select', conv.id)">
        <div class="conv-info">
          <el-avatar :size="36" :icon="ChatDotRound" />
          <div class="conv-text">
            <div class="conv-title">{{ conv.title || '未命名会话' }}</div>
            <div class="conv-meta">
              <span v-if="conv.message_count === 0 && !conv.last_message_at" class="conv-new">新会话</span>
              <span v-else class="conv-count">{{ conv.message_count }} 条消息</span>
            </div>
          </div>
        </div>
        <el-tag v-if="conv.status === 'archived'" size="small" type="info">已归档</el-tag>
      </div>
      <el-empty v-if="!conversations.length" description="暂无会话" :image-size="60" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Plus, ChatDotRound } from '@element-plus/icons-vue'
import { conversationsApi } from '@/api/conversations'
import { useRouter } from 'vue-router'
import type { Conversation } from '@/types'

const $router = useRouter()
defineProps<{ conversations: Conversation[]; activeId: number | null }>()
defineEmits<{ select: [id: number]; refresh: [] }>()
</script>

<style scoped>
.conv-sidebar { width: 280px; border-right: 1px solid #e4e7ed; display: flex; flex-direction: column; background: #fff; flex-shrink: 0; }
.sidebar-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; border-bottom: 1px solid #ebeef5; }
.sidebar-header h4 { margin: 0; font-size: 15px; }
.sidebar-list { flex: 1; overflow-y: auto; }
.conv-item { padding: 12px 16px; cursor: pointer; border-bottom: 1px solid #f2f3f5; transition: background .2s; }
.conv-item:hover { background: #f5f7fa; }
.conv-item.active { background: #ecf5ff; border-left: 3px solid #409eff; }
.conv-info { display: flex; align-items: center; gap: 10px; }
.conv-text { flex: 1; min-width: 0; }
.conv-title { font-size: 14px; color: #303133; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.conv-meta { display: flex; gap: 12px; margin-top: 4px; font-size: 12px; color: #909399; }
.conv-new { color: #409eff; font-weight: 500; }
</style>
