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
    <scroll-view
      scroll-y
      class="activity-list"
      @scrolltolower="loadMore"
      lower-threshold="100"
    >
      <view
        v-for="activity in activityList"
        :key="activity.id"
        class="activity-card"
        @click="goToDetail(activity.id)"
      >
        <!-- 活动封面 -->
        <image
          v-if="activity.cover"
          :src="activity.cover"
          class="activity-cover"
          mode="aspectFill"
        ></image>

        <view class="activity-content">
          <!-- 活动标题 -->
          <view class="activity-header">
            <text class="activity-title">{{ activity.title }}</text>
            <view
              class="status-badge"
              :style="{ background: getStatusColor(activity.status) }"
            >
              {{ getStatusText(activity.status) }}
            </view>
          </view>

          <!-- 活动描述 -->
          <text class="activity-desc">{{ activity.description }}</text>

          <!-- 活动信息 -->
          <view class="activity-meta">
            <view class="meta-item">
              <text class="meta-icon">📅</text>
              <text class="meta-text">{{ formatDate(activity.start_time) }}</text>
            </view>
            <view class="meta-item">
              <text class="meta-icon">👥</text>
              <text class="meta-text">{{ activity.participant_count }}人参与</text>
            </view>
          </view>

          <!-- 操作按钮 -->
          <view class="activity-footer">
            <button
              v-if="!activity.is_joined && activity.status === 'upcoming'"
              class="btn-join"
              @click.stop="handleJoin(activity.id)"
            >
              立即报名
            </button>
            <button
              v-else-if="activity.is_joined && activity.status === 'upcoming'"
              class="btn-cancel"
              @click.stop="handleCancel(activity.id)"
            >
              取消报名
            </button>
            <button
              v-else-if="activity.is_joined && activity.status === 'ongoing'"
              class="btn-checkin"
              @click.stop="handleCheckIn(activity.id)"
            >
              立即签到
            </button>
            <button
              v-else
              class="btn-view"
              @click.stop="goToDetail(activity.id)"
            >
              查看详情
            </button>
          </view>
        </view>
      </view>

      <!-- 加载更多 -->
      <view v-if="loading" class="loading">
        <text>加载中...</text>
      </view>

      <view v-if="!hasMore && activityList.length > 0" class="no-more">
        <text>没有更多了</text>
      </view>

      <!-- 空状态 -->
      <view v-if="!loading && activityList.length === 0" class="empty">
        <text class="empty-icon">🎯</text>
        <text class="empty-text">暂无活动</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useActivityStore } from '@/store/activity'
import { formatDate } from '@/utils/index'

const activityStore = useActivityStore()

const currentFilter = ref('all')
const activityList = ref([])
const loading = ref(false)
const hasMore = ref(true)

const filters = [
  { label: '全部', value: 'all' },
  { label: '即将开始', value: 'upcoming' },
  { label: '进行中', value: 'ongoing' },
  { label: '已结束', value: 'finished' }
]

onMounted(() => {
  loadActivities()
})

// 加载活动列表
const loadActivities = async () => {
  try {
    loading.value = true

    const params = { page: 1 }
    if (currentFilter.value !== 'all') {
      params.status = currentFilter.value
    }

    const res = await activityStore.fetchActivityList(params)
    activityList.value = res.results || []
    hasMore.value = activityStore.hasMore
  } catch (error) {
    console.error('Load activities error:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多
const loadMore = async () => {
  if (!hasMore.value || loading.value) return

  try {
    loading.value = true

    const params = {}
    if (currentFilter.value !== 'all') {
      params.status = currentFilter.value
    }

    await activityStore.loadMore(params)
    activityList.value = activityStore.activityList
    hasMore.value = activityStore.hasMore
  } catch (error) {
    console.error('Load more error:', error)
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = (value) => {
  currentFilter.value = value
  loadActivities()
}

// 获取状态颜色
const getStatusColor = (status) => {
  const colors = {
    upcoming: '#E6A23C',
    ongoing: '#67C23A',
    finished: '#909399'
  }
  return colors[status] || '#909399'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    upcoming: '即将开始',
    ongoing: '进行中',
    finished: '已结束'
  }
  return texts[status] || '未知'
}

// 报名活动
const handleJoin = async (activityId) => {
  try {
    await activityStore.join(activityId)
    loadActivities()
  } catch (error) {
    console.error('Join activity error:', error)
  }
}

// 取消报名
const handleCancel = async (activityId) => {
  uni.showModal({
    title: '确认取消',
    content: '确定要取消报名吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await activityStore.cancel(activityId)
          loadActivities()
        } catch (error) {
          console.error('Cancel activity error:', error)
        }
      }
    }
  })
}

// 签到
const handleCheckIn = async (activityId) => {
  try {
    await activityStore.checkIn(activityId)
  } catch (error) {
    console.error('Check in error:', error)
  }
}

// 跳转到详情
const goToDetail = (activityId) => {
  uni.navigateTo({
    url: `/pages/activity-detail/activity-detail?id=${activityId}`
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
  overflow-x: auto;
  white-space: nowrap;
}

.filter-item {
  padding: 12rpx 32rpx;
  font-size: 26rpx;
  color: #666666;
  background: #f5f7fa;
  border-radius: 24rpx;
  transition: all 0.3s;
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
  line-height: 1.5;
  margin-right: 16rpx;
}

.status-badge {
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
  color: #ffffff;
  white-space: nowrap;
}

.activity-desc {
  font-size: 26rpx;
  color: #666666;
  line-height: 1.6;
  margin-bottom: 24rpx;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.activity-meta {
  display: flex;
  gap: 32rpx;
  margin-bottom: 24rpx;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.meta-icon {
  font-size: 28rpx;
}

.meta-text {
  font-size: 24rpx;
  color: #999999;
}

.activity-footer {
  display: flex;
  justify-content: flex-end;
}

.activity-footer button {
  padding: 16rpx 48rpx;
  font-size: 26rpx;
  border-radius: 8rpx;
  border: none;
}

.btn-join {
  background: #667eea;
  color: #ffffff;
}

.btn-cancel {
  background: #f56c6c;
  color: #ffffff;
}

.btn-checkin {
  background: #67c23a;
  color: #ffffff;
}

.btn-view {
  background: #909399;
  color: #ffffff;
}

.loading,
.no-more {
  text-align: center;
  padding: 32rpx;
  font-size: 24rpx;
  color: #999999;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
