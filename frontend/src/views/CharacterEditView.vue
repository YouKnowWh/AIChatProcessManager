<template>
  <div class="page">
    <div class="page-header">
      <h3>{{ isCreate ? '创建 AI 角色' : '编辑 AI 角色' }}</h3>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <el-card style="max-width: 700px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" v-loading="loading">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="输入角色名称" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="头像 URL" prop="avatar">
          <el-input v-model="form.avatar" placeholder="输入头像图片 URL（可选）" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="选择或输入分类" allow-create clearable filterable style="width: 100%">
            <el-option label="通用" value="通用" />
            <el-option label="编程" value="编程" />
            <el-option label="写作" value="写作" />
            <el-option label="翻译" value="翻译" />
            <el-option label="数据分析" value="数据分析" />
            <el-option label="创意" value="创意" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签" prop="tags">
          <el-input v-model="form.tags" placeholder="逗号分隔，如：聊天,问答,日常" maxlength="255" />
        </el-form-item>
        <el-form-item label="简介" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="角色简介" />
        </el-form-item>
        <el-form-item label="系统提示词" prop="system_prompt">
          <el-input v-model="form.system_prompt" type="textarea" :rows="5" placeholder="角色的基础提示词（System Prompt）" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            {{ isCreate ? '创建' : '保存' }}
          </el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { charactersApi } from '@/api/characters'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const submitting = ref(false)

const characterId = computed(() => {
  const id = Number(route.params.id)
  return id > 0 ? id : null
})
const isCreate = computed(() => !characterId.value)

const form = reactive({
  name: '',
  avatar: '',
  category: '',
  tags: '',
  description: '',
  system_prompt: '',
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
}

onMounted(async () => {
  if (characterId.value) {
    loading.value = true
    try {
      const res = await charactersApi.getById(characterId.value)
      const d = res.data
      Object.assign(form, {
        name: d.name || '',
        avatar: d.avatar || '',
        category: d.category || '',
        tags: d.tags || '',
        description: d.description || '',
        system_prompt: d.system_prompt || '',
      })
    } finally {
      loading.value = false
    }
  }
})

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    if (isCreate.value) {
      await charactersApi.create(form)
      ElMessage.success('创建成功')
    } else {
      await charactersApi.update(characterId.value!, form)
      ElMessage.success('保存成功')
    }
    router.push('/characters/manage')
  } catch {
    // 错误由拦截器处理
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h3 { margin: 0; }
</style>
