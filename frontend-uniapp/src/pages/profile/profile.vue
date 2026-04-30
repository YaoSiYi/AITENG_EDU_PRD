<template>
  <view class="profile-container">
    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="user-info">
        <image :src="userAvatar" class="avatar" @click="handleAvatarClick"></image>
        <view class="user-details">
          <text class="nickname">{{ userNickname }}</text>
          <text class="role">{{ userRoleText }}</text>
        </view>
      </view>

      <!-- 学习统计 -->
      <view class="stats-row">
        <view class="stat-item">
          <text class="stat-value">{{ userStats.questionCount }}</text>
          <text class="stat-label">已答题目</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ userStats.accuracy }}%</text>
          <text class="stat-label">正确率</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ userStats.studyDays }}</text>
          <text class="stat-label">学习天数</text>
        </view>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-item" @click="goToWrongBook">
        <view class="menu-left">
          <text class="menu-icon">📝</text>
          <text class="menu-text">我的错题本</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>

      <view class="menu-item" @click="goToMyActivities">
        <view class="menu-left">
          <text class="menu-icon">🎯</text>
          <text class="menu-text">我的活动</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>

      <view class="menu-item" @click="goToSettings">
        <view class="menu-left">
          <text class="menu-icon">⚙️</text>
          <text class="menu-text">设置</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
    </view>

    <!-- 其他功能 -->
    <view class="menu-section">
      <view class="menu-item" @click="handleAbout">
        <view class="menu-left">
          <text class="menu-icon">ℹ️</text>
          <text class="menu-text">关于我们</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>

      <view class="menu-item" @click="handleFeedback">
        <view class="menu-left">
          <text class="menu-icon">💬</text>
          <text class="menu-text">意见反馈</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
    </view>

    <!-- 退出登录 -->
    <view v-if="isLoggedIn" class="logout-section">
      <button class="btn-logout" @click="handleLogout">退出登录</button>
    </view>
    <view v-else class="logout-section">
      <button class="btn-login" @click="goToLogin">立即登录</button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const userStats = ref({
  questionCount: 0,
  accuracy: 0,
  studyDays: 0
})

// 是否已登录
const isLoggedIn = computed(() => userStore.hasLogin)

// 用户头像
const userAvatar = computed(() => userStore.avatar)

// 用户昵称
const userNickname = computed(() => userStore.nickname)

// 用户角色文本
const userRoleText = computed(() => {
  const roleMap = {
    admin: '管理员',
    teacher: '老师',
    student: '学生',
    guest: '游客'
  }
  return roleMap[userStore.userRole] || '游客'
})

onMounted(() => {
  if (isLoggedIn.value) {
    loadUserStats()
  }
})

// 加载用户统计
const loadUserStats = async () => {
  try {
    // TODO: 调用API获取用户统计数据
    // const res = await getUserStats()
    // userStats.value = res

    // 模拟数据
    userStats.value = {
      questionCount: 156,
      accuracy: 85,
      studyDays: 30
    }
  } catch (error) {
    console.error('Load user stats error:', error)
  }
}

// 点击头像
const handleAvatarClick = () => {
  if (!isLoggedIn.value) {
    goToLogin()
    return
  }

  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      const tempFilePath = res.tempFilePaths[0]
      // TODO: 上传头像
      console.log('Upload avatar:', tempFilePath)
      uni.showToast({
        title: '头像上传功能开发中',
        icon: 'none'
      })
    }
  })
}

// 跳转到错题本
const goToWrongBook = () => {
  if (!checkLogin()) return
  uni.navigateTo({
    url: '/pages/wrong-book/wrong-book'
  })
}

// 跳转到我的活动
const goToMyActivities = () => {
  if (!checkLogin()) return
  uni.navigateTo({
    url: '/pages/my-activities/my-activities'
  })
}

// 跳转到设置
const goToSettings = () => {
  if (!checkLogin()) return
  uni.navigateTo({
    url: '/pages/settings/settings'
  })
}

// 关于我们
const handleAbout = () => {
  uni.showModal({
    title: '关于我们',
    content: '艾腾教育 - 软件测试全栈工程师培训平台\n版本：v1.0.0',
    showCancel: false
  })
}

// 意见反馈
const handleFeedback = () => {
  uni.showToast({
    title: '意见反馈功能开发中',
    icon: 'none'
  })
}

// 退出登录
const handleLogout = () => {
  uni.showModal({
    title: '确认退出',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
      }
    }
  })
}

// 跳转到登录
const goToLogin = () => {
  uni.navigateTo({
    url: '/pages/login/login'
  })
}

// 检查登录状态
const checkLogin = () => {
  if (!isLoggedIn.value) {
    uni.showModal({
      title: '提示',
      content: '请先登录',
      success: (res) => {
        if (res.confirm) {
          goToLogin()
        }
      }
    })
    return false
  }
  return true
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 40rpx;
}

.user-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 32rpx 40rpx;
  margin-bottom: 20rpx;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 40rpx;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  border: 4rpx solid rgba(255, 255, 255, 0.3);
  margin-right: 24rpx;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.nickname {
  font-size: 36rpx;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 8rpx;
}

.role {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  padding: 8rpx 16rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8rpx;
  align-self: flex-start;
}

.stats-row {
  display: flex;
  justify-content: space-around;
  padding: 32rpx 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.menu-section {
  background: #ffffff;
  margin-bottom: 20rpx;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  border-bottom: 1rpx solid #f5f7fa;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-left {
  display: flex;
  align-items: center;
}

.menu-icon {
  font-size: 40rpx;
  margin-right: 24rpx;
}

.menu-text {
  font-size: 28rpx;
  color: #333333;
}

.menu-arrow {
  font-size: 40rpx;
  color: #cccccc;
}

.logout-section {
  padding: 0 32rpx;
  margin-top: 40rpx;
}

.btn-logout {
  width: 100%;
  height: 88rpx;
  background: #f56c6c;
  color: #ffffff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 12rpx;
  border: none;
}

.btn-login {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 12rpx;
  border: none;
}
</style>
