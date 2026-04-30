<template>
  <view class="wrong-book-container">
    <!-- 统计卡片 -->
    <view class="stats-cards">
      <view class="stat-card">
        <text class="stat-value">{{ wrongQuestions.length }}</text>
        <text class="stat-label">错题总数</text>
      </view>
      <view class="stat-card">
        <text class="stat-value">{{ masteredCount }}</text>
        <text class="stat-label">已掌握</text>
      </view>
      <view class="stat-card">
        <text class="stat-value">{{ unmasteredCount }}</text>
        <text class="stat-label">待复习</text>
      </view>
    </view>

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

    <!-- 错题列表 -->
    <scroll-view scroll-y class="question-list">
      <view
        v-for="item in filteredQuestions"
        :key="item.id"
        class="question-card"
        @click="goToDetail(item.question.id)"
      >
        <view class="question-header">
          <text class="question-title">{{ item.question.content }}</text>
          <view
            v-if="item.is_mastered"
            class="mastered-badge"
          >
            ✓ 已掌握
          </view>
        </view>

        <view class="question-meta">
          <text class="meta-item">{{ item.question.category_name }}</text>
          <text class="meta-item">错误 {{ item.wrong_count }} 次</text>
        </view>

        <view class="question-footer">
          <text class="add-time">{{ formatDate(item.created_at) }}</text>
          <view class="actions">
            <text
              v-if="!item.is_mastered"
              class="action-btn primary"
              @click.stop="handleMarkMastered(item.id)"
            >
              标记掌握
            </text>
            <text
              class="action-btn danger"
              @click.stop="handleRemove(item.id)"
            >
              移除
            </text>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view v-if="filteredQuestions.length === 0" class="empty">
        <text class="empty-icon">📝</text>
        <text class="empty-text">{{ emptyText }}</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuestionStore } from '@/store/question'
import { formatDate } from '@/utils/index'

const questionStore = useQuestionStore()

const wrongQuestions = ref([])
const currentFilter = ref('all')

const filters = [
  { label: '全部', value: 'all' },
  { label: '待复习', value: 'unmastered' },
  { label: '已掌握', value: 'mastered' }
]

// 已掌握数量
const masteredCount = computed(() => {
  return wrongQuestions.value.filter(item => item.is_mastered).length
})

// 待复习数量
const unmasteredCount = computed(() => {
  return wrongQuestions.value.filter(item => !item.is_mastered).length
})

// 过滤后的题目
const filteredQuestions = computed(() => {
  if (currentFilter.value === 'all') {
    return wrongQuestions.value
  } else if (currentFilter.value === 'mastered') {
    return wrongQuestions.value.filter(item => item.is_mastered)
  } else {
    return wrongQuestions.value.filter(item => !item.is_mastered)
  }
})

// 空状态文本
const emptyText = computed(() => {
  if (currentFilter.value === 'mastered') {
    return '暂无已掌握的题目'
  } else if (currentFilter.value === 'unmastered') {
    return '暂无待复习的题目'
  } else {
    return '错题本为空，快去刷题吧！'
  }
})

onMounted(() => {
  loadWrongQuestions()
})

// 加载错题本
const loadWrongQuestions = async () => {
  try {
    const res = await questionStore.fetchWrongQuestions()
    wrongQuestions.value = res.results || res
  } catch (error) {
    console.error('Load wrong questions error:', error)
  }
}

// 筛选变化
const handleFilterChange = (value) => {
  currentFilter.value = value
}

// 标记已掌握
const handleMarkMastered = async (id) => {
  try {
    await questionStore.markMastered(id)

    // 更新本地数据
    const item = wrongQuestions.value.find(q => q.id === id)
    if (item) {
      item.is_mastered = true
    }
  } catch (error) {
    console.error('Mark mastered error:', error)
  }
}

// 移除
const handleRemove = async (id) => {
  uni.showModal({
    title: '确认移除',
    content: '确定要从错题本中移除这道题吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await questionStore.removeFromWrong(id)

          // 更新本地数据
          wrongQuestions.value = wrongQuestions.value.filter(item => item.id !== id)
        } catch (error) {
          console.error('Remove error:', error)
        }
      }
    }
  })
}

// 跳转到题目详情
const goToDetail = (questionId) => {
  uni.navigateTo({
    url: `/pages/question-detail/question-detail?id=${questionId}`
  })
}
</script>

<style scoped>
.wrong-book-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.stats-cards {
  display: flex;
  gap: 24rpx;
  padding: 32rpx;
  background: #ffffff;
  margin-bottom: 20rpx;
}

.stat-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32rpx 16rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12rpx;
  color: #ffffff;
}

.stat-value {
  font-size: 48rpx;
  font-weight: bold;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
}

.filter-bar {
  display: flex;
  gap: 24rpx;
  padding: 24rpx 32rpx;
  background: #ffffff;
  border-bottom: 1rpx solid #eeeeee;
}

.filter-item {
  flex: 1;
  text-align: center;
  padding: 16rpx 0;
  font-size: 28rpx;
  color: #666666;
  border-radius: 8rpx;
  transition: all 0.3s;
}

.filter-item.active {
  background: #667eea;
  color: #ffffff;
  font-weight: bold;
}

.question-list {
  height: calc(100vh - 400rpx);
  padding: 24rpx 32rpx;
}

.question-card {
  background: #ffffff;
  border-radius: 12rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24rpx;
}

.question-title {
  flex: 1;
  font-size: 30rpx;
  font-weight: bold;
  color: #333333;
  line-height: 1.6;
  margin-right: 16rpx;
}

.mastered-badge {
  padding: 8rpx 16rpx;
  background: #67c23a;
  color: #ffffff;
  font-size: 22rpx;
  border-radius: 8rpx;
  white-space: nowrap;
}

.question-meta {
  display: flex;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.meta-item {
  font-size: 24rpx;
  color: #999999;
}

.question-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-time {
  font-size: 24rpx;
  color: #999999;
}

.actions {
  display: flex;
  gap: 16rpx;
}

.action-btn {
  padding: 8rpx 20rpx;
  font-size: 24rpx;
  border-radius: 8rpx;
}

.action-btn.primary {
  background: #667eea;
  color: #ffffff;
}

.action-btn.danger {
  background: #f56c6c;
  color: #ffffff;
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
