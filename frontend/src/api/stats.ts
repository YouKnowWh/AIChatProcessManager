import request from './request'

export const statsApi = {
  getMyStats() {
    return request.get('/stats/me')
  },
}
