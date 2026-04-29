<template>
  <el-dialog
    v-model="visible"
    :title="question?.title"
    width="900px"
    :close-on-click-modal="false"
    class="question-dialog"
  >
    <div v-if="question" class="question-detail">
      <div class="question-header">
        <div class="question-tags">
          <span class="tag subject" :style="{ background: question.subjectColor }">
            {{ question.subject }}
          </span>
          <span class="tag difficulty" :style="{ color: question.difficultyColor }">
            {{ question.difficulty }}
          </span>
          <span class="tag type">{{ question.type }}</span>
        </div>
        <div class="question-meta">
          <el-icon><Clock /></el-icon>
          <span>{{ question.time }}分钟</span>
          <el-icon><User /></el-icon>
          <span>{{ question.attempts }}人已做</span>
        </div>
      </div>

      <div class="question-content">
        <h3 class="content-title">题目内容</h3>
        <div class="content-text" v-html="question.content"></div>

        <div v-if="question.options && question.options.length" class="question-options">
          <div
            v-for="(option, index) in question.options"
            :key="index"
            :class="['option-item', {
              selected: selectedAnswer === option.key,
              correct: showAnswer && option.key === question.correctAnswer,
              wrong: showAnswer && selectedAnswer === option.key && option.key !== question.correctAnswer
            }]"
            @click="!showAnswer && selectAnswer(option.key)"
          >
            <div class="option-key">{{ option.key }}</div>
            <div class="option-text">{{ option.text }}</div>
            <el-icon v-if="showAnswer && option.key === question.correctAnswer" class="check-icon">
              <Check />
            </el-icon>
            <el-icon v-if="showAnswer && selectedAnswer === option.key && option.key !== question.correctAnswer" class="close-icon">
              <Close />
            </el-icon>
          </div>
        </div>

        <div v-else class="answer-input">
          <el-input
            v-model="textAnswer"
            type="textarea"
            :rows="6"
            placeholder="请输入你的答案..."
            :disabled="showAnswer"
          />
        </div>
      </div>

      <div v-if="showAnswer" class="answer-section">
        <div class="correct-answer">
          <h4 class="section-title">
            <el-icon><Check /></el-icon>
            正确答案
          </h4>
          <div class="answer-content">{{ question.correctAnswerText }}</div>
        </div>

        <div v-if="question.explanation" class="explanation">
          <h4 class="section-title">
            <el-icon><Document /></el-icon>
            答案解析
          </h4>
          <div class="explanation-content" v-html="question.explanation"></div>
        </div>

        <div v-if="question.keyPoints && question.keyPoints.length" class="key-points">
          <h4 class="section-title">
            <el-icon><Star /></el-icon>
            知识点
          </h4>
          <div class="points-list">
            <span v-for="(point, index) in question.keyPoints" :key="index" class="point-tag">
              {{ point }}
            </span>
          </div>
        </div>
      </div>

      <div v-if="!showAnswer && isAnswered" class="result-section">
        <div :class="['result-card', isCorrect ? 'correct' : 'wrong']">
          <el-icon class="result-icon">
            <component :is="isCorrect ? 'CircleCheck' : 'CircleClose'" />
          </el-icon>
          <div class="result-text">
            <h3>{{ isCorrect ? '回答正确！' : '回答错误' }}</h3>
            <p>{{ isCorrect ? '继续保持，再接再厉！' : '不要气馁，查看解析学习一下吧' }}</p>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <div class="footer-left">
          <el-button v-if="!showAnswer && !isAnswered" @click="visible = false">
            取消
          </el-button>
        </div>
        <div class="footer-right">
          <el-button v-if="!showAnswer && !isAnswered" type="primary" @click="submitAnswer" :disabled="!canSubmit">
            提交答案
          </el-button>
          <el-button v-if="isAnswered && !showAnswer" type="primary" @click="viewAnswer">
            查看解析
          </el-button>
          <el-button v-if="showAnswer && !isCorrect" type="warning" @click="addToWrongBook">
            <el-icon><Warning /></el-icon>
            加入错题本
          </el-button>
          <el-button v-if="showAnswer" @click="nextQuestion">
            下一题
          </el-button>
          <el-button v-if="showAnswer" @click="visible = false">
            关闭
          </el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  question: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'addToWrong'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const selectedAnswer = ref('')
const textAnswer = ref('')
const showAnswer = ref(false)
const isAnswered = ref(false)
const isCorrect = ref(false)

const canSubmit = computed(() => {
  if (props.question?.options?.length) {
    return !!selectedAnswer.value
  }
  return !!textAnswer.value.trim()
})

const selectAnswer = (key) => {
  selectedAnswer.value = key
}

const submitAnswer = () => {
  if (!canSubmit.value) {
    ElMessage.warning('请先选择或输入答案')
    return
  }

  const userAnswer = props.question.options?.length ? selectedAnswer.value : textAnswer.value
  isCorrect.value = userAnswer === props.question.correctAnswer
  isAnswered.value = true

  if (isCorrect.value) {
    ElMessage.success('回答正确！')
  } else {
    ElMessage.error('回答错误，查看解析学习一下吧')
  }
}

const viewAnswer = () => {
  showAnswer.value = true
}

const addToWrongBook = () => {
  emit('addToWrong', props.question)
  ElMessage.success('已加入错题本')
}

const nextQuestion = () => {
  emit('next')
  resetState()
}

const resetState = () => {
  selectedAnswer.value = ''
  textAnswer.value = ''
  showAnswer.value = false
  isAnswered.value = false
  isCorrect.value = false
}

watch(() => props.modelValue, (val) => {
  if (val) {
    resetState()
  }
})
</script>

<style scoped>
.question-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.question-detail {
  max-height: 70vh;
  overflow-y: auto;
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

.tag.type {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.6);
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

.question-meta .el-icon {
  font-size: 16px;
}

.question-content {
  padding: 28px;
}

.content-title {
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 16px;
}

.content-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 15px;
  line-height: 1.8;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border-left: 4px solid #667eea;
  border-radius: 8px;
  margin-bottom: 24px;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 2px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(102, 126, 234, 0.3);
}

.option-item.selected {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.option-item.correct {
  background: rgba(16, 185, 129, 0.1);
  border-color: #10b981;
}

.option-item.wrong {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
}

.option-key {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  flex-shrink: 0;
}

.option-item.selected .option-key {
  background: #667eea;
}

.option-item.correct .option-key {
  background: #10b981;
}

.option-item.wrong .option-key {
  background: #ef4444;
}

.option-text {
  flex: 1;
  color: rgba(255, 255, 255, 0.8);
  font-size: 15px;
  line-height: 1.6;
}

.check-icon,
.close-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.check-icon {
  color: #10b981;
}

.close-icon {
  color: #ef4444;
}

.answer-input {
  margin-top: 16px;
}

.answer-input :deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 15px;
  line-height: 1.8;
}

.answer-section {
  padding: 28px;
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.correct-answer,
.explanation,
.key-points {
  margin-bottom: 24px;
}

.correct-answer:last-child,
.explanation:last-child,
.key-points:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 12px;
}

.answer-content,
.explanation-content {
  color: rgba(255, 255, 255, 0.8);
  font-size: 15px;
  line-height: 1.8;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
}

.points-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.point-tag {
  padding: 6px 12px;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: #667eea;
  font-size: 13px;
  font-weight: 600;
}

.result-section {
  padding: 28px;
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.result-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  border-radius: 16px;
  border: 2px solid;
}

.result-card.correct {
  background: rgba(16, 185, 129, 0.1);
  border-color: #10b981;
}

.result-card.wrong {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
}

.result-icon {
  font-size: 48px;
  flex-shrink: 0;
}

.result-card.correct .result-icon {
  color: #10b981;
}

.result-card.wrong .result-icon {
  color: #ef4444;
}

.result-text h3 {
  color: #fff;
  font-size: 20px;
  font-weight: 800;
  margin-bottom: 6px;
}

.result-text p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-left,
.footer-right {
  display: flex;
  gap: 12px;
}
</style>
