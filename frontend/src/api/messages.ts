import request from './request'

export const messagesApi = {
  list(conversationId: number, params?: any) {
    return request.get(`/conversations/${conversationId}/messages`, { params })
  },
  send(conversationId: number, content: string) {
    return request.post(`/conversations/${conversationId}/messages`, { content })
  },
  getById(id: number) {
    return request.get(`/messages/${id}`)
  },
  getDetail(id: number) {
    return request.get(`/messages/${id}/detail`)
  },
  search(keyword: string, params?: any) {
    return request.get('/messages/search', { params: { keyword, ...params } })
  },
  delete(id: number) {
    return request.delete(`/messages/${id}`)
  },
  getContents(id: number) {
    return request.get(`/messages/${id}/contents`)
  },
  getReasoning(id: number) {
    return request.get(`/messages/${id}/reasoning`)
  },
  getToolCalls(id: number) {
    return request.get(`/messages/${id}/tool-calls`)
  },
  getMetadata(id: number) {
    return request.get(`/messages/${id}/metadata`)
  },
}
