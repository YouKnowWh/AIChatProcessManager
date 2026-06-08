import request from './request'

export const adminApi = {
  getUsers(params?: any) {
    return request.get('/admin/users', { params })
  },
  getUser(id: number) {
    return request.get(`/admin/users/${id}`)
  },
  updateUser(id: number, data: any) {
    return request.put(`/admin/users/${id}`, data)
  },
  resetPassword(id: number, newPassword: string) {
    return request.put(`/admin/users/${id}/password`, { new_password: newPassword })
  },
  disableUser(id: number) {
    return request.put(`/admin/users/${id}/disable`)
  },
  enableUser(id: number) {
    return request.put(`/admin/users/${id}/enable`)
  },
  deleteUser(id: number) {
    return request.delete(`/admin/users/${id}`)
  },
  getMessages(params?: any) {
    return request.get('/admin/messages', { params })
  },
  hideMessage(id: number) {
    return request.put(`/admin/messages/${id}/hide`)
  },
  restoreMessage(id: number) {
    return request.put(`/admin/messages/${id}/restore`)
  },
  getFeedbacks(params?: any) {
    return request.get('/admin/feedbacks', { params })
  },
  getLogs(params?: any) {
    return request.get('/admin/logs', { params })
  },
  getStats() {
    return request.get('/admin/stats')
  },
  createAuditRecord(params: any) {
    return request.post('/admin/audit-records', null, { params })
  },
  getAuditRecords(params?: any) {
    return request.get('/admin/audit-records', { params })
  },
}
