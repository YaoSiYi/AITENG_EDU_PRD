<template>
  <div class="wrong-book-container">
    <PageBreadcrumb current-name="我的错题本" />

    <div class="wrong-book-header">
      <div class="header-content">
        <h1 class="page-title">我的错题本</h1>
        <p class="page-subtitle">温故知新 · 查漏补缺 · 技能提升</p>
      </div>
      <div class="header-actions">
        <el-select v-model="selectedSubject" placeholder="选择课程" size="large">
          <el-option label="全部课程" value="all" />
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
        <el-button type="primary" size="large" @click="startReview">
          <el-icon><Refresh /></el-icon>
          开始复习
        </el-button>
      </div>
    </div>

    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%)">
          <el-icon><Warning /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ totalWrong }}</span>
          <span class="stat-label">错题总数</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%)">
          <el-icon><Check /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ mastered }}</span>
          <span class="stat-label">已掌握</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%)">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ reviewing }}</span>
          <span class="stat-label">复习中</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
          <el-icon><TrendCharts /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ masteryRate }}%</span>
          <span class="stat-label">掌握率</span>
        </div>
      </div>
    </div>

    <div class="wrong-questions-list">
      <div
        v-for="question in filteredQuestions"
        :key="question.id"
        class="wrong-question-card"
      >
        <div class="question-header">
          <div class="question-tags">
            <span class="tag subject" :style="{ background: question.subjectColor }">
              {{ question.subject }}
            </span>
            <span class="tag difficulty" :style="{ color: question.difficultyColor }">
              {{ question.difficulty }}
            </span>
            <span class="tag status" :class="question.status">
              {{ question.statusText }}
            </span>
          </div>
          <div class="question-actions">
            <el-button size="small" text @click="reviewQuestion(question)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button size="small" text @click="markAsMastered(question)">
              <el-icon><Check /></el-icon>
              已掌握
            </el-button>
            <el-button size="small" text type="danger" @click="deleteQuestion(question)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </div>

        <div class="question-content">
          <h3 class="question-title">{{ question.title }}</h3>
          <div class="question-body">
            <p class="question-text">{{ question.question }}</p>
          </div>

          <div class="answer-section">
            <div class="answer-item wrong">
              <span class="answer-label">你的答案</span>
              <span class="answer-value">{{ question.yourAnswer }}</span>
            </div>
            <div class="answer-item correct">
              <span class="answer-label">正确答案</span>
              <span class="answer-value">{{ question.correctAnswer }}</span>
            </div>
          </div>

          <div class="explanation-section" v-if="question.explanation">
            <h4 class="explanation-title">
              <el-icon><Document /></el-icon>
              解析
            </h4>
            <p class="explanation-text">{{ question.explanation }}</p>
          </div>

          <div class="question-meta">
            <div class="meta-item">
              <el-icon><Calendar /></el-icon>
              <span>错误时间：{{ question.wrongDate }}</span>
            </div>
            <div class="meta-item">
              <el-icon><Refresh /></el-icon>
              <span>复习次数：{{ question.reviewCount }}次</span>
            </div>
            <div class="meta-item" v-if="question.lastReviewDate">
              <el-icon><Clock /></el-icon>
              <span>上次复习：{{ question.lastReviewDate }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useQuestionStore } from '@/stores/question'
import PageBreadcrumb from '@/components/PageBreadcrumb.vue'

const questionStore = useQuestionStore()

const selectedSubject = ref('all')
const totalWrong = ref(48)
const mastered = ref(32)
const reviewing = ref(16)
const masteryRate = ref(67)

const wrongQuestions = ref([
  {
    id: 1,
    title: '软件测试生命周期理解',
    subject: '软件测试基础',
    subjectColor: '#667eea',
    difficulty: '中等',
    difficultyColor: '#f59e0b',
    status: 'reviewing',
    statusText: '复习中',
    question: '请描述软件测试生命周期（STLC）的各个阶段及其主要活动',
    yourAnswer: '需求分析、测试设计、测试执行、缺陷跟踪',
    correctAnswer: '需求分析、测试计划、测试设计、测试环境搭建、测试执行、缺陷跟踪、测试报告、测试总结',
    explanation: '软件测试生命周期包含8个完整阶段，每个阶段都有明确的输入输出和交付物。需求分析是起点，测试总结是终点，形成完整的闭环。',
    wrongDate: '2024-04-15',
    reviewCount: 2,
    lastReviewDate: '2024-04-18'
  },
  {
    id: 2,
    title: 'Selenium元素定位方法',
    subject: 'UI自动化',
    subjectColor: '#10b981',
    difficulty: '困难',
    difficultyColor: '#ef4444',
    status: 'new',
    statusText: '待复习',
    question: '使用Selenium定位动态生成的元素，id和class都会变化，应该使用什么定位方法？',
    yourAnswer: '使用xpath定位',
    correctAnswer: '使用xpath的相对定位或CSS选择器的属性定位，结合contains()、starts-with()等函数定位部分属性值',
    explanation: '对于动态元素，应该找到元素的稳定属性（如data-*属性、文本内容、相对位置等），使用xpath的高级函数或CSS选择器的属性选择器进行定位。',
    wrongDate: '2024-04-20',
    reviewCount: 0,
    lastReviewDate: null
  },
  {
    id: 3,
    title: 'Postman接口测试断言',
    subject: '接口测试',
    subjectColor: '#f59e0b',
    difficulty: '简单',
    difficultyColor: '#10b981',
    status: 'mastered',
    statusText: '已掌握',
    question: '在Postman中如何断言响应状态码为200且响应时间小于500ms？',
    yourAnswer: 'pm.test("Status code is 200", function () { pm.response.to.have.status(200); });',
    correctAnswer: 'pm.test("Status code is 200", function () { pm.response.to.have.status(200); });\npm.test("Response time is less than 500ms", function () { pm.expect(pm.response.responseTime).to.be.below(500); });',
    explanation: '需要编写两个独立的test断言，分别验证状态码和响应时间。使用pm.response.responseTime获取响应时间，使用to.be.below()方法进行数值比较。',
    wrongDate: '2024-04-10',
    reviewCount: 3,
    lastReviewDate: '2024-04-19'
  },
  {
    id: 4,
    title: 'JMeter性能测试指标分析',
    subject: '性能测试',
    subjectColor: '#ef4444',
    difficulty: '困难',
    difficultyColor: '#ef4444',
    status: 'reviewing',
    statusText: '复习中',
    question: '在JMeter测试报告中，TPS为100，平均响应时间为2000ms，并发用户数应该设置为多少？',
    yourAnswer: '100个并发用户',
    correctAnswer: '200个并发用户。根据Little定律：并发用户数 = TPS × 平均响应时间 = 100 × 2 = 200',
    explanation: 'Little定律（L = λ × W）是性能测试的基础公式，其中L是系统中的平均用户数（并发数），λ是到达率（TPS），W是平均响应时间（秒）。',
    wrongDate: '2024-04-16',
    reviewCount: 1,
    lastReviewDate: '2024-04-18'
  },
  {
    id: 5,
    title: 'MySQL索引优化',
    subject: 'Linux和MySQL',
    subjectColor: '#4facfe',
    difficulty: '中等',
    difficultyColor: '#f59e0b',
    status: 'reviewing',
    statusText: '复习中',
    question: '对于WHERE条件中包含多个字段的查询，如何创建联合索引才能达到最优效果？',
    yourAnswer: '按照字段在WHERE中出现的顺序创建索引',
    correctAnswer: '按照字段的区分度从高到低创建索引，遵循最左前缀原则。区分度高的字段放在前面，等值查询的字段优先于范围查询的字段',
    explanation: '联合索引的创建需要考虑：1) 字段的区分度（选择性）；2) 最左前缀原则；3) 查询类型（等值 vs 范围）；4) 排序和分组需求。',
    wrongDate: '2024-04-17',
    reviewCount: 2,
    lastReviewDate: '2024-04-20'
  }
])

const filteredQuestions = computed(() => {
  if (selectedSubject.value === 'all') return wrongQuestions.value
  return wrongQuestions.value.filter(q => {
    const subjectMap = {
      'stage1': '软件测试基础',
      'stage2': '功能与非功能测试',
      'stage3': 'Linux和MySQL',
      'stage4': 'Python课程',
      'stage5': 'UI自动化',
      'stage6': '接口测试',
      'stage7': '性能测试',
      'stage8': '接口自动化',
      'stage9': '项目实战',
      'stage10': 'AI大模型与Agent'
    }
    return q.subject === subjectMap[selectedSubject.value]
  })
})

// 页面加载时获取错题本
onMounted(async () => {
  try {
    // 尝试从API获取错题本
    // await questionStore.fetchWrongQuestions()
    // 如果API返回数据，使用API数据替换本地数据
    // wrongQuestions.value = questionStore.wrongQuestions
  } catch (error) {
    // API调用失败时使用本地模拟数据
    console.log('使用本地模拟数据')
  }
})

const startReview = () => {
  ElMessage.success('开始复习模式')
}

const reviewQuestion = (question) => {
  console.log('查看题目:', question)
}

const markAsMastered = async (question) => {
  try {
    // 调用API标记为已掌握
    await questionStore.markQuestionCorrect(question.id)
    question.status = 'mastered'
    question.statusText = '已掌握'
    ElMessage.success('已标记为掌握')
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

const deleteQuestion = (question) => {
  ElMessage.success('已删除错题')
}
</script>

<style scoped>
.wrong-book-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
  padding: 40px;
}

.wrong-book-header {
  max-width: 1400px;
  margin: 0 auto 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 48px;
  font-weight: 900;
  background: linear-gradient(135deg, #ef4444 0%, #f093fb 100%);
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

.header-actions {
  display: flex;
  gap: 16px;
}

.stats-overview {
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
  align-items: center;
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
  font-size: 36px;
  font-weight: 900;
  color: #fff;
}

.stat-label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
}

.wrong-questions-list {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.wrong-question-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s;
}

.wrong-question-card:hover {
  border-color: rgba(239, 68, 68, 0.3);
  box-shadow: 0 8px 32px rgba(239, 68, 68, 0.15);
}

.question-header {
  padding: 24px 28px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-tags {
  display: flex;
  gap: 12px;
}

.tag {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tag.subject {
  color: #fff;
}

.tag.difficulty {
  background: rgba(255, 255, 255, 0.05);
}

.tag.status {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.6);
}

.tag.status.new {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.tag.status.reviewing {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.tag.status.mastered {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.question-actions {
  display: flex;
  gap: 8px;
}

.question-content {
  padding: 28px;
}

.question-title {
  color: #fff;
  font-size: 22px;
  font-weight: 800;
  margin-bottom: 20px;
}

.question-body {
  margin-bottom: 24px;
}

.question-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
  line-height: 1.8;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border-left: 4px solid #667eea;
  border-radius: 8px;
}

.answer-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.answer-item {
  padding: 20px;
  border-radius: 12px;
  border: 2px solid;
}

.answer-item.wrong {
  background: rgba(239, 68, 68, 0.05);
  border-color: rgba(239, 68, 68, 0.3);
}

.answer-item.correct {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.3);
}

.answer-label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.answer-item.wrong .answer-label {
  color: #ef4444;
}

.answer-item.correct .answer-label {
  color: #10b981;
}

.answer-value {
  display: block;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.explanation-section {
  padding: 24px;
  background: rgba(102, 126, 234, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  margin-bottom: 24px;
}

.explanation-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 12px;
}

.explanation-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 15px;
  line-height: 1.8;
}

.question-meta {
  display: flex;
  gap: 32px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
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

@media (max-width: 1024px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .wrong-book-container {
    padding: 20px 16px;
  }

  .wrong-book-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
  }

  .header-actions .el-select,
  .header-actions .el-button {
    width: 100%;
  }

  .page-title {
    font-size: 32px;
  }

  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-card {
    padding: 16px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 22px;
  }

  .stat-value {
    font-size: 28px;
  }

  .question-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }

  .question-content {
    padding: 16px;
  }

  .answer-section {
    grid-template-columns: 1fr;
  }

  .question-meta {
    flex-wrap: wrap;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .stats-overview {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 24px;
  }

  .question-title {
    font-size: 17px;
  }
}
</style>
