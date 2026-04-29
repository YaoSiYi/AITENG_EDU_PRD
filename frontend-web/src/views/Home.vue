<template>
  <div class="home-container">
    <!-- 反重力粒子背景 -->
    <BackgroundParticles />
    <nav class="navbar">
      <div class="nav-content">
        <div class="logo">艾腾教育</div>
        <div class="nav-links">
          <router-link to="/questions" class="nav-link">题库</router-link>
          <router-link to="/activities" class="nav-link">活动</router-link>
          <router-link to="/stats" class="nav-link">统计</router-link>
          <router-link to="/seats" class="nav-link">查看座次</router-link>
          <router-link to="/wrong-book" class="nav-link">错题本</router-link>
          <router-link v-if="userStore.isAuthenticated" to="/testcases" class="nav-link">测试用例</router-link>
          <router-link v-if="userStore.isAuthenticated" to="/dashboard" class="nav-link">数据看板</router-link>
          <router-link v-if="userStore.isAdmin" to="/admin" class="nav-link admin-link">管理后台</router-link>

          <!-- 个人中心下拉菜单 -->
          <el-dropdown v-if="userStore.isAuthenticated" trigger="hover" @command="handleCommand">
            <span class="nav-link profile-dropdown">
              个人中心
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  <span>个人资料</span>
                </el-dropdown-item>
                <el-dropdown-item command="online" divided>
                  <el-icon><View /></el-icon>
                  <span>{{ showOnlineStatus ? '隐藏' : '显示' }}在线状态</span>
                </el-dropdown-item>
                <el-dropdown-item command="public">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>{{ publicLearningData ? '隐藏' : '公开' }}学习数据</span>
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon style="color: #f56c6c"><SwitchButton /></el-icon>
                  <span style="color: #f56c6c">退出账号</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <router-link v-else to="/login" class="nav-link-btn">登录</router-link>
        </div>
      </div>
    </nav>

    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">软件测试全栈工程师</h1>
        <p class="hero-subtitle">十年磨一剑 · 助力零基础到高级软件测试工程师</p>
        <div class="hero-actions">
          <HoverBorderGlow>
            <el-button type="primary" size="large" @click="$router.push('/questions')">
              开始学习
            </el-button>
          </HoverBorderGlow>
          <HoverBorderGlow>
            <el-button size="large" @click="$router.push('/activities')">
              查看活动
            </el-button>
          </HoverBorderGlow>
          <HoverBorderGlow>
            <el-button size="large" style="background: #10b981; border-color: #10b981; color: #fff;" @click="$router.push('/seats')">
              查看座次
            </el-button>
          </HoverBorderGlow>
        </div>
      </div>
      <div class="hero-visual">
        <div class="floating-card card-1">
          <el-icon><TrendCharts /></el-icon>
          <span>10阶段课程体系</span>
        </div>
        <div class="floating-card card-2">
          <el-icon><Document /></el-icon>
          <span>3大实战项目</span>
        </div>
        <div class="floating-card card-3">
          <el-icon><Trophy /></el-icon>
          <span>AI大模型测试</span>
        </div>
      </div>

      <!-- 右侧悬浮展示框 -->
      <div class="stats-sidebar">
        <!-- 优秀学员展示 -->
        <div class="stats-card excellent-students">
          <div class="card-header">
            <el-icon><Star /></el-icon>
            <h3>优秀学员</h3>
          </div>
          <div class="card-content">
            <div
              v-for="student in excellentStudents"
              :key="student.id"
              class="student-item"
            >
              <div class="student-avatar">
                <img v-if="student.avatar" :src="student.avatar" :alt="student.name" />
                <div v-else class="avatar-placeholder">{{ student.name.charAt(0) }}</div>
              </div>
              <div class="student-info">
                <div class="student-name">{{ student.name }}</div>
                <div class="student-company">{{ student.company }}</div>
                <div class="student-salary">{{ student.salary }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 学员统计 -->
        <div class="stats-card student-stats">
          <div class="card-header">
            <el-icon><User /></el-icon>
            <h3>学员统计</h3>
          </div>
          <div class="card-content">
            <div class="stat-item">
              <div class="stat-label">累计学员</div>
              <div class="stat-value">{{ studentStats.total }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">在读学员</div>
              <div class="stat-value">{{ studentStats.current }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">毕业学员</div>
              <div class="stat-value">{{ studentStats.graduated }}</div>
            </div>
          </div>
        </div>

        <!-- 就业统计 -->
        <div class="stats-card employment-stats">
          <div class="card-header">
            <el-icon><Briefcase /></el-icon>
            <h3>就业统计</h3>
          </div>
          <div class="card-content">
            <div class="stat-item">
              <div class="stat-label">就业率</div>
              <div class="stat-value highlight">{{ employmentStats.rate }}%</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">平均薪资</div>
              <div class="stat-value">{{ employmentStats.avgSalary }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">最高薪资</div>
              <div class="stat-value highlight">{{ employmentStats.maxSalary }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/utils/request'
import BackgroundParticles from '@/components/BackgroundParticles.vue'
import HoverBorderGlow from '@/components/HoverBorderGlow.vue'

const router = useRouter()
const userStore = useUserStore()

// 用户设置状态
const showOnlineStatus = ref(true)
const publicLearningData = ref(false)

// 优秀学员数据
const excellentStudents = ref([
  {
    id: 1,
    name: '张三',
    avatar: '',
    company: '腾讯',
    salary: '25K'
  },
  {
    id: 2,
    name: '李四',
    avatar: '',
    company: '阿里巴巴',
    salary: '28K'
  },
  {
    id: 3,
    name: '王五',
    avatar: '',
    company: '字节跳动',
    salary: '30K'
  }
])

// 学员统计数据
const studentStats = ref({
  total: 0,
  current: 0,
  graduated: 0
})

// 就业统计数据
const employmentStats = ref({
  rate: 0,
  avgSalary: '0K',
  maxSalary: '0K'
})

// 加载优秀学员数据
const loadExcellentStudents = async () => {
  try {
    const response = await api.get('/api/stats/excellent-students/')
    console.log('优秀学员 API 响应:', response)
    if (response && response.length > 0) {
      excellentStudents.value = response.slice(0, 3)
      console.log('优秀学员数据已更新:', excellentStudents.value)
    }
  } catch (error) {
    console.error('加载优秀学员失败:', error)
  }
}

// 加载学员统计数据
const loadStudentStats = async () => {
  try {
    const response = await api.get('/api/stats/student-stats/')
    console.log('学员统计 API 响应:', response)
    if (response) {
      studentStats.value = {
        total: response.total || 0,
        current: response.current || 0,
        graduated: response.graduated || 0
      }
      console.log('学员统计数据已更新:', studentStats.value)
    }
  } catch (error) {
    console.error('加载学员统计失败:', error)
  }
}

// 加载就业统计数据
const loadEmploymentStats = async () => {
  try {
    const response = await api.get('/api/stats/employment-stats/')
    console.log('就业统计 API 响应:', response)
    if (response) {
      employmentStats.value = {
        rate: response.rate || 0,
        avgSalary: response.avg_salary || '0K',
        maxSalary: response.max_salary || '0K'
      }
      console.log('就业统计数据已更新:', employmentStats.value)
    }
  } catch (error) {
    console.error('加载就业统计失败:', error)
  }
}

// 处理下拉菜单命令
const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'online':
      showOnlineStatus.value = !showOnlineStatus.value
      ElMessage.success(showOnlineStatus.value ? '已显示在线状态' : '已隐藏在线状态')
      break
    case 'public':
      publicLearningData.value = !publicLearningData.value
      ElMessage.success(publicLearningData.value ? '学习数据已公开' : '学习数据已隐藏')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm(
    '确定要退出当前账号吗？',
    '退出确认',
    {
      confirmButtonText: '确定退出',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }).catch(() => {
    // 用户取消
  })
}

// 页面加载时获取数据
onMounted(() => {
  loadExcellentStudents()
  loadStudentStats()
  loadEmploymentStats()
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(10, 14, 39, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  gap: 32px;
  align-items: center;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #fff;
}

.profile-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  transition: transform 0.2s;
}

.nav-link-btn:hover {
  transform: translateY(-2px);
}

.hero {
  padding: 160px 40px 80px;
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr 320px;
  gap: 60px;
  align-items: start;
  position: relative;
}

@media (max-width: 1200px) {
  .hero {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }

  .stats-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    padding: 100px 20px 40px;
    gap: 40px;
  }

  .nav-links {
    display: none;
  }
}

.hero-title {
  font-size: 56px;
  font-weight: 900;
  color: #fff;
  line-height: 1.1;
  margin-bottom: 24px;
  letter-spacing: -2px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
    letter-spacing: -1px;
  }
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 40px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-subtitle {
    font-size: 16px;
    margin-bottom: 32px;
  }
}

.hero-actions {
  display: flex;
  gap: 16px;
}

@media (max-width: 768px) {
  .hero-actions {
    flex-direction: column;
  }

  .hero-actions .el-button {
    width: 100%;
  }
}

.hero-visual {
  position: relative;
  height: 400px;
}

@media (max-width: 768px) {
  .hero-visual {
    height: 300px;
  }
}

.floating-card {
  position: absolute;
  padding: 24px 32px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #fff;
  font-weight: 600;
  animation: float-card 6s ease-in-out infinite;
}

.floating-card .el-icon {
  font-size: 24px;
  color: #667eea;
}

.card-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: 10%;
  animation-delay: 2s;
}

.card-3 {
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float-card {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 右侧悬浮展示框样式 */
.stats-sidebar {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s;
}

.stats-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header .el-icon {
  font-size: 20px;
  color: #667eea;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 优秀学员样式 */
.student-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  transition: all 0.3s;
}

.student-item:hover {
  background: rgba(255, 255, 255, 0.06);
  transform: translateX(4px);
}

.student-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.student-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 20px;
  font-weight: 700;
}

.student-info {
  flex: 1;
  min-width: 0;
}

.student-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.student-company {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 2px;
}

.student-salary {
  font-size: 13px;
  font-weight: 700;
  color: #f093fb;
}

/* 统计数据样式 */
.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
}

.stat-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.stat-value.highlight {
  color: #f093fb;
  font-size: 20px;
}

.card-1 {
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: 10%;
  animation-delay: 2s;
}

.card-3 {
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float-card {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
</style>
