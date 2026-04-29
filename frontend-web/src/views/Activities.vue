<template>
  <div class="activities-container">
    <PageBreadcrumb current-name="学习活动" />

    <div class="activities-header">
      <div class="header-content">
        <h1 class="page-title">学习活动</h1>
        <p class="page-subtitle">实战项目 · 技能提升 · 赢取奖励</p>
      </div>
      <el-button type="primary" size="large">
        <el-icon><Plus /></el-icon>
        创建活动
      </el-button>
    </div>

    <div class="filter-bar">
      <el-tabs v-model="activeTab" class="activity-tabs">
        <el-tab-pane label="全部活动" name="all" />
        <el-tab-pane label="进行中" name="ongoing" />
        <el-tab-pane label="即将开始" name="upcoming" />
        <el-tab-pane label="已结束" name="finished" />
      </el-tabs>
    </div>

    <div class="activities-grid">
      <div
        v-for="activity in filteredActivities"
        :key="activity.id"
        class="activity-card"
        :class="activity.status"
      >
        <div class="activity-banner" :style="{ background: activity.bannerGradient }">
          <div class="activity-badge" :class="activity.status">
            {{ activity.statusText }}
          </div>
          <div class="activity-icon">
            <el-icon><component :is="activity.icon" /></el-icon>
          </div>
        </div>

        <div class="activity-content">
          <h3 class="activity-title">{{ activity.title }}</h3>
          <p class="activity-desc">{{ activity.description }}</p>

          <div class="activity-meta">
            <div class="meta-item">
              <el-icon><Calendar /></el-icon>
              <span>{{ formatDate(activity.startDate) }} - {{ formatDate(activity.endDate) }}</span>
            </div>
            <div class="meta-item">
              <el-icon><User /></el-icon>
              <span>{{ activity.participants }}人参与</span>
            </div>
          </div>

          <div class="activity-progress" v-if="activity.progress !== undefined">
            <div class="progress-info">
              <span class="progress-label">完成进度</span>
              <span class="progress-value">{{ activity.progress }}%</span>
            </div>
            <el-progress
              :percentage="activity.progress"
              :color="activity.progressColor"
              :stroke-width="8"
            />
          </div>

          <div class="activity-rewards">
            <div class="reward-item" v-for="reward in activity.rewards" :key="reward.type">
              <el-icon><component :is="reward.icon" /></el-icon>
              <span>{{ reward.value }}</span>
            </div>
          </div>

          <el-button
            :type="activity.status === 'ongoing' ? 'primary' : 'default'"
            size="large"
            class="activity-btn"
            @click="handleActivityAction(activity)"
          >
            {{ activity.buttonText }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useActivityStore } from '@/stores/activity'
import { formatDate } from '@/utils/datetime'
import PageBreadcrumb from '@/components/PageBreadcrumb.vue'

const activityStore = useActivityStore()
const activeTab = ref('all')

const activities = ref([
  {
    id: 1,
    title: 'Python编程挑战赛',
    description: '完成50道Python编程题，掌握Python核心语法和数据处理能力',
    status: 'ongoing',
    statusText: '进行中',
    startDate: '2026-04-15',
    endDate: '2026-04-30',
    participants: 1234,
    progress: 68,
    progressColor: '#667eea',
    bannerGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    icon: 'TrendCharts',
    rewards: [
      { type: 'points', icon: 'Star', value: '+500积分' },
      { type: 'badge', icon: 'Medal', value: 'Python达人' }
    ],
    buttonText: '继续挑战'
  },
  {
    id: 2,
    title: 'UI自动化实战周',
    description: '连续7天完成Selenium自动化测试实战，养成自动化测试习惯',
    status: 'ongoing',
    statusText: '进行中',
    startDate: '2026-04-18',
    endDate: '2026-04-25',
    participants: 856,
    progress: 42,
    progressColor: '#f093fb',
    bannerGradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    icon: 'View',
    rewards: [
      { type: 'points', icon: 'Star', value: '+300积分' },
      { type: 'streak', icon: 'Calendar', value: '连续打卡' }
    ],
    buttonText: '立即打卡'
  },
  {
    id: 3,
    title: '接口测试马拉松',
    description: '参与接口测试实战，掌握Postman和接口自动化测试技能',
    status: 'upcoming',
    statusText: '即将开始',
    startDate: '2026-04-25',
    endDate: '2026-05-02',
    participants: 432,
    bannerGradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    icon: 'Link',
    rewards: [
      { type: 'points', icon: 'Star', value: '+400积分' },
      { type: 'certificate', icon: 'Document', value: '接口测试证书' }
    ],
    buttonText: '预约参加'
  },
  {
    id: 4,
    title: '金融项目实战',
    description: '完成金融项目的完整测试流程，从需求分析到测试报告',
    status: 'finished',
    statusText: '已结束',
    startDate: '2026-04-01',
    endDate: '2026-04-14',
    participants: 2341,
    progress: 100,
    progressColor: '#10b981',
    bannerGradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    icon: 'Briefcase',
    rewards: [
      { type: 'points', icon: 'Star', value: '+600积分' },
      { type: 'badge', icon: 'Trophy', value: '项目实战之星' }
    ],
    buttonText: '查看成绩'
  }
])

const filteredActivities = computed(() => {
  if (activeTab.value === 'all') return activities.value
  return activities.value.filter(a => a.status === activeTab.value)
})

// 页面加载时获取活动列表
onMounted(async () => {
  try {
    // 尝试从API获取活动列表
    // await activityStore.fetchActivities()
    // 如果API返回数据，使用API数据替换本地数据
    // activities.value = activityStore.activities
  } catch (error) {
    // API调用失败时使用本地模拟数据
    console.log('使用本地模拟数据')
  }
})

const handleActivityAction = (activity) => {
  console.log('活动操作:', activity)

  switch (activity.status) {
    case 'ongoing':
      // 进行中的活动
      if (activity.buttonText === '继续挑战') {
        handleContinueChallenge(activity)
      } else if (activity.buttonText === '立即打卡') {
        handleCheckIn(activity)
      }
      break
    case 'upcoming':
      // 即将开始的活动
      handleReserve(activity)
      break
    case 'finished':
      // 已结束的活动
      handleViewScore(activity)
      break
    default:
      ElMessage.info('未知的活动状态')
  }
}

// 继续挑战
const handleContinueChallenge = (activity) => {
  ElMessage.success(`正在进入 ${activity.title}...`)
  // TODO: 跳转到挑战页面
  setTimeout(() => {
    ElMessage.info('挑战功能开发中，敬请期待！')
  }, 500)
}

// 立即打卡
const handleCheckIn = (activity) => {
  ElMessageBox.confirm(
    `确认完成今日打卡？`,
    '打卡确认',
    {
      confirmButtonText: '确认打卡',
      cancelButtonText: '取消',
      type: 'success'
    }
  ).then(() => {
    // 更新进度
    const activityIndex = activities.value.findIndex(a => a.id === activity.id)
    if (activityIndex !== -1) {
      activities.value[activityIndex].progress = Math.min(100, activities.value[activityIndex].progress + 14)
      ElMessage.success('打卡成功！连续打卡中...')
    }
  }).catch(() => {
    ElMessage.info('已取消打卡')
  })
}

// 预约参加
const handleReserve = (activity) => {
  ElMessageBox.confirm(
    `确认预约参加 ${activity.title}？活动将在 ${formatDate(activity.startDate)} 开始。`,
    '预约确认',
    {
      confirmButtonText: '确认预约',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    ElMessage.success('预约成功！我们会在活动开始前提醒您')
    // TODO: 调用预约API
  }).catch(() => {
    ElMessage.info('已取消预约')
  })
}

// 查看成绩
const handleViewScore = (activity) => {
  ElMessageBox.alert(
    `<div style="text-align: center; padding: 20px;">
      <h3 style="margin-bottom: 20px; color: #667eea;">${activity.title}</h3>
      <div style="margin-bottom: 15px;">
        <span style="font-size: 48px; font-weight: bold; color: #10b981;">95</span>
        <span style="font-size: 24px; color: #666;">分</span>
      </div>
      <div style="color: #666; margin-bottom: 10px;">完成进度: ${activity.progress}%</div>
      <div style="color: #666; margin-bottom: 10px;">排名: 前 15%</div>
      <div style="color: #666;">获得奖励: ${activity.rewards.map(r => r.value).join(', ')}</div>
    </div>`,
    '活动成绩',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '确定',
      center: true
    }
  )
}
</script>

<style scoped>
.activities-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
  padding: 40px;
}

.activities-header {
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
  margin-bottom: 8px;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.5);
  font-size: 16px;
  letter-spacing: 1px;
}

.filter-bar {
  max-width: 1400px;
  margin: 0 auto 32px;
}

.activity-tabs :deep(.el-tabs__nav-wrap) {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 8px;
}

.activity-tabs :deep(.el-tabs__item) {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 10px;
}

.activity-tabs :deep(.el-tabs__item.is-active) {
  color: #fff;
  background: rgba(102, 126, 234, 0.2);
}

.activity-tabs :deep(.el-tabs__active-bar) {
  display: none;
}

.activities-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 28px;
}

.activity-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s;
}

.activity-card:hover {
  transform: translateY(-6px);
  border-color: rgba(102, 126, 234, 0.3);
  box-shadow: 0 16px 48px rgba(102, 126, 234, 0.2);
}

.activity-banner {
  position: relative;
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.activity-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.activity-badge.ongoing {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.activity-badge.upcoming {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.activity-badge.finished {
  background: rgba(107, 114, 128, 0.2);
  color: #9ca3af;
}

.activity-icon {
  font-size: 64px;
  color: rgba(255, 255, 255, 0.9);
}

.activity-content {
  padding: 28px;
}

.activity-title {
  color: #fff;
  font-size: 22px;
  font-weight: 800;
  margin-bottom: 12px;
  line-height: 1.3;
}

.activity-desc {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.activity-meta {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

.meta-item .el-icon {
  font-size: 16px;
}

.activity-progress {
  margin-bottom: 20px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
}

.progress-value {
  color: #667eea;
  font-size: 14px;
  font-weight: 700;
}

.activity-rewards {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
}

.reward-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  font-weight: 600;
}

.reward-item .el-icon {
  font-size: 18px;
  color: #f59e0b;
}

.activity-btn {
  width: 100%;
  height: 48px;
  font-size: 15px;
  font-weight: 700;
  border-radius: 12px;
}

@media (max-width: 1024px) {
  .activities-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .activities-container {
    padding: 20px 16px;
  }

  .activities-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .activities-header .el-button {
    width: 100%;
  }

  .page-title {
    font-size: 32px;
  }

  .activities-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .activity-content {
    padding: 20px;
  }

  .activity-rewards {
    flex-wrap: wrap;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 24px;
  }

  .activity-title {
    font-size: 18px;
  }

  .activity-banner {
    height: 120px;
  }

  .activity-icon {
    font-size: 48px;
  }
}
</style>
