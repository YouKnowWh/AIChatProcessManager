<template>
  <div class="page">
    <h3>会话管理</h3>
    <el-table :data="conversations" stripe @row-click="(row: any) => $router.push(`/chat/${row.id}`)" style="cursor: pointer">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="character_name" label="AI 角色" width="120" />
      <el-table-column prop="message_count" label="消息数" width="80" />
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status === 'active' ? '进行中' : '已归档' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_message_at" label="最后消息" width="170">
        <template #default="{ row }">{{ row.last_message_at || '-' }}</template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="100">
        <template #default="{ row }">
          <el-button v-if="row.status === 'archived'" text size="small" type="success" @click.stop="handleUnarchive(row)">恢复</el-button>
          <el-button v-if="row.status === 'active'" text size="small" type="warning" @click.stop="handleArchive(row)">归档</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { conversationsApi } from '@/api/conversations'
import type { Conversation } from '@/types'

const conversations = ref<Conversation[]>([])

onMounted(loadData)

async function loadData() {
  try {
    const res = await conversationsApi.list()
    conversations.value = res.data
  } catch {
    // 错误已由拦截器提示，此处仅忽略
  }
}

async function handleUnarchive(row: Conversation) {
  await conversationsApi.unarchive(row.id)
  ElMessage.success('已恢复为进行中')
  loadData()
}

async function handleArchive(row: Conversation) {
  await conversationsApi.archive(row.id)
  ElMessage.success('已归档')
  loadData()
}
</script>
