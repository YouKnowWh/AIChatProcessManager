<template>
  <div class="page">
    <h3>我的收藏</h3>
    <el-table :data="favorites" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="message_preview" label="消息预览" show-overflow-tooltip />
      <el-table-column prop="conversation_title" label="所属会话" width="200" />
      <el-table-column prop="created_at" label="收藏时间" width="170" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="danger" text @click="handleRemove(row)">取消收藏</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { favoritesApi } from '@/api/favorites'
import { ElMessage } from 'element-plus'

const favorites = ref<any[]>([])

onMounted(async () => {
  const res = await favoritesApi.list()
  favorites.value = res.data.items
})

async function handleRemove(row: any) {
  await favoritesApi.remove(row.message_id)
  ElMessage.success('已取消收藏')
  favorites.value = favorites.value.filter(f => f.message_id !== row.message_id)
}
</script>
