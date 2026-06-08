import request from './request'

export const conversationsApi = {
  list(params?: any) {
    return request.get('/conversations', { params })
  },
  create(data: any) {
    return request.post('/conversations', data)
  },
  getById(id: number) {
    return request.get(`/conversations/${id}`)
  },
  update(id: number, data: any) {
    return request.put(`/conversations/${id}`, data)
  },
  archive(id: number) {
    return request.put(`/conversations/${id}/archive`)
  },
  delete(id: number) {
    return request.delete(`/conversations/${id}`)
  },
}
