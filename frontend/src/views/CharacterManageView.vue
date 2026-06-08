<template>
  <div class="page">
    <div class="page-header">
      <h3>AI 角色管理</h3>
      <el-button type="primary" :icon="Plus" @click="$router.push('/characters/0/edit')">创建角色</el-button>
    </div>

    <el-table :data="characters" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="头像" width="70">
        <template #default="{ row }">
          <el-avatar :size="36" :src="row.avatar" />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="名称" width="140" />
      <el-table-column prop="category" label="分类" width="100">
        <template #default="{ row }">
          <el-tag v-if="row.category" size="small">{{ row.category }}</el-tag>
          <span v-else class="text-muted">-</span>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="简介" show-overflow-tooltip min-width="180" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">
            {{ row.status === 'active' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="usage_count" label="使用次数" width="90" />
      <el-table-column prop="created_at" label="创建时间" width="170">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" size="small" @click="$router.push(`/characters/${row.id}/edit`)">编辑</el-button>
          <el-button text type="warning" size="small" @click="$router.push(`/characters/${row.id}/stats`)">统计</el-button>
          <el-button text type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { charactersApi } from '@/api/characters'
import type { AICharacter } from '@/types'

const characters = ref<AICharacter[]>([])
const loading = ref(false)

onMounted(loadCharacters)

async function loadCharacters() {
  loading.value = true
  try {
    const res = await charactersApi.list()
    characters.value = res.data
  } finally {
    loading.value = false
  }
}

async function handleDelete(row: AICharacter) {
  try {
    await ElMessageBox.confirm(`确定删除角色「${row.name}」？`, '确认删除', { type: 'warning' })
  } catch { return }
  await charactersApi.delete(row.id)
  ElMessage.success('已删除')
  loadCharacters()
}

function formatTime(ts: string) {
  return new Date(ts).toLocaleString('zh-CN')
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h3 { margin: 0; }
.text-muted { color: #c0c4cc; }
</style>
