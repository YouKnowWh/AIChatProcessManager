// 认证相关类型
export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  nickname?: string
}

export interface TokenResponse {
  code: number
  message: string
  data: {
    access_token: string
    token_type: string
    expires_in: number
    user: UserBrief
  }
}

export interface UserBrief {
  id: number
  username: string
  email: string
  nickname: string | null
  role: 'user' | 'character_manager' | 'admin'
  avatar: string | null
}

// 用户相关
export interface UserInfo extends UserBrief {
  phone: string | null
  bio: string | null
  status: 'active' | 'disabled'
  last_login_at: string | null
  created_at: string
}

// AI 角色
export interface AICharacter {
  id: number
  creator_id: number
  name: string
  avatar: string | null
  description: string | null
  system_prompt: string | null
  category: string | null
  tags: string | null
  status: 'active' | 'disabled'
  usage_count: number
  created_at: string
  updated_at: string
}

export interface CharacterBrief {
  id: number
  creator_id: number
  name: string
  avatar: string | null
  description: string | null
  category: string | null
  tags: string | null
  status: string
  usage_count: number
}

// 会话
export interface Conversation {
  id: number
  user_id: number
  character_id: number
  character_name?: string
  character_avatar?: string
  title: string | null
  status: 'active' | 'archived' | 'deleted'
  last_message_at: string | null
  message_count: number
  created_at: string
  updated_at: string
}

// 消息
export interface ContentBlock {
  id: number
  content_type: 'text' | 'markdown' | 'code' | 'link' | 'image'
  content: string
  sort_order: number
}

export interface Message {
  id: number
  conversation_id: number
  parent_message_id: number | null
  sender_type: 'user' | 'ai' | 'system' | 'tool'
  role: 'user' | 'assistant' | 'system' | 'tool'
  status: 'normal' | 'hidden' | 'deleted'
  sequence_number: number
  created_at: string
  is_favorited?: boolean
  contents: ContentBlock[]
}

export interface ReasoningBlock {
  id: number
  reasoning_content: string
  visibility: string
}

export interface ToolCallBlock {
  id: number
  tool_name: string
  tool_type: string
  arguments: Record<string, any>
  call_id: string | null
  status: string
  result: ToolResultBlock | null
}

export interface ToolResultBlock {
  id: number
  result_content: Record<string, any>
  is_error: boolean
}

export interface MetadataBlock {
  id: number
  model_name: string | null
  provider: string | null
  prompt_tokens: number | null
  completion_tokens: number | null
  total_tokens: number | null
  duration_ms: number | null
  finish_reason: string | null
  temperature: number | null
  top_p: number | null
}

export interface MessageDetail {
  message: Message
  contents: ContentBlock[]
  reasoning: ReasoningBlock | null
  tool_calls: ToolCallBlock[]
  metadata: MetadataBlock | null
}

// API 响应
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PaginatedData<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// 反馈
export interface Feedback {
  id: number
  user_id: number
  message_id: number
  character_id: number
  feedback_type: 'like' | 'dislike' | 'text'
  content: string | null
  tags: string | null
  created_at: string
}

// 系统日志
export interface SystemLog {
  id: number
  user_id: number | null
  action: string
  target_type: string | null
  target_id: number | null
  detail: string | null
  ip_address: string | null
  created_at: string
}
