import request from './request'

export const favoritesApi = {
  toggle(messageId: number) {
    return request.post(`/messages/${messageId}/favorite`)
  },
  remove(messageId: number) {
    return request.delete(`/messages/${messageId}/favorite`)
  },
  list(params?: any) {
    return request.get('/favorites', { params })
  },
}
