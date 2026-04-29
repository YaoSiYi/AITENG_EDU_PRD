<template>
  <view class="home-container">
    <!-- 顶部Banner -->
    <view class="banner-section">
      <swiper class="banner-swiper" indicator-dots circular autoplay>
        <swiper-item v-for="(banner, index) in banners" :key="index">
          <image :src="banner.image" mode="aspectFill" class="banner-image"></image>
        </swiper-item>
      </swiper>
    </view>

    <!-- 快捷入口 -->
    <view class="quick-entry">
      <view class="entry-item" @click="goToQuestions">
        <text class="entry-icon">📚</text>
        <text class="entry-text">题库练习</text>
      </view>
      <view class="entry-item" @click="goToWrongBook">
        <text class="entry-icon">📝</text>
        <text class="entry-text">错题本</text>
      </view>
      <view class="entry-item" @click="goToActivities">
        <text class="entry-icon">🎯</text>
        <text class="entry-text">活动中心</text>
      </view>
      <view class="entry-item" @click="goToProfile">
        <text class="entry-icon">👤</text>
        <text class="entry-text">个人中心</text>
      </view>
    </view>

    <!-- 课程体系 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">课程体系</text>
        <text class="section-more">查看全部 ></text>
      </view>
      <view class="course-grid">
        <view
          v-for="stage in courseStages"
          :key="stage.id"
          class="course-card"
          @click="goToCourse(stage.id)"
        >
          <view class="course-badge" :style="{ background: stage.color }">
            {{ stage.level }}
          </view>
          <text class="course-name">{{ stage.name }}</text>
          <text class="course-desc">{{ stage.desc }}</text>
        </view>
      </view>
    </view>

    <!-- 统计数据 -->
    <view class="stats-section">
      <view class="stat-item">
        <text class="stat-value">{{ stats.questionCount }}</text>
        <text class="stat-label">题目总数</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ stats.studentCount }}</text>
        <text class="stat-label">学员人数</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ stats.activityCount }}</text>
        <text class="stat-label">活动数量</text>
      </view>
    </view>

    <!-- 优秀学员 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">优秀学员</text>
      </view>
      <scroll-view scroll-x class="student-scroll">
        <view
          v-for="student in excellentStudents"
          :key="student.id"
          class="student-card"
        >
          <image :src="student.avatar" class="student-avatar"></image>
          <text class="student-name">{{ student.name }}</text>
          <text class="student-company">{{ student.company }}</text>
          <text class="student-salary">{{ student.salary }}</text>
        </view>
      </scroll-view>
    </view>

    <!-- 高频面试题 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">高频面试题</text>
      </view>
      <view class="question-list">
        <view
          v-for="question in frequentQuestions"
          :key="question.id"
          class="question-item"
          @click="goToQuestion(question.id)"
        >
          <text class="question-title">{{ question.title }}</text>
          <text class="question-tag">{{ question.category }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

// 轮播图数据
const banners = ref([
  { image: '/static/images/banner1.jpg' },
  { image: '/static/images/banner2.jpg' },
  { image: '/static/images/banner3.jpg' }
])

// 课程阶段
const courseStages = ref([
  { id: 1, level: '初级', name: '软件测试基础', desc: '第1-3阶段', color: '#67C23A' },
  { id: 2, level: '中级', name: 'Python与自动化', desc: '第4-7阶段', color: '#E6A23C' },
  { id: 3, level: '高级', name: '项目实战', desc: '第8-10阶段', color: '#F56C6C' }
])

// 统计数据
const stats = ref({
  questionCount: 0,
  studentCount: 0,
  activityCount: 0
})

// 优秀学员
const excellentStudents = ref([])

// 高频面试题
const frequentQuestions = ref([])

onMounted(() => {
  loadHomeData()
})

// 加载首页数据
const loadHomeData = async () => {
  try {
    // TODO: 调用API获取首页数据
    // const res = await getHomeStats()
    // stats.value = res

    // 模拟数据
    stats.value = {
      questionCount: 1200,
      studentCount: 5000,
      activityCount: 50
    }

    excellentStudents.value = [
      {
        id: 1,
        avatar: '/static/images/avatar1.jpg',
        name: '张三',
        company: '阿里巴巴',
        salary: '25K'
      },
      {
        id: 2,
        avatar: '/static/images/avatar2.jpg',
        name: '李四',
        company: '腾讯',
        salary: '23K'
      }
    ]

    frequentQuestions.value = [
      { id: 1, title: '什么是软件测试？', category: '基础知识' },
      { id: 2, title: 'Selenium如何定位元素？', category: 'UI自动化' },
      { id: 3, title: 'JMeter如何进行性能测试？', category: '性能测试' }
    ]
  } catch (error) {
    console.error('Load home data error:', error)
  }
}

// 跳转到题库
const goToQuestions = () => {
  uni.switchTab({
    url: '/pages/questions/questions'
  })
}

// 跳转到错题本
const goToWrongBook = () => {
  uni.navigateTo({
    url: '/pages/wrong-book/wrong-book'
  })
}

// 跳转到活动
const goToActivities = () => {
  uni.switchTab({
    url: '/pages/activities/activities'
  })
}

// 跳转到个人中心
const goToProfile = () => {
  uni.switchTab({
    url: '/pages/profile/profile'
  })
}

// 跳转到课程
const goToCourse = (stageId) => {
  uni.navigateTo({
    url: `/pages/questions/questions?stage=${stageId}`
  })
}

// 跳转到题目详情
const goToQuestion = (questionId) => {
  uni.navigateTo({
    url: `/pages/question-detail/question-detail?id=${questionId}`
  })
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.banner-section {
  width: 100%;
  height: 400rpx;
}

.banner-swiper {
  width: 100%;
  height: 100%;
}

.banner-image {
  width: 100%;
  height: 100%;
}

.quick-entry {
  display: flex;
  justify-content: space-around;
  padding: 40rpx 32rpx;
  background: #ffffff;
  margin-bottom: 20rpx;
}

.entry-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.entry-icon {
  font-size: 64rpx;
  margin-bottom: 16rpx;
}

.entry-text {
  font-size: 24rpx;
  color: #666666;
}

.section {
  background: #ffffff;
  padding: 32rpx;
  margin-bottom: 20rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
}

.section-more {
  font-size: 24rpx;
  color: #999999;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24rpx;
}

.course-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32rpx 16rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
}

.course-badge {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 24rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
}

.course-name {
  font-size: 26rpx;
  font-weight: bold;
  color: #333333;
  margin-bottom: 8rpx;
}

.course-desc {
  font-size: 22rpx;
  color: #999999;
}

.stats-section {
  display: flex;
  justify-content: space-around;
  padding: 40rpx 32rpx;
  background: #ffffff;
  margin-bottom: 20rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 48rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999999;
}

.student-scroll {
  white-space: nowrap;
}

.student-card {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  width: 200rpx;
  margin-right: 24rpx;
  padding: 24rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
}

.student-avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  margin-bottom: 16rpx;
}

.student-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333333;
  margin-bottom: 8rpx;
}

.student-company {
  font-size: 24rpx;
  color: #666666;
  margin-bottom: 8rpx;
}

.student-salary {
  font-size: 26rpx;
  font-weight: bold;
  color: #f56c6c;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
}

.question-title {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
}

.question-tag {
  font-size: 22rpx;
  color: #667eea;
  padding: 8rpx 16rpx;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8rpx;
}
</style>
