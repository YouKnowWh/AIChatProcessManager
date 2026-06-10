import request from './request'

export const knowledgeApi = {
  list() {
    return request.get('/knowledge')
  },
  create(data: any) {
    return request.post('/knowledge', data)
  },
  update(entryId: number, data: any) {
    return request.put(`/knowledge/${entryId}`, data)
  },
  delete(entryId: number) {
    return request.delete(`/knowledge/${entryId}`)
  },
}
