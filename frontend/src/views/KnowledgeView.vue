<template>
  <div class="page">
    <h3>知识库</h3>
    <div v-loading="loading">
      <div v-if="!items.length" style="color:#909399;padding:20px;text-align:center">暂无知识条目</div>
      <el-table :data="items" stripe size="small" v-else>
        <el-table-column prop="title" label="标题" width="200" />
        <el-table-column prop="content_type" label="类型" width="80">
          <template #default="{ row }"><el-tag size="small">{{ row.content_type }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="content" label="内容" show-overflow-tooltip />
        <el-table-column label="操作" width="70">
          <template #default="{ row }">
            <el-button text type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top:12px;display:flex;gap:8px">
        <el-input v-model="title" placeholder="标题" size="small" style="width:180px" />
        <el-select v-model="contentType" size="small" style="width:90px">
          <el-option label="text" value="text" /><el-option label="markdown" value="markdown" />
        </el-select>
        <el-input v-model="content" placeholder="内容" size="small" style="flex:1" />
        <el-button type="primary" size="small" :disabled="!title||!content" @click="add">添加</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { knowledgeApi } from '@/api/knowledge'

const items = ref<any[]>([])
const loading = ref(false)
const title = ref('')
const contentType = ref('text')
const content = ref('')

onMounted(load)
async function load() { loading.value = true; try { const r = await knowledgeApi.list(); items.value = r.data } finally { loading.value = false } }
async function add() { await knowledgeApi.create({ title: title.value, content: content.value, content_type: contentType.value }); ElMessage.success('已添加'); title.value=''; content.value=''; load() }
async function handleDelete(id: number) { await knowledgeApi.delete(id); ElMessage.success('已删除'); load() }
</script>
