/**
 * Pinia状态管理配置
 */
import { createPinia } from 'pinia'

const pinia = createPinia()

// 持久化插件配置（使用uni.storage）
pinia.use(({ store }) => {
  // 从本地存储恢复状态
  const storageKey = `pinia-${store.$id}`
  const savedState = uni.getStorageSync(storageKey)

  if (savedState) {
    try {
      store.$patch(JSON.parse(savedState))
    } catch (e) {
      console.error('Failed to restore state:', e)
    }
  }

  // 监听状态变化并保存到本地存储
  store.$subscribe((mutation, state) => {
    try {
      uni.setStorageSync(storageKey, JSON.stringify(state))
    } catch (e) {
      console.error('Failed to save state:', e)
    }
  })
})

export default pinia
