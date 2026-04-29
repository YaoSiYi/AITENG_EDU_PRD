<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="register-title">创建账号</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="0">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="nickname">
          <el-input
            v-model="form.nickname"
            placeholder="昵称"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><Avatar /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="phone">
          <el-input
            v-model="form.phone"
            placeholder="手机号"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><Iphone /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="hometown">
          <el-input
            v-model="form.hometown"
            placeholder="籍贯（格式：xx省xx市）"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><Location /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码（6-20位）"
            size="large"
            show-password
            clearable
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="确认密码"
            size="large"
            show-password
            clearable
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="passwordHint">
          <el-input
            v-model="form.passwordHint"
            placeholder="密码提示（选填，用于找回密码）"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><QuestionFilled /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="gender" class="gender-item">
          <div class="gender-container">
            <div class="gender-label">
              <el-icon><User /></el-icon>
              <span>性别</span>
              <span class="required">*</span>
            </div>
            <el-radio-group v-model="form.gender" size="large">
              <el-radio value="male" class="male-radio">男</el-radio>
              <el-radio value="female" class="female-radio">女</el-radio>
            </el-radio-group>
          </div>
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="register-btn"
          @click="handleRegister"
          :loading="loading"
        >
          注册
        </el-button>

        <div class="login-hint">
          已有账号？<router-link to="/login">立即登录</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/utils/request'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  nickname: '',
  phone: '',
  hometown: '',
  password: '',
  confirmPassword: '',
  passwordHint: '',
  gender: ''
})

// 验证籍贯格式
const validateHometown = (rule, value, callback) => {
  if (!value) {
    callback()
    return
  }
  const pattern = /^.+省.+市$/
  if (!pattern.test(value)) {
    callback(new Error('籍贯格式应为：xx省xx市'))
  } else {
    callback()
  }
}

// 验证确认密码
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为 3-20 位字符', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 50, message: '昵称长度为 2-50 位字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  hometown: [
    { validator: validateHometown, trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为 6-20 位字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  passwordHint: [
    { max: 200, message: '密码提示最多 200 个字符', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ]
}

const handleRegister = async () => {
  try {
    const valid = await formRef.value?.validate()
    if (!valid) return

    loading.value = true

    const response = await api.post('/api/users/register/', {
      username: form.username,
      nickname: form.nickname,
      phone: form.phone,
      hometown: form.hometown,
      password: form.password,
      confirm_password: form.confirmPassword,
      password_hint: form.passwordHint,
      gender: form.gender
    })

    ElMessage.success('注册成功！请登录')
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
    const errorMsg = error.response?.data?.message ||
                     error.response?.data?.error ||
                     error.response?.data?.username?.[0] ||
                     error.response?.data?.phone?.[0] ||
                     error.response?.data?.confirm_password?.[0] ||
                     '注册失败，请重试'
    ElMessage.error(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

.register-card {
  width: 100%;
  max-width: 480px;
  padding: 48px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.register-title {
  color: #fff;
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 32px;
}

.register-btn {
  width: 100%;
  margin-top: 16px;
  font-weight: 600;
}

.login-hint {
  text-align: center;
  margin-top: 16px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.login-hint a {
  color: #409eff;
  text-decoration: none;
  font-weight: 600;
}

.login-hint a:hover {
  color: #66b1ff;
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

:deep(.el-input__wrapper:hover) {
  background: rgba(255, 255, 255, 0.12);
}

:deep(.el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.15);
  border-color: #409eff;
}

:deep(.el-input__inner) {
  color: #fff;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.4);
}

:deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.6);
}

:deep(.el-icon) {
  color: rgba(255, 255, 255, 0.6);
}

.gender-item {
  margin-bottom: 24px;
}

.gender-container {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.gender-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  min-width: 60px;
}

.required {
  color: #f56c6c;
  font-size: 14px;
  margin-left: -4px;
}

:deep(.el-radio) {
  margin-right: 16px;
}

:deep(.el-radio__label) {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

:deep(.el-radio__inner) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.3);
}

/* 男生选中颜色 - 湖蓝色 */
:deep(.male-radio .el-radio__input.is-checked .el-radio__inner) {
  background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
  border-color: #22d3ee;
}

:deep(.male-radio .el-radio__input.is-checked + .el-radio__label) {
  color: #22d3ee;
}

/* 女生选中颜色 - 粉色 */
:deep(.female-radio .el-radio__input.is-checked .el-radio__inner) {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  border-color: #f472b6;
}

:deep(.female-radio .el-radio__input.is-checked + .el-radio__label) {
  color: #f472b6;
}
</style>
