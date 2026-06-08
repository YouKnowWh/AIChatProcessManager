<template>
  <div class="msg-input">
    <el-input
      v-model="text"
      type="textarea"
      :rows="3"
      :disabled="disabled"
      placeholder="输入消息... (Enter 发送，Shift+Enter 换行)"
      resize="none"
      @keydown="handleKeydown"
    />
    <el-button
      type="primary"
      :disabled="disabled || !text.trim()"
      :loading="disabled"
      @click="handleSend"
    >
      <el-icon><Promotion /></el-icon>
      发送
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Promotion } from '@element-plus/icons-vue'

const props = defineProps<{ disabled: boolean }>()
const emit = defineEmits<{ send: [content: string] }>()

const text = ref('')

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

function handleSend() {
  if (!text.value.trim() || props.disabled) return
  emit('send', text.value)
  text.value = ''
}
</script>

<style scoped>
.msg-input { display: flex; gap: 12px; padding: 16px 20px; border-top: 1px solid #e4e7ed; background: #fff; align-items: flex-end; }
.msg-input .el-button { height: 40px; }
</style>
