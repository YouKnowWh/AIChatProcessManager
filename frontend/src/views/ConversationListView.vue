<template>
  <div class="page">
    <h3>会话列表</h3>
    <el-table :data="conversations" stripe @row-click="(row: any) => $router.push(`/chat/${row.id}`)" style="cursor: pointer">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="character_name" label="AI 角色" width="120" />
      <el-table-column prop="message_count" label="消息数" width="80" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status === 'active' ? '进行中' : '已归档' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_message_at" label="最后消息" width="170" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { conversationsApi } from '@/api/conversations'
import type { Conversation } from '@/types'

const conversations = ref<Conversation[]>([])

onMounted(async () => {
  const res = await conversationsApi.list()
  conversations.value = res.data
})
</script>
