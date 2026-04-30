<template>
  <view class="activities-container">
    <!-- 筛选栏 -->
    <view class="filter-bar">
      <view
        v-for="filter in filters"
        :key="filter.value"
        class="filter-item"
        :class="{ active: currentFilter === filter.value }"
        @click="handleFilterChange(filter.value)"
      >
        <text>{{ filter.label }}</text>
      </view>
    </view>

    <!-- 活动列表 -->
    <scroll-view scroll-y class="activity-list">
      <view
        v-for="activity in activityList"
        :key="activity.id"
        class="activity-card"
        @click="goToDetail(activity.id)"
      >
        <image
          v-if="activity.cover"
          :src="activity.cover"
          class="activity-cover"
          mode="aspectFill"
        ></image>

        <view class="activity-content">
          <view class="activity-header">
            <text class="activity-title">{{ activity.title }}</text>
            <view class="status-badge" :style="{ background: getStatusColor(activity.status) }">
              {{ getStatusText(activity.status) }}
            </view>
          </view>

          <text class="activity-desc">{{ activity.description }}</text>

          <view class="activity-meta">
            <view class="meta-item">
              <text class="meta-icon">📅</text>
              <text class="meta-text">{{ activity.start_time }}</text>
            </view>
            <view class="meta-item">
              <text class="meta-icon">📍</text>
              <text class="meta-text">{{ activity.location }}</text>
            </view>
            <view class="meta-item">
              <text class="meta-icon">👥</text>
              <text class="meta-text">{{ activity.participants }}人</text>
            </view>
          </view>
        </view>
      </view>

      <view v-if="loading" class="loading">
        <text>加载中...</text>
      </view>

      <view v-if="!loading && activityList.length === 0" class="empty">
        <text class="empty-icon">🎯</text>
        <text class="empty-text">暂无活动</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentFilter = ref('all')
const activityList = ref([])
const loading = ref(false)

const filters = [
  { label: '全部', value: 'all' },
  { label: '即将开始', value: 'upcoming' },
  { label: '进行中', value: 'ongoing' },
  { label: '已结束', value: 'finished' }
]

onMounted(() => {
  loadActivities()
})

const loadActivities = () => {
  loading.value = true
  
  activityList.value = [
    {
      id: 1,
      title: '软件测试技能大赛',
      description: '测试你的软件测试技能，赢取丰厚奖品',
      cover: '/static/images/banner1.svg',
      status: 'ongoing',
      start_time: '2026-05-01 09:00',
      location: '线上',
      participants: 128
    },
    {
      id: 2,
      title: '自动化测试工作坊',
      description: '学习Selenium、Appium等自动化测试工具',
      cover: '/static/images/banner2.svg',
      status: 'upcoming',
      start_time: '2026-05-20 14:00',
      location: '北京',
      participants: 45
    },
    {
      id: 3,
      title: '性能测试实战',
      description: 'JMeter性能测试实战演练',
      cover: '/static/images/banner3.svg',
      status: 'finished',
      start_time: '2026-04-10 10:00',
      location: '上海',
      participants: 89
    }
  ]
  
  loading.value = false
}

const handleFilterChange = (value) => {
  currentFilter.value = value
  loadActivities()
}

const getStatusColor = (status) => {
  const colors = {
    upcoming: '#E6A23C',
    ongoing: '#67C23A',
    finished: '#909399'
  }
  return colors[status] || '#909399'
}

const getStatusText = (status) => {
  const texts = {
    upcoming: '即将开始',
    ongoing: '进行中',
    finished: '已结束'
  }
  return texts[status] || '未知'
}

const goToDetail = (activityId) => {
  uni.showToast({
    title: '活动详情开发中',
    icon: 'none'
  })
}
</script>

<style scoped>
.activities-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.filter-bar {
  display: flex;
  gap: 16rpx;
  padding: 24rpx 32rpx;
  background: #ffffff;
  border-bottom: 1rpx solid #eeeeee;
}

.filter-item {
  padding: 12rpx 32rpx;
  font-size: 26rpx;
  color: #666666;
  background: #f5f7fa;
  border-radius: 24rpx;
}

.filter-item.active {
  background: #667eea;
  color: #ffffff;
  font-weight: bold;
}

.activity-list {
  height: calc(100vh - 120rpx);
  padding: 24rpx 32rpx;
}

.activity-card {
  background: #ffffff;
  border-radius: 12rpx;
  margin-bottom: 24rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.activity-cover {
  width: 100%;
  height: 360rpx;
}

.activity-content {
  padding: 32rpx;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16rpx;
}

.activity-title {
  flex: 1;
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
  margin-right: 16rpx;
}

.status-badge {
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
  color: #ffffff;
}

.activity-desc {
  font-size: 26rpx;
  color: #666666;
  line-height: 1.6;
  margin-bottom: 24rpx;
}

.activity-meta {
  display: flex;
  gap: 32rpx;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.meta-icon {
  font-size: 24rpx;
}

.meta-text {
  font-size: 24rpx;
  color: #999999;
}

.loading {
  text-align: center;
  padding: 32rpx;
  font-size: 24rpx;
  color: #999999;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 120rpx 0;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 32rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999999;
}
</style>
