<template>
  <view class="questions-container">
    <!-- 筛选栏 -->
    <view class="filter-bar">
      <picker
        mode="selector"
        :range="stageOptions"
        range-key="label"
        :value="filterForm.stageIndex"
        @change="handleStageChange"
      >
        <view class="filter-item">
          <text>{{ stageOptions[filterForm.stageIndex].label }}</text>
          <text class="arrow">▼</text>
        </view>
      </picker>

      <picker
        mode="selector"
        :range="difficultyOptions"
        range-key="label"
        :value="filterForm.difficultyIndex"
        @change="handleDifficultyChange"
      >
        <view class="filter-item">
          <text>{{ difficultyOptions[filterForm.difficultyIndex].label }}</text>
          <text class="arrow">▼</text>
        </view>
      </picker>
    </view>

    <!-- 题目列表 -->
    <scroll-view
      scroll-y
      class="question-list"
      @scrolltolower="loadMore"
      lower-threshold="100"
    >
      <view
        v-for="question in questionList"
        :key="question.id"
        class="question-card"
        @click="goToDetail(question.id)"
      >
        <view class="question-header">
          <text class="question-title">{{ question.content }}</text>
          <view
            class="difficulty-tag"
            :style="{ background: getDifficultyColor(question.difficulty) }"
          >
            {{ getDifficultyText(question.difficulty) }}
          </view>
        </view>

        <view class="question-meta">
          <text class="meta-item">{{ question.category_name }}</text>
          <text class="meta-item">{{ question.stage_name }}</text>
        </view>

        <view class="question-footer">
          <text class="answer-count">{{ question.answer_count || 0 }}人已答</text>
          <text class="accuracy">正确率 {{ question.accuracy || 0 }}%</text>
        </view>
      </view>

      <!-- 加载更多 -->
      <view v-if="loading" class="loading">
        <text>加载中...</text>
      </view>

      <view v-if="!hasMore && questionList.length > 0" class="no-more">
        <text>没有更多了</text>
      </view>

      <!-- 空状态 -->
      <view v-if="!loading && questionList.length === 0" class="empty">
        <text class="empty-icon">📚</text>
        <text class="empty-text">暂无题目</text>
      </view>
    </scroll-view>

    <!-- 随机练习按钮 -->
    <view class="random-btn" @click="handleRandomPractice">
      <text>🎲 随机练习</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuestionStore } from '@/store/question'
import { getStageName, getDifficultyLabel } from '@/utils/index'

const questionStore = useQuestionStore()

// 筛选表单
const filterForm = ref({
  stageIndex: 0,
  difficultyIndex: 0
})

// 阶段选项
const stageOptions = ref([
  { label: '全部阶段', value: '' },
  { label: '第一阶段', value: 1 },
  { label: '第二阶段', value: 2 },
  { label: '第三阶段', value: 3 },
  { label: '第四阶段', value: 4 },
  { label: '第五阶段', value: 5 },
  { label: '第六阶段', value: 6 },
  { label: '第七阶段', value: 7 },
  { label: '第八阶段', value: 8 },
  { label: '第九阶段', value: 9 },
  { label: '第十阶段', value: 10 }
])

// 难度选项
const difficultyOptions = ref([
  { label: '全部难度', value: '' },
  { label: '简单', value: 'easy' },
  { label: '中等', value: 'medium' },
  { label: '困难', value: 'hard' }
])

const questionList = ref([])
const loading = ref(false)
const hasMore = ref(true)

onMounted(() => {
  loadQuestions()
})

// 加载题目列表
const loadQuestions = async () => {
  try {
    loading.value = true

    const params = {
      page: 1
    }

    // 添加筛选条件
    const stage = stageOptions.value[filterForm.value.stageIndex].value
    const difficulty = difficultyOptions.value[filterForm.value.difficultyIndex].value

    if (stage) params.stage = stage
    if (difficulty) params.difficulty = difficulty

    const res = await questionStore.fetchQuestionList(params)
    questionList.value = res.results || []
    hasMore.value = questionStore.hasMore
  } catch (error) {
    console.error('Load questions error:', error)
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
    const stage = stageOptions.value[filterForm.value.stageIndex].value
    const difficulty = difficultyOptions.value[filterForm.value.difficultyIndex].value

    if (stage) params.stage = stage
    if (difficulty) params.difficulty = difficulty

    await questionStore.loadMore(params)
    questionList.value = questionStore.questionList
    hasMore.value = questionStore.hasMore
  } catch (error) {
    console.error('Load more error:', error)
  } finally {
    loading.value = false
  }
}

// 阶段变化
const handleStageChange = (e) => {
  filterForm.value.stageIndex = e.detail.value
  loadQuestions()
}

// 难度变化
const handleDifficultyChange = (e) => {
  filterForm.value.difficultyIndex = e.detail.value
  loadQuestions()
}

// 获取难度颜色
const getDifficultyColor = (difficulty) => {
  const label = getDifficultyLabel(difficulty)
  return label.color
}

// 获取难度文本
const getDifficultyText = (difficulty) => {
  const label = getDifficultyLabel(difficulty)
  return label.text
}

// 跳转到题目详情
const goToDetail = (questionId) => {
  uni.navigateTo({
    url: `/pages/question-detail/question-detail?id=${questionId}`
  })
}

// 随机练习
const handleRandomPractice = async () => {
  try {
    const params = { count: 1 }

    const stage = stageOptions.value[filterForm.value.stageIndex].value
    if (stage) params.stage = stage

    const res = await questionStore.fetchRandomQuestions(params)

    if (res && res.length > 0) {
      goToDetail(res[0].id)
    } else {
      uni.showToast({
        title: '暂无题目',
        icon: 'none'
      })
    }
  } catch (error) {
    console.error('Random practice error:', error)
  }
}
</script>

<style scoped>
.questions-container {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 120rpx;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16rpx 24rpx;
  background: #f5f7fa;
  border-radius: 8rpx;
  font-size: 26rpx;
  color: #333333;
}

.arrow {
  font-size: 20rpx;
  color: #999999;
}

.question-list {
  height: calc(100vh - 200rpx);
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

.difficulty-tag {
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
  color: #ffffff;
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
  font-size: 24rpx;
  color: #666666;
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

.random-btn {
  position: fixed;
  bottom: 40rpx;
  right: 40rpx;
  width: 160rpx;
  height: 160rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 28rpx;
  font-weight: bold;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.4);
}
</style>
