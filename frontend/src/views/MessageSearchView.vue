<template>
  <div class="page">
    <h3>消息搜索</h3>
    <el-input v-model="keyword" placeholder="输入关键词搜索消息..." @keyup.enter="search" style="width: 400px; margin-bottom: 16px;">
      <template #append>
        <el-button @click="search">搜索</el-button>
      </template>
    </el-input>
    <el-table :data="results" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="内容预览">
        <template #default="{ row }">
          <span v-if="row.contents?.[0]">{{ row.contents[0].content.substring(0, 80) }}...</span>
        </template>
      </el-table-column>
      <el-table-column prop="sender_type" label="发送者" width="80" />
      <el-table-column prop="created_at" label="时间" width="170" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { messagesApi } from '@/api/messages'

const keyword = ref('')
const results = ref<any[]>([])

async function search() {
  if (!keyword.value.trim()) return
  const res = await messagesApi.search(keyword.value)
  results.value = res.data.items
}
</script>
