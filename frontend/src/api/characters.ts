import request from './request'

export const charactersApi = {
  list(params?: any) {
    return request.get('/characters', { params })
  },
  getById(id: number) {
    return request.get(`/characters/${id}`)
  },
  create(data: any) {
    return request.post('/characters', data)
  },
  update(id: number, data: any) {
    return request.put(`/characters/${id}`, data)
  },
  delete(id: number) {
    return request.delete(`/characters/${id}`)
  },
  disable(id: number) {
    return request.put(`/characters/${id}/disable`)
  },
  getStats(id: number) {
    return request.get(`/characters/${id}/stats`)
  },
  getFeedbacks(id: number, params?: any) {
    return request.get(`/characters/${id}/feedbacks`, { params })
  },
}
