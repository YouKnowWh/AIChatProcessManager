import request from './request'
import type { LoginRequest, RegisterRequest, TokenResponse } from '@/types/auth'

export const authApi = {
  register(data: RegisterRequest): Promise<TokenResponse> {
    return request.post('/auth/register', data)
  },
  login(data: LoginRequest): Promise<TokenResponse> {
    return request.post('/auth/login', data)
  },
  me() {
    return request.get('/auth/me')
  },
  logout() {
    return request.post('/auth/logout')
  },
}
