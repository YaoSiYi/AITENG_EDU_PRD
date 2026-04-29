<template>
  <div class="mobile-nav" v-if="isMobile">
    <div class="mobile-nav-header">
      <h2 class="brand">艾腾教育</h2>
      <el-button text @click="toggleMenu" class="menu-btn">
        <el-icon :size="24">
          <component :is="showMenu ? 'Close' : 'Menu'" />
        </el-icon>
      </el-button>
    </div>

    <transition name="slide">
      <div v-if="showMenu" class="mobile-menu">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="mobile-menu-item"
          @click="closeMenu"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </router-link>

        <div class="mobile-menu-footer">
          <router-link v-if="!userStore.isAuthenticated" to="/login" class="mobile-menu-btn" @click="closeMenu">
            登录
          </router-link>
          <router-link v-else to="/profile" class="mobile-menu-btn" @click="closeMenu">
            个人中心
          </router-link>
        </div>
      </div>
    </transition>

    <div v-if="showMenu" class="mobile-overlay" @click="closeMenu"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const showMenu = ref(false)
const isMobile = ref(false)

const menuItems = [
  { path: '/', label: '首页', icon: 'HomeFilled' },
  { path: '/questions', label: '题库', icon: 'Document' },
  { path: '/activities', label: '活动', icon: 'Calendar' },
  { path: '/stats', label: '统计', icon: 'TrendCharts' },
  { path: '/wrong-book', label: '错题本', icon: 'Warning' },
  { path: '/testcases', label: '测试用例', icon: 'Finished' },
  { path: '/dashboard', label: '数据看板', icon: 'DataLine' }
]

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    showMenu.value = false
  }
}

const toggleMenu = () => {
  showMenu.value = !showMenu.value
  if (showMenu.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMenu = () => {
  showMenu.value = false
  document.body.style.overflow = ''
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.mobile-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(10, 14, 39, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
}

.brand {
  font-size: 20px;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.menu-btn {
  color: #fff;
  padding: 8px;
}

.mobile-menu {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 14, 39, 0.98);
  backdrop-filter: blur(20px);
  padding: 20px;
  overflow-y: auto;
  z-index: 999;
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s;
}

.mobile-menu-item:active {
  background: rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.3);
  color: #667eea;
}

.mobile-menu-item .el-icon {
  font-size: 20px;
}

.mobile-menu-footer {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-menu-btn {
  display: block;
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: #fff;
  text-align: center;
  text-decoration: none;
  font-size: 16px;
  font-weight: 700;
  transition: all 0.3s;
}

.mobile-menu-btn:active {
  transform: scale(0.98);
}

.mobile-overlay {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(-100%);
}

@media (min-width: 769px) {
  .mobile-nav {
    display: none;
  }
}
</style>
