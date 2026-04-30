<template>
  <view class="login-container">
    <!-- Logo区域 -->
    <view class="logo-section">
      <image class="logo" src="/static/images/logo.png" mode="aspectFit"></image>
      <text class="title">艾腾教育</text>
      <text class="subtitle">软件测试全栈工程师培训</text>
    </view>

    <!-- 登录表单 -->
    <view class="form-section">
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">👤</text>
          <input
            v-model="loginForm.username"
            placeholder="请输入用户名/手机号"
            placeholder-class="placeholder"
            class="input"
          />
        </view>
      </view>

      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">🔒</text>
          <input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            placeholder-class="placeholder"
            class="input"
          />
        </view>
      </view>

      <view class="options">
        <label class="remember">
          <checkbox :checked="rememberMe" @change="handleRememberChange" />
          <text>记住密码</text>
        </label>
        <text class="forgot" @click="handleForgotPassword">忘记密码？</text>
      </view>

      <button class="btn-login" @click="handleLogin" :loading="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>

      <!-- 微信登录 -->
      <!-- #ifdef MP-WEIXIN -->
      <button class="btn-wechat" @click="handleWechatLogin">
        <text class="wechat-icon">💬</text>
        微信一键登录
      </button>
      <!-- #endif -->

      <view class="register-link">
        <text>还没有账号？</text>
        <text class="link" @click="goToRegister">立即注册</text>
      </view>

      <!-- 游客登录 -->
      <view class="guest-login">
        <text class="link" @click="handleGuestLogin">游客模式</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const loginForm = ref({
  username: '',
  password: ''
})

const rememberMe = ref(false)
const loading = ref(false)

// 登录
const handleLogin = async () => {
  if (!loginForm.value.username) {
    uni.showToast({
      title: '请输入用户名',
      icon: 'none'
    })
    return
  }

  if (!loginForm.value.password) {
    uni.showToast({
      title: '请输入密码',
      icon: 'none'
    })
    return
  }

  try {
    loading.value = true
    await userStore.login(loginForm.value)

    uni.showToast({
      title: '登录成功',
      icon: 'success'
    })

    // 跳转到首页
    setTimeout(() => {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }, 1500)
  } catch (error) {
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}

// 微信登录
const handleWechatLogin = () => {
  uni.login({
    provider: 'weixin',
    success: async (loginRes) => {
      try {
        // 获取用户信息
        uni.getUserProfile({
          desc: '用于完善用户资料',
          success: async (infoRes) => {
            console.log('User info:', infoRes)
            // TODO: 调用后端微信登录接口
            await userStore.wechatLogin(loginRes.code)

            uni.showToast({
              title: '登录成功',
              icon: 'success'
            })

            setTimeout(() => {
              uni.switchTab({
                url: '/pages/index/index'
              })
            }, 1500)
          },
          fail: (err) => {
            console.error('Get user profile error:', err)
            uni.showToast({
              title: '获取用户信息失败',
              icon: 'none'
            })
          }
        })
      } catch (error) {
        console.error('Wechat login error:', error)
      }
    },
    fail: (err) => {
      console.error('Wechat login fail:', err)
      uni.showToast({
        title: '微信登录失败',
        icon: 'none'
      })
    }
  })
}

// 游客登录
const handleGuestLogin = () => {
  uni.showModal({
    title: '游客模式',
    content: '游客模式下部分功能受限，确定以游客身份继续吗？',
    success: (res) => {
      if (res.confirm) {
        uni.switchTab({
          url: '/pages/index/index'
        })
      }
    }
  })
}

// 记住密码
const handleRememberChange = (e) => {
  rememberMe.value = e.detail.value.length > 0
}

// 忘记密码
const handleForgotPassword = () => {
  uni.showToast({
    title: '请联系管理员重置密码',
    icon: 'none',
    duration: 2000
  })
}

// 跳转注册
const goToRegister = () => {
  uni.navigateTo({
    url: '/pages/register/register'
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 40rpx;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 80rpx;
}

.logo {
  width: 160rpx;
  height: 160rpx;
  margin-bottom: 30rpx;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 16rpx;
}

.subtitle {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

.form-section {
  background: #ffffff;
  border-radius: 24rpx;
  padding: 60rpx 40rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 32rpx;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border-radius: 12rpx;
  padding: 24rpx 32rpx;
}

.icon {
  font-size: 36rpx;
  margin-right: 20rpx;
}

.input {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
}

.placeholder {
  color: #999999;
}

.options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
  font-size: 26rpx;
}

.remember {
  display: flex;
  align-items: center;
  color: #666666;
}

.remember checkbox {
  margin-right: 12rpx;
}

.forgot {
  color: #667eea;
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
  margin-bottom: 24rpx;
}

.btn-wechat {
  width: 100%;
  height: 88rpx;
  background: #07c160;
  color: #ffffff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 12rpx;
  border: none;
  margin-bottom: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wechat-icon {
  font-size: 36rpx;
  margin-right: 12rpx;
}

.register-link {
  text-align: center;
  font-size: 26rpx;
  color: #666666;
  margin-bottom: 24rpx;
}

.link {
  color: #667eea;
  margin-left: 8rpx;
}

.guest-login {
  text-align: center;
  font-size: 26rpx;
  padding-top: 24rpx;
  border-top: 1rpx solid #eeeeee;
}
</style>
