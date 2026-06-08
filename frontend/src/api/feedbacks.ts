import request from './request'

export const feedbacksApi = {
  create(messageId: number, data: any) {
    return request.post(`/messages/${messageId}/feedback`, data)
  },
  list(params?: any) {
    return request.get('/feedbacks', { params })
  },
}
