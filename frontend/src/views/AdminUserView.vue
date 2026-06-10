<template>
  <div class="page">
    <h3>用户管理</h3>
    <div class="filter-bar">
      <el-select v-model="filterRole" placeholder="角色筛选" clearable @change="loadUsers" style="width: 150px">
        <el-option label="普通用户" value="user" />
        <el-option label="管理员" value="admin" />
      </el-select>
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable @change="loadUsers" style="width: 150px">
        <el-option label="启用" value="active" />
        <el-option label="禁用" value="disabled" />
      </el-select>
    </div>

    <el-table :data="users" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column prop="nickname" label="昵称" width="120" />
      <el-table-column prop="role" label="角色" width="110">
        <template #default="{ row }">
          <el-tag :type="row.role === 'admin' ? 'danger' : 'info'" size="small">{{ roleLabel(row.role) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">{{ row.status === 'active' ? '正常' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="知识库条目" width="100" align="center">
        <template #default="{ row }">{{ knowledgeMap[row.id] ?? '-' }}</template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="160">
        <template #default="{ row }">{{ fmt(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="280" fixed="right">
        <template #default="{ row }">
          <el-button text size="small" @click="editUser(row)">编辑</el-button>
          <el-button text size="small" @click="resetPwd(row)">重置密码</el-button>
          <el-button v-if="row.status === 'active'" text type="warning" size="small" @click="toggleStatus(row, 'disable')">禁用</el-button>
          <el-button v-else text type="success" size="small" @click="toggleStatus(row, 'enable')">启用</el-button>
          <el-button text type="danger" size="small" @click="delUser(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="page" :page-size="pageSize" :total="total" layout="prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="loadUsers" />

    <!-- 编辑弹窗 -->
    <el-dialog v-model="editVisible" title="编辑用户" width="450px">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="昵称"><el-input v-model="editForm.nickname" /></el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editForm.role" style="width: 100%">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="简介"><el-input v-model="editForm.bio" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '@/api/admin'
import request from '@/api/request'

const users = ref<any[]>([])
const knowledgeMap = ref<Record<number, number>>({})
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterRole = ref('')
const filterStatus = ref('')

const editVisible = ref(false)
const editForm = ref({ id: 0, nickname: '', role: '', bio: '' })

onMounted(loadUsers)

async function loadUsers() {
  loading.value = true
  try {
    const params: any = { page: page.value, page_size: pageSize.value }
    if (filterRole.value) params.role = filterRole.value
    if (filterStatus.value) params.status = filterStatus.value
    const res = await adminApi.getUsers(params)
    users.value = res.data.items
    total.value = res.data.total
  } finally { loading.value = false }
  // 加载知识库统计
  try {
    const kr = await request.get('/admin/knowledge-stats')
    const map: Record<number, number> = {}
    for (const r of kr.data) { map[r.user_id] = r.active_entries }
    knowledgeMap.value = map
  } catch { /* ignore */ }
}

function editUser(row: any) {
  editForm.value = { id: row.id, nickname: row.nickname || '', role: row.role, bio: row.bio || '' }
  editVisible.value = true
}

async function saveEdit() {
  await adminApi.updateUser(editForm.value.id, editForm.value)
  ElMessage.success('保存成功')
  editVisible.value = false
  loadUsers()
}

async function resetPwd(row: any) {
  try {
    const { value } = await ElMessageBox.prompt('输入新密码', '重置密码', { inputType: 'password', inputValidator: (v: string) => v.length >= 6 ? true : '至少 6 位' })
    await adminApi.resetPassword(row.id, value)
    ElMessage.success('密码已重置')
  } catch { /* cancel */ }
}

async function toggleStatus(row: any, action: string) {
  if (action === 'disable') await adminApi.disableUser(row.id)
  else await adminApi.enableUser(row.id)
  ElMessage.success(action === 'disable' ? '已禁用' : '已启用')
  loadUsers()
}

async function delUser(row: any) {
  try { await ElMessageBox.confirm(`确定删除用户「${row.username}」？`, '确认', { type: 'warning' }) } catch { return }
  await adminApi.deleteUser(row.id)
  ElMessage.success('已删除')
  loadUsers()
}

function roleLabel(r: string) { const m: Record<string, string> = { admin: '管理员', user: '普通用户' }; return m[r] || r }
function fmt(ts: string) { return new Date(ts).toLocaleString('zh-CN') }
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
</style>
