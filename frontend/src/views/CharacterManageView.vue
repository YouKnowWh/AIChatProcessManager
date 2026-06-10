<template>
  <div class="page">
    <div class="page-header">
      <h3>角色管理</h3>
      <el-button type="primary" :icon="Plus" @click="openCreate">创建角色</el-button>
    </div>

    <el-table :data="characters" stripe v-loading="loading">
      <el-table-column label="头像" width="70">
        <template #default="{ row }"><el-avatar :size="36" :src="row.avatar" /></template>
      </el-table-column>
      <el-table-column prop="name" label="名称" width="140" />
      <el-table-column prop="category" label="分类" width="100">
        <template #default="{ row }"><el-tag v-if="row.category" size="small">{{ row.category }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="creator_username" label="创建者" width="100" />
      <el-table-column prop="usage_count" label="使用" width="70" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">{{ row.status === 'active' ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="240">
        <template #default="{ row }">
          <el-button text type="primary" size="small" @click="openEdit(row)">编辑</el-button>
          <el-button text size="small" @click="openStats(row)">统计</el-button>
          <el-button text type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑弹窗 -->
    <el-dialog v-model="editVisible" :title="isCreate ? '创建角色' : '编辑角色'" width="580px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item v-if="isCreate && isManager" label="所属用户">
          <el-select v-model="form.owner_id" placeholder="选择用户" style="width:100%">
            <el-option v-for="u in availableUsers" :key="u.id" :label="`${u.nickname} (${u.username})`" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="角色名称" maxlength="100" />
        </el-form-item>
        <el-form-item label="头像 URL">
          <el-input v-model="form.avatar" placeholder="头像图片 URL" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="选择或输入" allow-create clearable filterable style="width: 100%">
            <el-option label="通用" value="通用" /><el-option label="编程" value="编程" />
            <el-option label="写作" value="写作" /><el-option label="翻译" value="翻译" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="form.tags" placeholder="逗号分隔" maxlength="255" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="简要描述" />
        </el-form-item>
        <el-form-item label="系统提示词">
          <el-input v-model="form.system_prompt" type="textarea" :rows="4" placeholder="System Prompt" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">{{ isCreate ? '创建' : '保存' }}</el-button>
      </template>
    </el-dialog>

    <!-- 统计弹窗 -->
    <el-dialog v-model="statsVisible" title="角色统计" width="500px">
      <el-row :gutter="16" v-loading="statsLoading">
        <el-col :span="8" v-for="card in statCards" :key="card.label">
          <el-card shadow="hover" style="text-align:center">
            <div style="font-size:28px;font-weight:bold;color:#409eff">{{ card.value }}</div>
            <div style="font-size:13px;color:#909399;margin-top:4px">{{ card.label }}</div>
          </el-card>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { charactersApi } from '@/api/characters'
import type { AICharacter } from '@/types'

const characters = ref<AICharacter[]>([])
const availableUsers = ref<{id:number,username:string,nickname:string}[]>([])
const loading = ref(false)
const isManager = ref(false)

// 列表
async function loadData() {
  loading.value = true
  try {
    const res = await charactersApi.listMine()
    if (res.data.characters) {
      characters.value = res.data.characters
      availableUsers.value = res.data.available_users || []
      isManager.value = res.data.available_users !== null
    } else {
      characters.value = res.data
    }
  } finally { loading.value = false }
}
loadData()

// 创建/编辑
const editVisible = ref(false)
const formRef = ref<FormInstance>()
const submitting = ref(false)
const editingId = ref<number | null>(null)
const isCreate = computed(() => editingId.value === null)

const form = reactive({ name: '', avatar: '', category: '', tags: '', description: '', system_prompt: '', owner_id: 0 })
const rules: FormRules = { name: [{ required: true, message: '请输入名称', trigger: 'blur' }] }

function resetForm() {
  form.name = ''; form.avatar = ''; form.category = ''; form.tags = ''
  form.description = ''; form.system_prompt = ''; form.owner_id = 0
  editingId.value = null
}

function openCreate() { resetForm(); editVisible.value = true }
function openEdit(row: AICharacter) {
  editingId.value = row.id
  form.name = row.name; form.avatar = row.avatar || ''
  form.category = row.category || ''; form.tags = row.tags || ''
  form.description = row.description || ''; form.system_prompt = row.system_prompt || ''
  editVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    if (isCreate.value) {
      const payload = { ...form, owner_id: form.owner_id || undefined }
      await charactersApi.create(payload)
      ElMessage.success('创建成功')
    } else {
      await charactersApi.update(editingId.value!, form)
      ElMessage.success('保存成功')
    }
    editVisible.value = false
    loadData()
  } finally { submitting.value = false }
}

async function handleDelete(row: AICharacter) {
  try { await ElMessageBox.confirm(`确定删除「${row.name}」？`, '确认', { type: 'warning' }) } catch { return }
  await charactersApi.delete(row.id)
  ElMessage.success('已删除')
  loadData()
}

// 统计
const statsVisible = ref(false)
const statsLoading = ref(false)
const stats = ref<Record<string, any>>({})
const statCards = computed(() => [
  { label: '使用次数', value: stats.value.usage_count ?? 0 },
  { label: '会话数', value: stats.value.conversation_count ?? 0 },
  { label: '消息数', value: stats.value.message_count ?? 0 },
  { label: '点赞', value: stats.value.like_count ?? 0 },
  { label: '点踩', value: stats.value.dislike_count ?? 0 },
  { label: '反馈', value: (stats.value.like_count ?? 0) + (stats.value.dislike_count ?? 0) },
])

async function openStats(row: AICharacter) {
  statsVisible.value = true
  statsLoading.value = true
  try {
    const res = await charactersApi.getStats(row.id)
    stats.value = res.data
  } finally { statsLoading.value = false }
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h3 { margin: 0; }
</style>
