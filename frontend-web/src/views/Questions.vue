<template>
  <div class="questions-container">
    <PageBreadcrumb current-name="智能题库" />

    <div class="questions-header">
      <div class="header-content">
        <h1 class="page-title">智能题库</h1>
        <p class="page-subtitle">从数据库加载真实题目数据</p>
      </div>
      <div class="header-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索题目..."
          prefix-icon="Search"
          size="large"
          class="search-input"
        />
        <el-button type="primary" size="large" @click="loadQuestions">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <div v-loading="loading" class="questions-content">
      <div class="sidebar">
        <div class="category-card">
          <h3 class="category-title">学科分类</h3>
          <div class="category-list">
            <div
              v-for="category in displayCategories"
              :key="category.id"
              :class="['category-item', { active: selectedCategory === category.id }]"
              @click="selectCategory(category.id)"
            >
              <span>{{ category.name }}</span>
              <span class="count">{{ getCategoryCount(category.id) }}</span>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <h3 class="stats-title">题库统计</h3>
          <div class="stat-item">
            <span class="stat-label">题目总数</span>
            <span class="stat-value">{{ totalQuestions }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">分类数量</span>
            <span class="stat-value">{{ apiCategories.length }}</span>
          </div>
        </div>
      </div>

      <div class="main-content">
        <div class="difficulty-tabs">
          <div
            v-for="level in difficultyLevels"
            :key="level.value"
            :class="['difficulty-tab', { active: selectedDifficulty === level.value }]"
            @click="selectedDifficulty = level.value"
          >
            <span class="difficulty-dot" :style="{ background: level.color }"></span>
            {{ level.label }}
          </div>
        </div>

        <div v-if="filteredQuestions.length === 0" class="empty-state">
          <el-empty description="暂无题目数据">
            <el-button type="primary" @click="loadQuestions">重新加载</el-button>
          </el-empty>
        </div>

        <div v-else>
          <div class="questions-grid">
            <div
              v-for="question in paginatedQuestions"
              :key="question.id"
              class="question-card"
              @click="openQuestion(question)"
            >
              <div class="question-header">
                <span class="question-type" :style="{ background: getDifficultyColor(question.difficulty) }">
                  {{ question.subject }}
                </span>
                <span class="question-difficulty" :style="{ color: getDifficultyColor(question.difficulty) }">
                  {{ getDifficultyLabel(question.difficulty) }}
                </span>
              </div>
              <h3 class="question-title">{{ question.content.substring(0, 50) }}{{ question.content.length > 50 ? '...' : '' }}</h3>
              <p class="question-preview">{{ question.answer.substring(0, 100) }}{{ question.answer.length > 100 ? '...' : '' }}</p>
              <div class="question-footer">
                <div class="question-meta">
                  <el-icon><Document /></el-icon>
                  <span>{{ question.subject }}</span>
                </div>
                <div class="question-meta">
                  <el-icon><Calendar /></el-icon>
                  <span>阶段{{ question.stage }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="pagination-container">
            <span class="pagination-total">共 {{ filteredQuestions.length }} 条</span>
            <el-select
              v-model="pageSize"
              class="page-size-select"
              @change="handleSizeChange"
            >
              <el-option :value="10" label="10 条/页" />
              <el-option :value="20" label="20 条/页" />
              <el-option :value="30" label="30 条/页" />
              <el-option :value="50" label="50 条/页" />
              <el-option :value="9999" label="全部" />
            </el-select>
            <el-pagination
              v-if="pageSize < 9999"
              v-model:current-page="currentPage"
              :page-size="pageSize"
              :total="filteredQuestions.length"
              layout="prev, pager, next, jumper"
              background
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </div>
    </div>

    <QuestionDetail
      v-model="showQuestionDetail"
      :question="currentQuestion"
      @next="handleNext"
      @addToWrong="handleAddToWrong"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import QuestionDetail from '@/components/QuestionDetail.vue'
import PageBreadcrumb from '@/components/PageBreadcrumb.vue'
import { useQuestionStore } from '@/stores/question'

const questionStore = useQuestionStore()

const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedDifficulty = ref('all')
const showQuestionDetail = ref(false)
const currentQuestion = ref(null)
const loading = ref(false)
const apiQuestions = ref([])
const apiCategories = ref([])
const currentPage = ref(1)
const pageSize = ref(10)

const difficultyLevels = [
  { value: 'all', label: '全部难度', color: '#667eea' },
  { value: 'easy', label: '简单', color: '#10b981' },
  { value: 'medium', label: '中等', color: '#f59e0b' },
  { value: 'hard', label: '困难', color: '#ef4444' }
]

// 难度排序权重
const difficultyOrder = {
  easy: 1,
  medium: 2,
  hard: 3
}

const displayCategories = computed(() => {
  const allCategory = { id: 'all', name: '全部分类', count: apiQuestions.value.length }
  return [allCategory, ...apiCategories.value]
})

const totalQuestions = computed(() => apiQuestions.value.length)

const filteredQuestions = computed(() => {
  const filtered = apiQuestions.value.filter(q => {
    const matchCategory = selectedCategory.value === 'all' || q.category === selectedCategory.value
    const matchDifficulty = selectedDifficulty.value === 'all' || q.difficulty === selectedDifficulty.value
    const matchSearch = !searchQuery.value ||
      q.content.includes(searchQuery.value) ||
      q.subject.includes(searchQuery.value) ||
      q.answer.includes(searchQuery.value)
    return matchCategory && matchDifficulty && matchSearch
  })

  // 按难度排序：简单 -> 中等 -> 困难
  return filtered.sort((a, b) => {
    const orderA = difficultyOrder[a.difficulty] || 999
    const orderB = difficultyOrder[b.difficulty] || 999
    return orderA - orderB
  })
})

// 分页后的题目列表
const paginatedQuestions = computed(() => {
  // 如果选择"全部"，直接返回所有筛选后的题目
  if (pageSize.value >= 9999) {
    return filteredQuestions.value
  }

  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredQuestions.value.slice(start, end)
})

const getDifficultyColor = (difficulty) => {
  const colors = {
    easy: '#10b981',
    medium: '#f59e0b',
    hard: '#ef4444'
  }
  return colors[difficulty] || '#667eea'
}

const getDifficultyLabel = (difficulty) => {
  const labels = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return labels[difficulty] || difficulty
}

const getCategoryCount = (categoryId) => {
  if (categoryId === 'all') {
    return apiQuestions.value.length
  }
  return apiQuestions.value.filter(q => q.category === categoryId).length
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  currentPage.value = 1 // 切换分类时重置到第一页
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1 // 改变每页条数时重置到第一页
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  // 滚动到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const loadQuestions = async () => {
  loading.value = true
  try {
    // 获取所有题目（使用大的 page_size 确保获取所有数据）
    const questionsData = await questionStore.fetchQuestions({ page_size: 1000 })
    apiQuestions.value = questionsData.results || questionsData || []

    // 从题目数据中提取分类信息
    const categoryMap = new Map()
    apiQuestions.value.forEach(q => {
      if (q.category && q.category_name) {
        if (!categoryMap.has(q.category)) {
          categoryMap.set(q.category, {
            id: q.category,
            name: q.category_name,
            count: 0
          })
        }
        categoryMap.get(q.category).count++
      }
    })
    apiCategories.value = Array.from(categoryMap.values())

    ElMessage.success(`成功加载 ${apiQuestions.value.length} 个题目`)
  } catch (error) {
    console.error('加载题目失败:', error)
    ElMessage.error('加载题目失败，请检查后端服务是否正常运行')
  } finally {
    loading.value = false
  }
}

const openQuestion = (question) => {
  currentQuestion.value = {
    ...question,
    title: question.content.substring(0, 50),
    preview: question.content,
    type: question.subject,
    typeColor: getDifficultyColor(question.difficulty),
    difficultyColor: getDifficultyColor(question.difficulty),
    time: 10,
    attempts: 0,
    accuracy: 0,
    options: null,
    correctAnswer: question.answer,
    correctAnswerText: question.answer,
    explanation: question.explanation || '暂无解析',
    keyPoints: [question.subject]
  }
  showQuestionDetail.value = true
}

const handleNext = () => {
  const currentIndex = filteredQuestions.value.findIndex(q => q.id === currentQuestion.value.id)
  if (currentIndex < filteredQuestions.value.length - 1) {
    openQuestion(filteredQuestions.value[currentIndex + 1])
  } else {
    ElMessage.info('已经是最后一题了')
    showQuestionDetail.value = false
  }
}

const handleAddToWrong = async (question) => {
  try {
    await questionStore.addWrongQuestion(question.id)
    ElMessage.success('已加入错题本')
  } catch (error) {
    ElMessage.error('添加失败，请重试')
  }
}

// 切换难度或搜索时重置到第一页
watch([selectedDifficulty, searchQuery], () => {
  currentPage.value = 1
})

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.questions-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
  padding: 40px;
}

.questions-header {
  max-width: 1400px;
  margin: 0 auto 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
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

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-input {
  width: 320px;
}

.search-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.search-input :deep(.el-input__inner) {
  color: #fff;
}

.questions-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.category-card,
.stats-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
}

.category-title,
.stats-title {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s;
}

.category-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.category-item.active {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
  font-weight: 600;
}

.category-item .count {
  margin-left: auto;
  font-size: 13px;
  opacity: 0.6;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
}

.stat-value {
  color: #667eea;
  font-size: 20px;
  font-weight: 700;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.difficulty-tabs {
  display: flex;
  gap: 12px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  width: fit-content;
}

.difficulty-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.difficulty-tab:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.difficulty-tab.active {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.difficulty-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 40px 0 20px;
  flex-wrap: wrap;
}

.pagination-total {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.page-size-select {
  width: 120px;
}

.page-size-select :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.page-size-select :deep(.el-input__inner) {
  color: #fff;
}

.pagination-container :deep(.el-pagination) {
  gap: 8px;
}

.pagination-container :deep(.el-pagination.is-background .el-pager li) {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-container :deep(.el-pagination.is-background .el-pager li:not(.is-disabled):hover) {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.pagination-container :deep(.el-pagination.is-background .el-pager li.is-active) {
  background: #667eea;
  color: #fff;
  border-color: #667eea;
}

.pagination-container :deep(.el-pagination button) {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-container :deep(.el-pagination button:not(:disabled):hover) {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.pagination-container :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-container :deep(.el-input__inner) {
  background: transparent;
  color: #fff;
}


.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.question-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.question-card:hover {
  transform: translateY(-4px);
  border-color: rgba(102, 126, 234, 0.3);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.question-type {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
}

.question-difficulty {
  font-size: 13px;
  font-weight: 600;
}

.question-title {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
  line-height: 1.4;
}

.question-preview {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.question-footer {
  display: flex;
  gap: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

.question-meta .el-icon {
  font-size: 16px;
}

@media (max-width: 1024px) {
  .questions-content {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }

  .questions-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
  }

  .search-input {
    width: 100% !important;
  }
}

@media (max-width: 768px) {
  .questions-container {
    padding: 20px 16px;
  }

  .page-title {
    font-size: 32px;
  }

  .questions-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .difficulty-tabs {
    width: 100%;
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 4px;
  }

  .difficulty-tab {
    white-space: nowrap;
    flex-shrink: 0;
  }

  .question-footer {
    flex-wrap: wrap;
    gap: 12px;
  }
}
</style>
