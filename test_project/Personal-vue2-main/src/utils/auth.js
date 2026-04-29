import Cookies from 'js-cookie'

const TokenKey = 'Token'
const RefreshTokenKey = 'Refresh-Token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function getRefreshToken() {
  return Cookies.get(RefreshTokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function setRefreshToken(refreshToken) {
  return Cookies.set(RefreshTokenKey, refreshToken)
}

export function removeToken() {
  Cookies.remove(TokenKey)
  Cookies.remove(RefreshTokenKey)
  return true
}