<template>
  <div class="page">
    <h3>角色管理</h3>
    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态" clearable @change="load" style="width: 130px">
        <el-option label="启用" value="active" />
        <el-option label="禁用" value="disabled" />
      </el-select>
    </div>
    <el-table :data="characters" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="头像" width="60">
        <template #default="{ row }"><el-avatar :size="32" :src="row.avatar" /></template>
      </el-table-column>
      <el-table-column prop="name" label="名称" width="140" />
      <el-table-column prop="category" label="分类" width="90" />
      <el-table-column prop="status" label="状态" width="70">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">{{ row.status === 'active' ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="usage_count" label="使用" width="60" />
      <el-table-column label="操作" align="center" width="160">
        <template #default="{ row }">
          <el-button text type="primary" size="small" @click="toggle(row)">{{ row.status === 'active' ? '禁用' : '启用' }}</el-button>
          <el-button text type="danger" size="small" @click="del(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { charactersApi } from '@/api/characters'
import type { AICharacter } from '@/types'

const characters = ref<AICharacter[]>([])
const loading = ref(false)
const filterStatus = ref('')

onMounted(load)
async function load() {
  loading.value = true
  try {
    const res = await charactersApi.list()
    characters.value = filterStatus.value ? res.data.filter((c: AICharacter) => c.status === filterStatus.value) : res.data
  } finally { loading.value = false }
}
async function toggle(row: AICharacter) {
  if (row.status === 'active') { await charactersApi.disable(row.id); ElMessage.success('已禁用') }
  else { await charactersApi.update(row.id, { status: 'active' }); ElMessage.success('已启用') }
  load()
}
async function del(row: AICharacter) {
  try { await ElMessageBox.confirm('确定删除？', '确认', { type: 'warning' }) } catch { return }
  await charactersApi.delete(row.id)
  ElMessage.success('已删除')
  load()
}
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
</style>
