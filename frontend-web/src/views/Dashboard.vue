<template>
  <div class="dashboard-container">
    <!-- 页面标题和导航 -->
    <div class="page-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>数据看板</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :xs="12" :sm="6" v-for="card in statCards" :key="card.title">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-card-inner">
            <div class="stat-icon" :style="{ background: card.color }">
              <el-icon :size="28"><component :is="card.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ card.value }}</div>
              <div class="stat-label">{{ card.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>测试用例优先级分布</template>
          <div ref="pieChartRef" style="height: 320px" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>测试用例状态统计</template>
          <div ref="barChartRef" style="height: 320px" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>用户角色分布</template>
          <div ref="userPieRef" style="height: 320px" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>题库难度分布</template>
          <div ref="questionBarRef" style="height: 320px" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, markRaw } from 'vue'
import { Document, User, Calendar, DataLine } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import request from '@/utils/request'

const pieChartRef = ref(null)
const barChartRef = ref(null)
const userPieRef = ref(null)
const questionBarRef = ref(null)

let charts = []

const statCards = ref([
  { title: '题目总数', value: '-', icon: markRaw(Document), color: 'linear-gradient(135deg, #667eea, #764ba2)' },
  { title: '用户总数', value: '-', icon: markRaw(User), color: 'linear-gradient(135deg, #f093fb, #f5576c)' },
  { title: '活动总数', value: '-', icon: markRaw(Calendar), color: 'linear-gradient(135deg, #4facfe, #00f2fe)' },
  { title: '测试用例数', value: '-', icon: markRaw(DataLine), color: 'linear-gradient(135deg, #43e97b, #38f9d7)' }
])

const loadStats = async () => {
  try {
    // 并行获取所有统计数据
    const [questions, users, activities, testcases, testcaseStats, userRoles] = await Promise.allSettled([
      request({ url: '/api/questions/', method: 'get', params: { limit: 1 } }),
      request({ url: '/api/users/', method: 'get', params: { limit: 1 } }),
      request({ url: '/api/activities/', method: 'get', params: { limit: 1 } }),
      request({ url: '/api/testcases/', method: 'get', params: { limit: 1 } }),
      request({ url: '/api/testcases/', method: 'get', params: { limit: 10000 } }), // 获取所有测试用例用于统计
      request({ url: '/api/stats/user_distribution/', method: 'get' })
    ])

    // 更新统计卡片
    if (questions.status === 'fulfilled') {
      statCards.value[0].value = questions.value.count || 0
    }
    if (users.status === 'fulfilled') {
      statCards.value[1].value = users.value.count || 0
    }
    if (activities.status === 'fulfilled') {
      statCards.value[2].value = activities.value.count || 0
    }
    if (testcases.status === 'fulfilled') {
      statCards.value[3].value = testcases.value.count || 0
    }

    // 更新测试用例图表数据
    if (testcaseStats.status === 'fulfilled' && testcaseStats.value.results) {
      updateTestcaseCharts(testcaseStats.value.results)
    }

    // 更新用户角色分布
    if (userRoles.status === 'fulfilled') {
      updateUserRoleChart(userRoles.value)
    }
  } catch (e) {
    console.error('加载统计数据失败:', e)
  }
}

// 更新测试用例图表
const updateTestcaseCharts = (testcases) => {
  // 统计优先级分布
  const priorityCount = { critical: 0, high: 0, medium: 0, low: 0 }
  const statusCount = { draft: 0, active: 0, deprecated: 0, closed: 0 }

  testcases.forEach(tc => {
    priorityCount[tc.priority] = (priorityCount[tc.priority] || 0) + 1
    statusCount[tc.status] = (statusCount[tc.status] || 0) + 1
  })

  // 更新优先级饼图
  if (charts[0]) {
    charts[0].setOption({
      tooltip: { trigger: 'item' },
      legend: { orient: 'horizontal', bottom: 0 },
      series: [{
        name: '优先级',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '45%'],
        data: [
          { value: priorityCount.critical || 0, name: '紧急', itemStyle: { color: '#f56c6c' } },
          { value: priorityCount.high || 0, name: '高', itemStyle: { color: '#e6a23c' } },
          { value: priorityCount.medium || 0, name: '中', itemStyle: { color: '#409eff' } },
          { value: priorityCount.low || 0, name: '低', itemStyle: { color: '#909399' } }
        ],
        emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } }
      }]
    }, true)
  }

  // 更新状态柱状图
  if (charts[1]) {
    charts[1].setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: ['草稿', '有效', '已废弃', '已关闭'] },
      yAxis: { type: 'value' },
      series: [{
        type: 'bar',
        data: [
          { value: statusCount.draft || 0, itemStyle: { color: '#909399' } },
          { value: statusCount.active || 0, itemStyle: { color: '#67c23a' } },
          { value: statusCount.deprecated || 0, itemStyle: { color: '#e6a23c' } },
          { value: statusCount.closed || 0, itemStyle: { color: '#f56c6c' } }
        ],
        barWidth: '50%'
      }],
      grid: { left: 40, right: 20, bottom: 30, top: 20 }
    }, true)
  }
}

// 更新用户角色分布图表
const updateUserRoleChart = (data) => {
  // 这里暂时使用模拟数据，因为后端API返回的是hometown统计
  // 如果需要真实的角色统计，需要后端提供对应的API
}

const initPieChart = () => {
  const chart = echarts.init(pieChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { orient: 'horizontal', bottom: 0 },
    series: [{
      name: '优先级',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      data: [
        { value: 0, name: '紧急', itemStyle: { color: '#f56c6c' } },
        { value: 0, name: '高', itemStyle: { color: '#e6a23c' } },
        { value: 0, name: '中', itemStyle: { color: '#409eff' } },
        { value: 0, name: '低', itemStyle: { color: '#909399' } }
      ],
      emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } }
    }]
  })
  charts.push(chart)
}

const initBarChart = () => {
  const chart = echarts.init(barChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['草稿', '有效', '已废弃', '已关闭'] },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [
        { value: 0, itemStyle: { color: '#909399' } },
        { value: 0, itemStyle: { color: '#67c23a' } },
        { value: 0, itemStyle: { color: '#e6a23c' } },
        { value: 0, itemStyle: { color: '#f56c6c' } }
      ],
      barWidth: '50%'
    }],
    grid: { left: 40, right: 20, bottom: 30, top: 20 }
  })
  charts.push(chart)
}

const initUserPieChart = () => {
  const chart = echarts.init(userPieRef.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { orient: 'horizontal', bottom: 0 },
    series: [{
      name: '角色分布',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      data: [
        { value: 1200, name: '学员', itemStyle: { color: '#409eff' } },
        { value: 80, name: '教师', itemStyle: { color: '#67c23a' } },
        { value: 15, name: '管理员', itemStyle: { color: '#f56c6c' } }
      ]
    }]
  })
  charts.push(chart)
}

const initQuestionBarChart = () => {
  const chart = echarts.init(questionBarRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['简单', '中等', '困难'] },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [
        { value: 38, itemStyle: { color: '#67c23a' } },
        { value: 8, itemStyle: { color: '#e6a23c' } },
        { value: 5, itemStyle: { color: '#f56c6c' } }
      ],
      barWidth: '50%'
    }],
    grid: { left: 40, right: 20, bottom: 30, top: 20 }
  })
  charts.push(chart)
}

const handleResize = () => {
  charts.forEach(c => c.resize())
}

onMounted(async () => {
  initPieChart()
  initBarChart()
  initUserPieChart()
  initQuestionBarChart()
  await loadStats()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach(c => c.dispose())
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  padding: 16px 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-card-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.charts-row {
  margin-bottom: 20px;
}
</style>
