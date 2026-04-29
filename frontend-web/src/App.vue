<template>
  <div id="app">
    <MobileNav />
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import MobileNav from '@/components/MobileNav.vue'

const userStore = useUserStore()

onMounted(() => {
  // 检查登录状态
  const token = localStorage.getItem('token')
  if (token) {
    userStore.checkAuth()
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 移动端时为导航栏留出空间 */
@media (max-width: 768px) {
  #app > div:not(.mobile-nav) {
    padding-top: 64px;
  }
}
</style>
