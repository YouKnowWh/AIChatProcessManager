import request from './request'

export const usersApi = {
  getMe() {
    return request.get('/users/me')
  },
  updateMe(data: any) {
    return request.put('/users/me', data)
  },
}
