import request from './request'

export const knowledgeApi = {
  list(characterId: number) {
    return request.get(`/characters/${characterId}/knowledge`)
  },
  create(characterId: number, data: any) {
    return request.post(`/characters/${characterId}/knowledge`, data)
  },
  update(entryId: number, data: any) {
    return request.put(`/knowledge/${entryId}`, data)
  },
  delete(entryId: number) {
    return request.delete(`/knowledge/${entryId}`)
  },
}
