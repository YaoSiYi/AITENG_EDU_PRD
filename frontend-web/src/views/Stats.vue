<template>
  <div class="stats-container">
    <PageBreadcrumb current-name="学习统计" />

    <div class="stats-header">
      <h1 class="page-title">学习统计</h1>
      <div class="time-range">
        <el-radio-group v-model="timeRange" size="large">
          <el-radio-button value="week">本周</el-radio-button>
          <el-radio-button value="month">本月</el-radio-button>
          <el-radio-button value="year">本年</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card highlight">
        <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
          <el-icon><TrendCharts /></el-icon>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ totalQuestions }}</h3>
          <p class="stat-label">累计答题</p>
          <span class="stat-trend positive">
            <el-icon><CaretTop /></el-icon>
            +12.5%
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
          <el-icon><Check /></el-icon>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ accuracy }}%</h3>
          <p class="stat-label">正确率</p>
          <span class="stat-trend positive">
            <el-icon><CaretTop /></el-icon>
            +3.2%
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ studyTime }}h</h3>
          <p class="stat-label">学习时长</p>
          <span class="stat-trend positive">
            <el-icon><CaretTop /></el-icon>
            +8.7%
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%)">
          <el-icon><Trophy /></el-icon>
        </div>
        <div class="stat-content">
          <h3 class="stat-value">{{ streak }}</h3>
          <p class="stat-label">连续天数</p>
          <span class="stat-trend">保持中</span>
        </div>
      </div>
    </div>

    <div class="charts-section">
      <div class="chart-card large">
        <div class="chart-header">
          <h3 class="chart-title">学习趋势</h3>
          <el-select v-model="chartType" size="small">
            <el-option label="答题数量" value="questions" />
            <el-option label="正确率" value="accuracy" />
            <el-option label="学习时长" value="time" />
          </el-select>
        </div>
        <div class="chart-body" ref="trendChartRef"></div>
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">课程阶段分布</h3>
        </div>
        <div class="chart-body" ref="subjectChartRef"></div>
      </div>
    </div>

    <div class="performance-section">
      <div class="performance-card">
        <h3 class="section-title">薄弱知识点</h3>
        <div class="weakness-list">
          <div v-for="item in weaknesses" :key="item.id" class="weakness-item">
            <div class="weakness-info">
              <span class="weakness-name">{{ item.name }}</span>
              <span class="weakness-category">{{ item.category }}</span>
            </div>
            <div class="weakness-progress">
              <el-progress
                :percentage="item.accuracy"
                :color="getProgressColor(item.accuracy)"
                :stroke-width="8"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="performance-card">
        <h3 class="section-title">最近成就</h3>
        <div class="achievements-list">
          <div v-for="achievement in achievements" :key="achievement.id" class="achievement-item">
            <div class="achievement-icon" :style="{ background: achievement.color }">
              <el-icon><component :is="achievement.icon" /></el-icon>
            </div>
            <div class="achievement-info">
              <h4 class="achievement-name">{{ achievement.name }}</h4>
              <p class="achievement-desc">{{ achievement.description }}</p>
              <span class="achievement-date">{{ achievement.date }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { useStatsStore } from '@/stores/stats'
import PageBreadcrumb from '@/components/PageBreadcrumb.vue'

const statsStore = useStatsStore()

const timeRange = ref('week')
const chartType = ref('questions')
const trendChartRef = ref(null)
const subjectChartRef = ref(null)

const totalQuestions = ref(1248)
const accuracy = ref(85)
const studyTime = ref(42)
const streak = ref(12)

const weaknesses = ref([
  { id: 1, name: 'Selenium元素定位', category: 'UI自动化', accuracy: 62 },
  { id: 2, name: 'Pytest框架使用', category: '接口自动化', accuracy: 68 },
  { id: 3, name: 'JMeter性能调优', category: '性能测试', accuracy: 71 },
  { id: 4, name: 'MySQL复杂查询', category: 'Linux和MySQL', accuracy: 58 }
])

const achievements = ref([
  {
    id: 1,
    name: '连续学习7天',
    description: '坚持就是胜利',
    date: '2天前',
    icon: 'Calendar',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: 2,
    name: '测试达人',
    description: '完成100道测试题',
    date: '5天前',
    icon: 'Medal',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  }
])

const getProgressColor = (percentage) => {
  if (percentage < 60) return '#ef4444'
  if (percentage < 75) return '#f59e0b'
  return '#10b981'
}

onMounted(async () => {
  initTrendChart()
  initSubjectChart()

  // 尝试从API获取统计数据
  try {
    // await statsStore.fetchDashboard()
    // 如果API返回数据，更新本地数据
  } catch (error) {
    console.log('使用本地模拟数据')
  }
})

const initTrendChart = () => {
  if (!trendChartRef.value) return

  const chart = echarts.init(trendChartRef.value)
  const option = {
    grid: { top: 20, right: 20, bottom: 40, left: 50 },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: { color: 'rgba(255,255,255,0.6)' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } },
      axisLabel: { color: 'rgba(255,255,255,0.6)' }
    },
    series: [{
      data: [45, 52, 38, 65, 58, 72, 68],
      type: 'line',
      smooth: true,
      lineStyle: { width: 3, color: '#667eea' },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
          { offset: 1, color: 'rgba(102, 126, 234, 0)' }
        ])
      },
      itemStyle: { color: '#667eea' }
    }]
  }
  chart.setOption(option)
}

const initSubjectChart = () => {
  if (!subjectChartRef.value) return

  const chart = echarts.init(subjectChartRef.value)
  const option = {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#1a1f3a', borderWidth: 2 },
      label: { color: '#fff' },
      data: [
        { value: 335, name: '初级课程', itemStyle: { color: '#667eea' } },
        { value: 456, name: '中级课程', itemStyle: { color: '#f093fb' } },
        { value: 298, name: '高级+进阶', itemStyle: { color: '#4facfe' } }
      ]
    }]
  }
  chart.setOption(option)
}
</script>

<style scoped>
.stats-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
  padding: 40px;
}

.stats-header {
  max-width: 1400px;
  margin: 0 auto 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 48px;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.time-range :deep(.el-radio-button__inner) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
}

.time-range :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: #fff;
}

.stats-grid {
  max-width: 1400px;
  margin: 0 auto 40px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 28px;
  display: flex;
  gap: 20px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(102, 126, 234, 0.3);
}

.stat-card.highlight {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.3);
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

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 36px;
  font-weight: 900;
  color: #fff;
  margin-bottom: 4px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
}

.stat-trend.positive {
  color: #10b981;
}

.charts-section {
  max-width: 1400px;
  margin: 0 auto 40px;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 28px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.chart-title {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
}

.chart-body {
  height: 300px;
}

.performance-section {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.performance-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 28px;
}

.section-title {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 24px;
}

.weakness-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.weakness-item {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.weakness-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.weakness-name {
  color: #fff;
  font-weight: 600;
}

.weakness-category {
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

.achievements-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.achievement-item {
  display: flex;
  gap: 16px;
}

.achievement-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  flex-shrink: 0;
}

.achievement-info {
  flex: 1;
}

.achievement-name {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.achievement-desc {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  margin-bottom: 6px;
}

.achievement-date {
  color: rgba(255, 255, 255, 0.3);
  font-size: 12px;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .performance-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-container {
    padding: 20px 16px;
  }

  .stats-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .page-title {
    font-size: 32px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-card {
    flex-direction: column;
    padding: 20px 16px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 22px;
  }

  .stat-value {
    font-size: 28px;
  }

  .chart-body {
    height: 220px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 24px;
  }

  .time-range :deep(.el-radio-button__inner) {
    padding: 8px 12px;
    font-size: 13px;
  }
}
</style>
