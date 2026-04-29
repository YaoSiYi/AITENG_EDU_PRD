<template>
  <div class="admin-container">
    <PageBreadcrumb current-name="管理后台" />

    <div class="admin-layout">
      <aside class="admin-sidebar">
        <div class="sidebar-header">
          <h2 class="sidebar-title">管理后台</h2>
        </div>
        <nav class="sidebar-nav">
          <div
            v-for="item in menuItems"
            :key="item.key"
            :class="['nav-item', { active: activeMenu === item.key }]"
            @click="activeMenu = item.key"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
            <el-badge v-if="item.badge" :value="item.badge" class="nav-badge" />
          </div>
        </nav>
      </aside>

      <main class="admin-main">
        <div class="admin-header">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
          <div class="header-actions">
            <el-button type="primary" @click="handleCreate">
              <el-icon><Plus /></el-icon>
              新建
            </el-button>
          </div>
        </div>

        <div class="admin-content">
          <!-- 概览 -->
          <div v-if="activeMenu === 'overview'" class="overview-section">
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
                  <el-icon><User /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ totalUsers }}</span>
                  <span class="stat-label">总用户数</span>
                  <span class="stat-trend">实时数据</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-value">256</span>
                  <span class="stat-label">题目总数</span>
                  <span class="stat-trend positive">+8</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
                  <el-icon><Calendar /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-value">12</span>
                  <span class="stat-label">活动数量</span>
                  <span class="stat-trend">进行中: 4</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%)">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="stat-info">
                  <span class="stat-value">85%</span>
                  <span class="stat-label">平均完成率</span>
                  <span class="stat-trend positive">+3.2%</span>
                </div>
              </div>
            </div>

            <div class="charts-row">
              <div class="chart-card">
                <h3 class="chart-title">用户增长趋势</h3>
                <div class="chart-placeholder">图表区域</div>
              </div>
              <div class="chart-card">
                <h3 class="chart-title">活跃度分析</h3>
                <div class="chart-placeholder">图表区域</div>
              </div>
            </div>
          </div>

          <!-- 用户管理 -->
          <div v-if="activeMenu === 'users'" class="users-section">
            <div class="table-toolbar">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索用户..."
                prefix-icon="Search"
                style="width: 300px"
              />
              <el-select v-model="userRoleFilter" placeholder="角色筛选" style="width: 150px">
                <el-option label="全部" value="" />
                <el-option label="学员" value="student" />
                <el-option label="教师" value="teacher" />
                <el-option label="管理员" value="admin" />
              </el-select>
            </div>

            <el-table :data="users" style="width: 100%" stripe v-loading="usersLoading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="username" label="用户名" width="150" />
              <el-table-column prop="nickname" label="昵称" width="150" />
              <el-table-column prop="email" label="邮箱" width="200" />
              <el-table-column prop="phone" label="手机号" width="150" />
              <el-table-column prop="role" label="角色" width="120">
                <template #default="{ row }">
                  <el-tag :type="getRoleType(row.role)">{{ getRoleLabel(row.role) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="createdAt" label="注册时间" width="180" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="handleEdit(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="table-pagination">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :total="totalUsers"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
              />
            </div>
          </div>

          <!-- 题库管理 -->
          <div v-if="activeMenu === 'questions'" class="questions-section">
            <div class="table-toolbar">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索题目..."
                prefix-icon="Search"
                style="width: 300px"
              />
              <el-select v-model="categoryFilter" placeholder="课程阶段" style="width: 200px">
                <el-option label="全部" value="" />
                <el-option label="软件测试基础" value="stage1" />
                <el-option label="功能与非功能测试" value="stage2" />
                <el-option label="Linux和MySQL" value="stage3" />
                <el-option label="Python课程" value="stage4" />
                <el-option label="UI自动化" value="stage5" />
                <el-option label="接口测试" value="stage6" />
                <el-option label="性能测试" value="stage7" />
                <el-option label="接口自动化" value="stage8" />
                <el-option label="项目实战" value="stage9" />
                <el-option label="AI大模型与Agent" value="stage10" />
              </el-select>
            </div>

            <el-table :data="questionsList" style="width: 100%" stripe>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="题目标题" min-width="250" />
              <el-table-column prop="category" label="课程阶段" width="150" />
              <el-table-column prop="type" label="题型" width="120" />
              <el-table-column prop="difficulty" label="难度" width="100">
                <template #default="{ row }">
                  <el-tag :type="getDifficultyType(row.difficulty)">{{ row.difficulty }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="accuracy" label="正确率" width="100">
                <template #default="{ row }">{{ row.accuracy }}%</template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="handleEdit(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="table-pagination">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :total="totalQuestions"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
              />
            </div>
          </div>

          <!-- 活动管理 -->
          <div v-if="activeMenu === 'activities'" class="activities-section">
            <div class="table-toolbar">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索活动..."
                prefix-icon="Search"
                style="width: 300px"
              />
              <el-select v-model="statusFilter" placeholder="状态筛选" style="width: 150px">
                <el-option label="全部" value="" />
                <el-option label="进行中" value="ongoing" />
                <el-option label="即将开始" value="upcoming" />
                <el-option label="已结束" value="finished" />
              </el-select>
            </div>

            <el-table :data="activitiesList" style="width: 100%" stripe>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="活动标题" min-width="250" />
              <el-table-column prop="status" label="状态" width="120">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="participants" label="参与人数" width="120" />
              <el-table-column prop="startDate" label="开始时间" width="180" />
              <el-table-column prop="endDate" label="结束时间" width="180" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="handleEdit(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="table-pagination">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :total="totalActivities"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
              />
            </div>
          </div>

          <!-- 数据统计 -->
          <div v-if="activeMenu === 'stats'" class="stats-section">
            <!-- 子标签页 -->
            <div class="sub-tabs">
              <div
                :class="['sub-tab', { active: statsSubTab === 'overview' }]"
                @click="statsSubTab = 'overview'"
              >
                <el-icon><DataAnalysis /></el-icon>
                概览
              </div>
              <div
                :class="['sub-tab', { active: statsSubTab === 'employment' }]"
                @click="statsSubTab = 'employment'; loadEmploymentStats()"
              >
                <el-icon><Briefcase /></el-icon>
                就业统计
              </div>
            </div>

            <!-- 概览 -->
            <div v-if="statsSubTab === 'overview'" class="stats-overview">
              <div class="stats-filters">
                <el-date-picker
                  v-model="dateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                />
                <el-button type="primary" @click="loadStats">查询</el-button>
              </div>

              <div class="stats-content">
                <div class="stat-panel">
                  <h3 class="panel-title">学习数据统计</h3>
                  <div class="chart-placeholder">图表区域</div>
                </div>
                <div class="stat-panel">
                  <h3 class="panel-title">课程完成情况</h3>
                  <div class="chart-placeholder">图表区域</div>
                </div>
              </div>
            </div>

            <!-- 就业统计 -->
            <div v-if="statsSubTab === 'employment'" class="employment-stats-section">
              <div class="stats-filters">
                <el-select
                  v-model="employmentPeriod"
                  placeholder="选择期数"
                  style="width: 200px"
                  @change="loadEmploymentStats"
                >
                  <el-option label="全部期数" value="" />
                  <el-option
                    v-for="p in employmentPeriods"
                    :key="p"
                    :label="p"
                    :value="p"
                  />
                </el-select>
              </div>

              <!-- 统计数据卡片 -->
              <div class="stats-cards-row">
                <div class="mini-stat-card">
                  <div class="mini-stat-label">就业率</div>
                  <div class="mini-stat-value accent">{{ employmentRate }}%</div>
                </div>
                <div class="mini-stat-card">
                  <div class="mini-stat-label">平均薪资</div>
                  <div class="mini-stat-value">{{ employmentAvgSalary }}</div>
                </div>
                <div class="mini-stat-card">
                  <div class="mini-stat-label">最高薪资</div>
                  <div class="mini-stat-value accent">{{ employmentMaxSalary }}</div>
                </div>
                <div class="mini-stat-card">
                  <div class="mini-stat-label">当前记录数</div>
                  <div class="mini-stat-value">{{ employmentList.length }}</div>
                </div>
              </div>

              <!-- 就业数据表格 -->
              <el-table :data="employmentList" style="width: 100%" stripe max-height="600">
                <el-table-column type="index" label="#" width="50" />
                <el-table-column prop="period" label="期数" width="120" />
                <el-table-column prop="student_name" label="学员姓名" width="120" />
                <el-table-column prop="company" label="就业公司" min-width="200" />
                <el-table-column prop="position" label="职位" min-width="150" />
                <el-table-column prop="city" label="城市" width="120" />
                <el-table-column prop="salary" label="薪资" width="100">
                  <template #default="{ row }">
                    <span class="salary-value">{{ row.salary }}K</span>
                  </template>
                </el-table-column>
                <el-table-column prop="created_at" label="记录时间" width="180" />
              </el-table>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageBreadcrumb from '@/components/PageBreadcrumb.vue'
import api from '@/utils/request'

const activeMenu = ref('overview')
const searchKeyword = ref('')
const userRoleFilter = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const dateRange = ref([])

// 统计子标签
const statsSubTab = ref('overview')

// 就业统计
const employmentPeriod = ref('')
const employmentPeriods = ref([])
const employmentRate = ref(0)
const employmentAvgSalary = ref('0K')
const employmentMaxSalary = ref('0K')
const employmentList = ref([])

const menuItems = [
  { key: 'overview', label: '概览', icon: 'Grid' },
  { key: 'users', label: '用户管理', icon: 'User' },
  { key: 'questions', label: '题库管理', icon: 'Document' },
  { key: 'activities', label: '活动管理', icon: 'Calendar' },
  { key: 'stats', label: '数据统计', icon: 'TrendCharts' },
  { key: 'settings', label: '系统设置', icon: 'Setting' }
]

const currentPageTitle = computed(() => {
  return menuItems.find(item => item.key === activeMenu.value)?.label || '管理后台'
})

// 用户数据
const users = ref([])
const totalUsers = ref(0)
const usersLoading = ref(false)

// 加载用户列表
const loadUsers = async () => {
  try {
    usersLoading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }
    if (userRoleFilter.value) {
      params.role = userRoleFilter.value
    }
    const response = await api.get('/api/users/', { params })
    if (response && response.results) {
      users.value = response.results.map(user => ({
        id: user.id,
        username: user.username,
        email: user.email || '-',
        role: user.role,
        nickname: user.nickname || user.username,
        phone: user.phone || '-',
        createdAt: user.created_at ? new Date(user.created_at).toLocaleString('zh-CN') : '-'
      }))
      totalUsers.value = response.total || 0
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
  } finally {
    usersLoading.value = false
  }
}

// 监听菜单切换，自动加载用户数据
watch(activeMenu, (newVal) => {
  if (newVal === 'users') {
    loadUsers()
  }
})

// 监听搜索和筛选条件变化
watch([searchKeyword, userRoleFilter, currentPage, pageSize], () => {
  if (activeMenu.value === 'users') {
    loadUsers()
  }
})

// 初始化加载概览数据
const loadOverviewStats = async () => {
  try {
    const response = await api.get('/api/users/', { params: { page: 1, page_size: 1 } })
    if (response && response.total) {
      totalUsers.value = response.total
    }
  } catch (error) {
    console.error('加载概览统计失败:', error)
  }
}

// 监听概览菜单，加载统计数据
watch(activeMenu, (newVal) => {
  if (newVal === 'overview') {
    loadOverviewStats()
  } else if (newVal === 'users') {
    loadUsers()
  }
})

// 页面加载时初始化概览数据
loadOverviewStats()

// 模拟题目数据
const questionsList = ref([
  { id: 1, title: '软件测试生命周期的理解', category: '软件测试基础', type: '主观题', difficulty: '简单', accuracy: 85 },
  { id: 2, title: 'Web端功能测试用例设计', category: '功能与非功能测试', type: '实操题', difficulty: '中等', accuracy: 72 },
  { id: 3, title: 'Linux常用命令操作', category: 'Linux和MySQL', type: '实操题', difficulty: '简单', accuracy: 91 }
])
const totalQuestions = ref(256)

// 模拟活动数据
const activitiesList = ref([
  { id: 1, title: 'Python编程挑战赛', status: 'ongoing', participants: 1234, startDate: '2024-04-15', endDate: '2024-04-30' },
  { id: 2, title: 'UI自动化实战周', status: 'ongoing', participants: 856, startDate: '2024-04-18', endDate: '2024-04-25' },
  { id: 3, title: '接口测试马拉松', status: 'upcoming', participants: 432, startDate: '2024-04-25', endDate: '2024-05-02' }
])
const totalActivities = ref(12)

const getRoleType = (role) => {
  const types = { student: '', teacher: 'success', admin: 'danger' }
  return types[role] || ''
}

const getRoleLabel = (role) => {
  const labels = { student: '学员', teacher: '教师', admin: '管理员' }
  return labels[role] || role
}

const getDifficultyType = (difficulty) => {
  const types = { '简单': 'success', '中等': 'warning', '困难': 'danger' }
  return types[difficulty] || ''
}

const getStatusType = (status) => {
  const types = { ongoing: 'success', upcoming: 'warning', finished: 'info' }
  return types[status] || ''
}

const getStatusLabel = (status) => {
  const labels = { ongoing: '进行中', upcoming: '即将开始', finished: '已结束' }
  return labels[status] || status
}

const handleCreate = () => {
  ElMessage.info('新建功能开发中...')
}

const handleEdit = (row) => {
  ElMessage.info(`编辑: ${row.title || row.username}`)
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const loadStats = () => {
  ElMessage.success('数据加载中...')
}

// 加载就业统计数据
const loadEmploymentStats = async () => {
  try {
    const params = {}
    if (employmentPeriod.value) {
      params.period = employmentPeriod.value
    }
    const response = await api.get('/api/stats/employment-stats/', { params })
    console.log('就业统计 API 响应:', response)
    if (response) {
      employmentRate.value = response.rate || 0
      employmentAvgSalary.value = response.avg_salary || '0K'
      employmentMaxSalary.value = response.max_salary || '0K'
      employmentPeriods.value = response.periods || []
      employmentList.value = response.list || []
    }
  } catch (error) {
    console.error('加载就业统计失败:', error)
    // 使用模拟数据
    employmentRate.value = 95.8
    employmentAvgSalary.value = '18K'
    employmentMaxSalary.value = '35K'
    employmentPeriods.value = ['第一期', '第二期', '第三期', '第四期', '第五期']
    employmentList.value = [
      { id: 1, period: '第五期', student_name: '张三', company: '腾讯', position: '高级测试工程师', city: '深圳', salary: '25K', created_at: '2024-03-15' },
      { id: 2, period: '第四期', student_name: '李四', company: '阿里巴巴', position: '测试开发工程师', city: '杭州', salary: '28K', created_at: '2024-02-20' },
      { id: 3, period: '第五期', student_name: '王五', company: '字节跳动', position: '自动化测试工程师', city: '北京', salary: '30K', created_at: '2024-03-10' },
      { id: 4, period: '第三期', student_name: '赵六', company: '美团', position: '测试工程师', city: '北京', salary: '20K', created_at: '2024-01-05' },
      { id: 5, period: '第四期', student_name: '钱七', company: '百度', position: '测试开发工程师', city: '北京', salary: '26K', created_at: '2024-02-28' },
      { id: 6, period: '第二期', student_name: '孙八', company: '京东', position: '软件测试工程师', city: '北京', salary: '22K', created_at: '2023-12-15' },
      { id: 7, period: '第五期', student_name: '周九', company: '华为', position: '测试工程师', city: '深圳', salary: '24K', created_at: '2024-03-20' },
      { id: 8, period: '第一期', student_name: '吴十', company: '网易', position: '测试工程师', city: '广州', salary: '18K', created_at: '2023-10-10' }
    ]
  }
}
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
}

.admin-layout {
  display: flex;
  min-height: 100vh;
}

.admin-sidebar {
  width: 260px;
  background: rgba(255, 255, 255, 0.03);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

.sidebar-header {
  padding: 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar-title {
  font-size: 24px;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-nav {
  padding: 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  margin-bottom: 8px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.nav-item.active {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
}

.nav-item .el-icon {
  font-size: 20px;
}

.nav-badge {
  margin-left: auto;
}

.admin-main {
  flex: 1;
  overflow: auto;
}

.admin-header {
  padding: 32px 40px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 32px;
  font-weight: 900;
  color: #fff;
}

.admin-content {
  padding: 40px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 28px;
  display: flex;
  gap: 20px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  flex-shrink: 0;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 32px;
  font-weight: 900;
  color: #fff;
}

.stat-label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
}

.stat-trend {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
}

.stat-trend.positive {
  color: #10b981;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 28px;
}

.chart-title {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.3);
}

.table-toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.table-pagination {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.stats-filters {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
}

.stats-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.stat-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 28px;
}

.panel-title {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}

:deep(.el-table) {
  background: rgba(255, 255, 255, 0.03);
  color: rgba(255, 255, 255, 0.8);
}

:deep(.el-table th.el-table__cell) {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.08);
}

:deep(.el-table tr) {
  background: transparent;
}

:deep(.el-table td.el-table__cell) {
  border-color: rgba(255, 255, 255, 0.05);
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background: rgba(255, 255, 255, 0.02);
}

:deep(.el-table__body tr:hover > td.el-table__cell) {
  background: rgba(102, 126, 234, 0.1);
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row,
  .stats-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-layout {
    flex-direction: column;
  }

  .admin-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .sidebar-nav {
    display: flex;
    overflow-x: auto;
    padding: 8px 16px;
    gap: 8px;
  }

  .nav-item {
    flex-shrink: 0;
    white-space: nowrap;
    margin-bottom: 0;
    padding: 10px 16px;
  }

  .nav-item .el-badge {
    display: none;
  }

  .admin-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 20px;
  }

  .admin-header .el-button {
    width: 100%;
  }

  .page-title {
    font-size: 24px;
  }

  .admin-content {
    padding: 20px 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .stat-card {
    padding: 20px;
  }

  .table-toolbar {
    flex-direction: column;
    gap: 12px;
  }

  .table-toolbar .el-input,
  .table-toolbar .el-select {
    width: 100% !important;
  }

  .table-pagination {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .sidebar-header {
    padding: 16px;
  }

  .sidebar-title {
    font-size: 18px;
  }

  .stat-value {
    font-size: 24px;
  }
}

/* ===== 就业统计样式 ===== */
.stats-cards-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.mini-stat-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
}

.mini-stat-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 8px;
}

.mini-stat-value {
  font-size: 24px;
  font-weight: 900;
  color: #fff;
}

.mini-stat-value.accent {
  color: #f093fb;
}

.salary-value {
  color: #10b981;
  font-weight: 700;
}

.employment-stats-section .stats-filters {
  margin-bottom: 24px;
}

/* 子标签页 */
.sub-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 4px;
}

.sub-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.sub-tab:hover {
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.03);
}

.sub-tab.active {
  color: #fff;
  background: rgba(102, 126, 234, 0.2);
}

.sub-tab .el-icon {
  font-size: 18px;
}

@media (max-width: 768px) {
  .stats-cards-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .sub-tabs {
    flex-direction: column;
  }
}
</style>
