<template>
  <view class="register-container">
    <!-- Logo区域 -->
    <view class="logo-section">
      <image class="logo" src="/static/images/banner1.svg" mode="aspectFit"></image>
      <text class="title">艾腾教育</text>
      <text class="subtitle">创建新账号</text>
    </view>

    <!-- 注册表单 -->
    <view class="form-section">
      <!-- 用户名 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">👤</text>
          <input
            v-model="registerForm.username"
            placeholder="用户名（3-20位字母或字母+数字）"
            placeholder-class="placeholder"
            class="input"
            maxlength="20"
          />
        </view>
        <view class="input-hint">
          <text>仅支持字母或字母+数字组合，如：zhangsan、user123</text>
        </view>
      </view>

      <!-- 昵称 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">😊</text>
          <input
            v-model="registerForm.nickname"
            placeholder="昵称（2-50位）"
            placeholder-class="placeholder"
            class="input"
            maxlength="50"
          />
        </view>
      </view>

      <!-- 手机号 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">📱</text>
          <input
            v-model="registerForm.phone"
            type="number"
            placeholder="手机号"
            placeholder-class="placeholder"
            class="input"
            maxlength="11"
          />
        </view>
      </view>

      <!-- 籍贯 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">📍</text>
          <input
            v-model="registerForm.hometown"
            placeholder="籍贯（格式：xx省xx市，选填）"
            placeholder-class="placeholder"
            class="input"
          />
        </view>
      </view>

      <!-- 期数 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">📅</text>
          <input
            v-model="registerForm.period"
            type="number"
            placeholder="期数（格式：YYYYMMDD，如：20240101）"
            placeholder-class="placeholder"
            class="input"
            maxlength="8"
          />
        </view>
        <view class="input-hint">
          <text>请输入8位数字的日期，如：20240101表示2024年01月01日</text>
        </view>
      </view>

      <!-- 密码 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">🔒</text>
          <input
            v-model="registerForm.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="密码（6-20位）"
            placeholder-class="placeholder"
            class="input"
            maxlength="20"
          />
          <text class="eye-icon" @click="togglePassword">
            {{ showPassword ? '👁️' : '👁️‍🗨️' }}
          </text>
        </view>
      </view>

      <!-- 确认密码 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">🔒</text>
          <input
            v-model="registerForm.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            placeholder="确认密码"
            placeholder-class="placeholder"
            class="input"
            maxlength="20"
          />
          <text class="eye-icon" @click="toggleConfirmPassword">
            {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
          </text>
        </view>
      </view>

      <!-- 密码提示 -->
      <view class="input-group">
        <view class="input-wrapper">
          <text class="icon">❓</text>
          <input
            v-model="registerForm.passwordHint"
            placeholder="密码提示（选填，用于找回密码）"
            placeholder-class="placeholder"
            class="input"
            maxlength="200"
          />
        </view>
      </view>

      <!-- 性别 -->
      <view class="input-group">
        <view class="gender-wrapper">
          <view class="gender-label">
            <text class="icon">👥</text>
            <text>性别</text>
            <text class="required">*</text>
          </view>
          <radio-group class="gender-radio-group" @change="handleGenderChange">
            <label class="gender-radio male-radio">
              <radio value="male" :checked="registerForm.gender === 'male'" color="#22d3ee" />
              <text>男</text>
            </label>
            <label class="gender-radio female-radio">
              <radio value="female" :checked="registerForm.gender === 'female'" color="#f472b6" />
              <text>女</text>
            </label>
          </radio-group>
        </view>
      </view>

      <!-- 用户协议 -->
      <view class="agreement">
        <checkbox-group @change="handleAgreeChange">
          <label class="agreement-label">
            <checkbox value="agreed" :checked="agreed" color="#667eea" />
            <text>我已阅读并同意</text>
            <text class="link" @click.stop="showAgreement">《用户协议》</text>
            <text>和</text>
            <text class="link" @click.stop="showPrivacy">《隐私政策》</text>
          </label>
        </checkbox-group>
      </view>

      <!-- 注册按钮 -->
      <button class="btn-register" @click="handleRegister" :loading="loading">
        {{ loading ? '注册中...' : '立即注册' }}
      </button>

      <!-- 登录链接 -->
      <view class="login-link">
        <text>已有账号？</text>
        <text class="link" @click="goToLogin">立即登录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const registerForm = ref({
  username: '',
  nickname: '',
  phone: '',
  hometown: '',
  period: '',
  password: '',
  confirmPassword: '',
  passwordHint: '',
  gender: ''
})

const agreed = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// 切换密码显示/隐藏
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// 切换确认密码显示/隐藏
const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

// 性别变化
const handleGenderChange = (e) => {
  registerForm.value.gender = e.detail.value
}

// 注册
const handleRegister = async () => {
  // 表单验证
  if (!registerForm.value.username) {
    uni.showToast({
      title: '请输入用户名',
      icon: 'none'
    })
    return
  }

  if (registerForm.value.username.length < 3 || registerForm.value.username.length > 20) {
    uni.showToast({
      title: '用户名长度为3-20位',
      icon: 'none'
    })
    return
  }

  // 验证用户名格式：只支持字母或字母+数字
  if (!/^[a-zA-Z][a-zA-Z0-9]*$/.test(registerForm.value.username)) {
    uni.showToast({
      title: '用户名只能包含字母和数字，且必须以字母开头',
      icon: 'none',
      duration: 3000
    })
    return
  }

  if (!registerForm.value.nickname) {
    uni.showToast({
      title: '请输入昵称',
      icon: 'none'
    })
    return
  }

  if (registerForm.value.nickname.length < 2 || registerForm.value.nickname.length > 50) {
    uni.showToast({
      title: '昵称长度为2-50位',
      icon: 'none'
    })
    return
  }

  if (!registerForm.value.phone) {
    uni.showToast({
      title: '请输入手机号',
      icon: 'none'
    })
    return
  }

  if (!/^1[3-9]\d{9}$/.test(registerForm.value.phone)) {
    uni.showToast({
      title: '请输入正确的手机号',
      icon: 'none'
    })
    return
  }

  // 验证籍贯格式（如果填写了）
  if (registerForm.value.hometown && !/^.+省.+市$/.test(registerForm.value.hometown)) {
    uni.showToast({
      title: '籍贯格式应为：xx省xx市',
      icon: 'none',
      duration: 3000
    })
    return
  }

  // 验证期数格式（必填）
  if (!registerForm.value.period) {
    uni.showToast({
      title: '请输入期数',
      icon: 'none'
    })
    return
  }

  if (!/^\d{8}$/.test(registerForm.value.period)) {
    uni.showToast({
      title: '期数格式应为8位数字，如：20240101',
      icon: 'none',
      duration: 3000
    })
    return
  }

  // 验证日期有效性
  const year = parseInt(registerForm.value.period.substring(0, 4))
  const month = parseInt(registerForm.value.period.substring(4, 6))
  const day = parseInt(registerForm.value.period.substring(6, 8))

  if (year < 2000 || year > 2100) {
    uni.showToast({
      title: '年份应在2000-2100之间',
      icon: 'none',
      duration: 3000
    })
    return
  }

  if (month < 1 || month > 12) {
    uni.showToast({
      title: '月份应在01-12之间',
      icon: 'none',
      duration: 3000
    })
    return
  }

  if (day < 1 || day > 31) {
    uni.showToast({
      title: '日期应在01-31之间',
      icon: 'none',
      duration: 3000
    })
    return
  }

  if (!registerForm.value.password) {
    uni.showToast({
      title: '请输入密码',
      icon: 'none'
    })
    return
  }

  if (registerForm.value.password.length < 6 || registerForm.value.password.length > 20) {
    uni.showToast({
      title: '密码长度为6-20位',
      icon: 'none'
    })
    return
  }

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    uni.showToast({
      title: '两次密码输入不一致',
      icon: 'none'
    })
    return
  }

  if (!registerForm.value.gender) {
    uni.showToast({
      title: '请选择性别',
      icon: 'none'
    })
    return
  }

  if (!agreed.value) {
    uni.showToast({
      title: '请阅读并同意用户协议',
      icon: 'none'
    })
    return
  }

  try {
    loading.value = true

    // 调用注册API
    await userStore.register({
      username: registerForm.value.username,
      nickname: registerForm.value.nickname,
      phone: registerForm.value.phone,
      hometown: registerForm.value.hometown || undefined,
      period: registerForm.value.period,
      password: registerForm.value.password,
      confirm_password: registerForm.value.confirmPassword,
      password_hint: registerForm.value.passwordHint || undefined,
      gender: registerForm.value.gender
    })

    uni.showToast({
      title: '注册成功',
      icon: 'success'
    })

    // 跳转到登录页
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error) {
    console.error('Register error:', error)
    // 显示具体的错误信息
    if (error.message && error.message !== '请求失败') {
      uni.showToast({
        title: error.message,
        icon: 'none',
        duration: 3000
      })
    }
  } finally {
    loading.value = false
  }
}

// 同意协议
const handleAgreeChange = (e) => {
  agreed.value = e.detail.value.length > 0
}

// 显示用户协议
const showAgreement = () => {
  uni.showModal({
    title: '用户协议',
    content: '这里是用户协议内容...',
    showCancel: false
  })
}

// 显示隐私政策
const showPrivacy = () => {
  uni.showModal({
    title: '隐私政策',
    content: '这里是隐私政策内容...',
    showCancel: false
  })
}

// 返回登录
const goToLogin = () => {
  uni.navigateBack()
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 48rpx;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 60rpx;
}

.logo {
  width: 140rpx;
  height: 140rpx;
  margin-bottom: 24rpx;
  border-radius: 20rpx;
}

.title {
  font-size: 44rpx;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 12rpx;
}

.subtitle {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.8);
}

.form-section {
  background: #ffffff;
  border-radius: 24rpx;
  padding: 48rpx 40rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 28rpx;
}

.input-hint {
  margin-top: 8rpx;
  padding-left: 48rpx;
  font-size: 22rpx;
  color: #999999;
  line-height: 1.5;
}

.input-wrapper {
  display: flex;
  align-items: center;
  padding: 24rpx 28rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
  border: 2rpx solid transparent;
  transition: all 0.3s;
  position: relative;
}

.input-wrapper:focus-within {
  background: #ffffff;
  border-color: #667eea;
}

.icon {
  font-size: 32rpx;
  margin-right: 16rpx;
}

.input {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
}

.placeholder {
  color: #999999;
}

.eye-icon {
  font-size: 36rpx;
  padding: 0 8rpx;
  cursor: pointer;
}

.gender-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx 28rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
}

.gender-label {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 28rpx;
  color: #333333;
}

.required {
  color: #f56c6c;
  font-size: 28rpx;
}

.gender-radio-group {
  display: flex;
  gap: 32rpx;
}

.gender-radio {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.gender-radio text {
  font-size: 28rpx;
  color: #333333;
}

.male-radio radio:checked ~ text {
  color: #22d3ee;
  font-weight: bold;
}

.female-radio radio:checked ~ text {
  color: #f472b6;
  font-weight: bold;
}

.agreement {
  margin-bottom: 32rpx;
  font-size: 24rpx;
  color: #666666;
}

.agreement-label {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.agreement checkbox {
  margin-right: 8rpx;
  transform: scale(0.9);
}

.link {
  color: #667eea;
  margin: 0 4rpx;
  font-weight: bold;
}

.btn-register {
  width: 100%;
  padding: 28rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 12rpx;
  border: none;
  margin-bottom: 28rpx;
}

.btn-register:active {
  opacity: 0.8;
}

.login-link {
  text-align: center;
  font-size: 26rpx;
  color: #666666;
}

.login-link .link {
  color: #667eea;
  font-weight: bold;
  margin-left: 8rpx;
}
</style>
