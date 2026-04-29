import axios from 'axios'
export function request(config) {
  return new Promise((resolve, reject) => {
    const instance = axios.create({
      baseURL: process.env.VUE_APP_BASE_API
    })
    instance(config)
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
      })
  })
}
