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
    <scroll-view scroll-y class="question-list">
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
          <text class="meta-tag">{{ question.category }}</text>
          <text class="meta-stage">第{{ question.stage }}阶段</text>
        </view>
      </view>

      <view v-if="loading" class="loading">
        <text>加载中...</text>
      </view>

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

const filterForm = ref({
  stageIndex: 0,
  difficultyIndex: 0
})

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

const difficultyOptions = ref([
  { label: '全部难度', value: '' },
  { label: '简单', value: 'easy' },
  { label: '中等', value: 'medium' },
  { label: '困难', value: 'hard' }
])

const questionList = ref([])
const loading = ref(false)

onMounted(() => {
  loadQuestions()
})

const loadQuestions = () => {
  loading.value = true

  questionList.value = [
    {
      id: 1,
      content: '什么是软件测试？',
      difficulty: 'easy',
      stage: 1,
      category: '基础知识'
    },
    {
      id: 2,
      content: 'Selenium如何定位元素？',
      difficulty: 'medium',
      stage: 4,
      category: 'UI自动化'
    },
    {
      id: 3,
      content: 'JMeter如何进行性能测试？',
      difficulty: 'hard',
      stage: 7,
      category: '性能测试'
    },
    {
      id: 4,
      content: 'Python中如何使用unittest框架？',
      difficulty: 'medium',
      stage: 5,
      category: '自动化测试'
    },
    {
      id: 5,
      content: 'MySQL数据库如何进行索引优化？',
      difficulty: 'hard',
      stage: 8,
      category: '数据库测试'
    },
    {
      id: 6,
      content: '什么是黑盒测试和白盒测试？',
      difficulty: 'easy',
      stage: 1,
      category: '基础知识'
    },
    {
      id: 7,
      content: 'Postman如何进行接口测试？',
      difficulty: 'medium',
      stage: 6,
      category: '接口测试'
    },
    {
      id: 8,
      content: 'Docker容器化部署的优势是什么？',
      difficulty: 'hard',
      stage: 9,
      category: '项目实战'
    }
  ]

  loading.value = false
}

const handleStageChange = (e) => {
  filterForm.value.stageIndex = e.detail.value
  loadQuestions()
}

const handleDifficultyChange = (e) => {
  filterForm.value.difficultyIndex = e.detail.value
  loadQuestions()
}

const getDifficultyColor = (difficulty) => {
  const colors = {
    easy: '#67C23A',
    medium: '#E6A23C',
    hard: '#F56C6C'
  }
  return colors[difficulty] || '#909399'
}

const getDifficultyText = (difficulty) => {
  const texts = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return texts[difficulty] || '未知'
}

const goToDetail = (questionId) => {
  uni.showToast({
    title: '题目详情开发中',
    icon: 'none'
  })
}

const handleRandomPractice = () => {
  uni.showToast({
    title: '随机练习开发中',
    icon: 'none'
  })
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
  gap: 16rpx;
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
  height: calc(100vh - 240rpx);
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
  margin-bottom: 16rpx;
}

.question-title {
  flex: 1;
  font-size: 30rpx;
  font-weight: 500;
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
}

.meta-tag,
.meta-stage {
  padding: 6rpx 16rpx;
  background: #f5f7fa;
  border-radius: 6rpx;
  font-size: 24rpx;
  color: #666666;
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

.random-btn {
  position: fixed;
  bottom: 120rpx;
  right: 32rpx;
  padding: 24rpx 48rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 48rpx;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.4);
  font-size: 28rpx;
  font-weight: bold;
  color: #ffffff;
}
</style>
