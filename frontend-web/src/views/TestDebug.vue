<template>
  <div class="test-debug">
    <h1>API 调试页面</h1>

    <el-card style="margin-bottom: 20px">
      <h3>认证状态</h3>
      <p>Token: {{ token ? '已设置' : '未设置' }}</p>
      <p>Token 值: {{ token ? token.substring(0, 50) + '...' : '-' }}</p>
      <el-button @click="testLogin">测试登录</el-button>
      <el-button @click="clearToken">清除 Token</el-button>
    </el-card>

    <el-card style="margin-bottom: 20px">
      <h3>API 测试</h3>
      <el-button @click="testGetList" type="primary">测试获取列表</el-button>
      <el-button @click="testGetUsers">测试获取用户列表</el-button>
    </el-card>

    <el-card>
      <h3>响应结果</h3>
      <pre style="max-height: 400px; overflow: auto; background: #f5f5f5; padding: 10px">{{ response }}</pre>
    </el-card>

    <el-card style="margin-top: 20px">
      <h3>错误信息</h3>
      <pre style="max-height: 200px; overflow: auto; background: #fff3f3; padding: 10px; color: red">{{ error }}</pre>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getTestcaseList, getAssignableUsers } from '@/api/testcases'
import request from '@/utils/request'

const token = ref('')
const response = ref('')
const error = ref('')

onMounted(() => {
  token.value = localStorage.getItem('token') || ''
})

const testLogin = async () => {
  try {
    error.value = ''
    response.value = '正在登录...'

    const res = await request({
      url: '/api/users/login/',
      method: 'post',
      data: {
        username: 'admin',
        password: 'admin123'
      }
    })

    response.value = JSON.stringify(res, null, 2)

    if (res.access) {
      localStorage.setItem('token', res.access)
      token.value = res.access
      ElMessage.success('登录成功')
    }
  } catch (err) {
    error.value = JSON.stringify(err, null, 2)
    ElMessage.error('登录失败')
  }
}

const clearToken = () => {
  localStorage.removeItem('token')
  token.value = ''
  ElMessage.success('Token 已清除')
}

const testGetList = async () => {
  try {
    error.value = ''
    response.value = '正在获取列表...'

    const res = await getTestcaseList({ page: 1, limit: 5 })

    response.value = JSON.stringify({
      count: res.count,
      results_length: res.results?.length,
      first_item: res.results?.[0]
    }, null, 2)

    ElMessage.success(`获取成功，共 ${res.count} 条数据`)
  } catch (err) {
    error.value = JSON.stringify({
      message: err.message,
      response: err.response?.data,
      status: err.response?.status
    }, null, 2)
    ElMessage.error('获取列表失败')
  }
}

const testGetUsers = async () => {
  try {
    error.value = ''
    response.value = '正在获取用户列表...'

    const res = await getAssignableUsers()

    response.value = JSON.stringify(res, null, 2)

    ElMessage.success(`获取成功，共 ${res.length || res.data?.length} 个用户`)
  } catch (err) {
    error.value = JSON.stringify({
      message: err.message,
      response: err.response?.data,
      status: err.response?.status
    }, null, 2)
    ElMessage.error('获取用户列表失败')
  }
}
</script>

<style scoped>
.test-debug {
  padding: 20px;
}

h3 {
  margin-top: 0;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
