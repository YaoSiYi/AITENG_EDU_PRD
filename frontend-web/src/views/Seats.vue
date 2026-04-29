<template>
  <div class="seats-container">
    <PageBreadcrumb current-name="查看座次" />

    <div class="seats-header">
      <h1 class="page-title">教室座位布局</h1>
      <div class="layout-controls">
        <el-radio-group v-model="layoutType" size="large">
          <el-radio-button value="8x6">
            <el-icon><Grid /></el-icon>
            8列6排 (48座)
          </el-radio-button>
          <el-radio-button value="10x8">
            <el-icon><Grid /></el-icon>
            10列8排 (80座)
          </el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <div class="classroom">
      <!-- 讲台 -->
      <div class="podium">
        <el-icon><Monitor /></el-icon>
        <span>讲台</span>
      </div>

      <!-- 座位区域 -->
      <div class="seats-area" :class="`layout-${layoutType}`">
        <div
          v-for="(row, rowIndex) in currentLayout.rows"
          :key="rowIndex"
          class="seat-row"
        >
          <div class="row-label">第{{ rowIndex + 1 }}排</div>

          <!-- 左侧座位 -->
          <div class="seat-section left-section">
            <div
              v-for="seatIndex in currentLayout.leftSeats"
              :key="`left-${seatIndex}`"
              class="seat"
              :class="getSeatClass(rowIndex, seatIndex, 'left')"
              @click="toggleSeat(rowIndex, seatIndex, 'left')"
            >
              <div class="seat-number">{{ getSeatNumber(rowIndex, seatIndex, 'left') }}</div>
              <div v-if="getSeatInfo(rowIndex, seatIndex, 'left')" class="seat-name">
                {{ getSeatInfo(rowIndex, seatIndex, 'left').name }}
              </div>
            </div>
          </div>

          <!-- 过道 -->
          <div class="aisle">
            <el-icon><Right /></el-icon>
          </div>

          <!-- 右侧座位 -->
          <div class="seat-section right-section">
            <div
              v-for="seatIndex in currentLayout.rightSeats"
              :key="`right-${seatIndex}`"
              class="seat"
              :class="getSeatClass(rowIndex, seatIndex, 'right')"
              @click="toggleSeat(rowIndex, seatIndex, 'right')"
            >
              <div class="seat-number">{{ getSeatNumber(rowIndex, seatIndex, 'right') }}</div>
              <div v-if="getSeatInfo(rowIndex, seatIndex, 'right')" class="seat-name">
                {{ getSeatInfo(rowIndex, seatIndex, 'right').name }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 图例 -->
      <div class="legend">
        <div class="legend-item">
          <div class="legend-seat empty"></div>
          <span>空座位</span>
        </div>
        <div class="legend-item">
          <div class="legend-seat female"></div>
          <span>女生</span>
        </div>
        <div class="legend-item">
          <div class="legend-seat male"></div>
          <span>男生</span>
        </div>
      </div>

      <!-- 期数信息 -->
      <div v-if="currentPeriod" class="period-info">
        <el-icon><Calendar /></el-icon>
        <span>{{ currentPeriod }}</span>
      </div>

      <!-- 统计信息 -->
      <div class="stats-info">
        <el-card>
          <div class="stat-item">
            <span class="stat-label">总座位：</span>
            <span class="stat-value">{{ totalSeats }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">已占座：</span>
            <span class="stat-value">{{ occupiedSeats }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">空座位：</span>
            <span class="stat-value">{{ emptySeats }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">女生：</span>
            <span class="stat-value female-count">{{ femaleCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">男生：</span>
            <span class="stat-value male-count">{{ maleCount }}</span>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Grid, Monitor, Right, Calendar } from '@element-plus/icons-vue'
import PageBreadcrumb from '@/components/PageBreadcrumb.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const layoutType = ref('8x6')

// 座位布局配置
const layouts = {
  '8x6': {
    rows: 6,
    leftSeats: 4,
    rightSeats: 4
  },
  '10x8': {
    rows: 8,
    leftSeats: 5,
    rightSeats: 5
  }
}

const currentLayout = computed(() => layouts[layoutType.value])

// 座位数据（示例数据）
const seats = ref({
  '8x6': {
    0: { // 第1排
      left: {
        0: { name: '张三', gender: 'female' },
        1: { name: '李四', gender: 'male' },
        2: null,
        3: { name: '王五', gender: 'female' }
      },
      right: {
        0: { name: '赵六', gender: 'male' },
        1: null,
        2: { name: '孙七', gender: 'female' },
        3: { name: '周八', gender: 'male' }
      }
    },
    1: { // 第2排
      left: {
        0: { name: '吴九', gender: 'male' },
        1: { name: '郑十', gender: 'female' },
        2: { name: '钱一', gender: 'male' },
        3: null
      },
      right: {
        0: null,
        1: { name: '陈二', gender: 'female' },
        2: { name: '刘三', gender: 'male' },
        3: { name: '杨四', gender: 'female' }
      }
    }
    // 其他排可以继续添加
  },
  '10x8': {
    0: {
      left: {
        0: { name: '张三', gender: 'female' },
        1: { name: '李四', gender: 'male' },
        2: null,
        3: { name: '王五', gender: 'female' },
        4: { name: '赵六', gender: 'male' }
      },
      right: {
        0: { name: '孙七', gender: 'female' },
        1: null,
        2: { name: '周八', gender: 'male' },
        3: { name: '吴九', gender: 'female' },
        4: { name: '郑十', gender: 'male' }
      }
    }
    // 其他排可以继续添加
  }
})

// 获取座位信息
const getSeatInfo = (rowIndex, seatIndex, section) => {
  const layoutSeats = seats.value[layoutType.value]
  if (!layoutSeats || !layoutSeats[rowIndex]) return null
  return layoutSeats[rowIndex][section]?.[seatIndex] || null
}

// 获取座位样式类
const getSeatClass = (rowIndex, seatIndex, section) => {
  const seatInfo = getSeatInfo(rowIndex, seatIndex, section)
  if (!seatInfo) return 'empty'
  return seatInfo.gender === 'female' ? 'female' : 'male'
}

// 获取座位编号
const getSeatNumber = (rowIndex, seatIndex, section) => {
  const leftSeats = currentLayout.value.leftSeats
  if (section === 'left') {
    return rowIndex * (leftSeats + currentLayout.value.rightSeats) + seatIndex + 1
  } else {
    return rowIndex * (leftSeats + currentLayout.value.rightSeats) + leftSeats + seatIndex + 1
  }
}

// 切换座位状态（点击座位）
const toggleSeat = (rowIndex, seatIndex, section) => {
  console.log(`点击座位: 第${rowIndex + 1}排, ${section === 'left' ? '左' : '右'}侧第${seatIndex + 1}个`)
  // TODO: 实现座位状态切换逻辑
}

// 统计信息
const totalSeats = computed(() => {
  const layout = currentLayout.value
  return layout.rows * (layout.leftSeats + layout.rightSeats)
})

const occupiedSeats = computed(() => {
  let count = 0
  const layoutSeats = seats.value[layoutType.value]
  if (!layoutSeats) return 0

  Object.values(layoutSeats).forEach(row => {
    if (row.left) {
      Object.values(row.left).forEach(seat => {
        if (seat) count++
      })
    }
    if (row.right) {
      Object.values(row.right).forEach(seat => {
        if (seat) count++
      })
    }
  })
  return count
})

const emptySeats = computed(() => totalSeats.value - occupiedSeats.value)

const femaleCount = computed(() => {
  let count = 0
  const layoutSeats = seats.value[layoutType.value]
  if (!layoutSeats) return 0

  Object.values(layoutSeats).forEach(row => {
    if (row.left) {
      Object.values(row.left).forEach(seat => {
        if (seat && seat.gender === 'female') count++
      })
    }
    if (row.right) {
      Object.values(row.right).forEach(seat => {
        if (seat && seat.gender === 'female') count++
      })
    }
  })
  return count
})

const maleCount = computed(() => {
  let count = 0
  const layoutSeats = seats.value[layoutType.value]
  if (!layoutSeats) return 0

  Object.values(layoutSeats).forEach(row => {
    if (row.left) {
      Object.values(row.left).forEach(seat => {
        if (seat && seat.gender === 'male') count++
      })
    }
    if (row.right) {
      Object.values(row.right).forEach(seat => {
        if (seat && seat.gender === 'male') count++
      })
    }
  })
  return count
})

// 获取当前用户的期数信息
const currentPeriod = computed(() => {
  const user = userStore.user
  console.log('当前用户信息:', user)
  console.log('期数字段:', user?.period)
  if (user && user.period) {
    return `第${user.period}期学员`
  }
  return ''
})
</script>

<style scoped>
.seats-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
  padding: 40px;
}

.seats-header {
  max-width: 1400px;
  margin: 0 auto 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 48px;
  font-weight: 900;
  background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.layout-controls :deep(.el-radio-button__inner) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.layout-controls :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: #10b981;
  border-color: #10b981;
  color: #fff;
}

.classroom {
  max-width: 1400px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 40px;
}

.podium {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #fff;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 40px;
  font-size: 20px;
  font-weight: 700;
}

.podium .el-icon {
  font-size: 32px;
}

.seats-area {
  margin-bottom: 40px;
}

.seat-row {
  display: flex;
  align-items: center;
  gap: 40px;
  margin-bottom: 28px;
}

.row-label {
  width: 80px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  font-weight: 600;
  text-align: right;
}

.seat-section {
  display: flex;
  gap: 28px;
}

.seat {
  width: 100px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.seat:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.seat.empty {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.seat.empty:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.seat.female {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  border-color: #f472b6;
  color: #fff;
}

.seat.male {
  background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
  border-color: #22d3ee;
  color: #fff;
}

.seat-number {
  font-size: 10px;
  opacity: 0.8;
}

.seat-name {
  font-size: 12px;
  font-weight: 600;
  margin-top: 2px;
}

.aisle {
  width: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.3);
  font-size: 24px;
}

.legend {
  display: flex;
  gap: 32px;
  justify-content: center;
  margin-bottom: 32px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.legend-seat {
  width: 40px;
  height: 40px;
  border-radius: 6px;
}

.legend-seat.empty {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.legend-seat.female {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
}

.legend-seat.male {
  background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
}

.period-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 24px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  margin-bottom: 32px;
  color: #10b981;
  font-size: 16px;
  font-weight: 600;
}

.period-info .el-icon {
  font-size: 20px;
}

.stats-info {
  margin-top: 0;
}

.stats-info :deep(.el-card) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.stats-info :deep(.el-card__body) {
  display: flex;
  gap: 32px;
  justify-content: center;
  padding: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.stat-value {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
}

.stat-value.female-count {
  color: #f472b6;
}

.stat-value.male-count {
  color: #22d3ee;
}

/* 10x8 布局调整 */
.layout-10x8 .seat {
  width: 84px;
  height: 42px;
}

.layout-10x8 .seat-name {
  font-size: 11px;
}

.layout-10x8 .seat-section {
  gap: 22px;
}

@media (max-width: 1024px) {
  .seats-container {
    padding: 20px;
  }

  .seats-header {
    flex-direction: column;
    gap: 20px;
  }

  .page-title {
    font-size: 32px;
  }

  .classroom {
    padding: 20px;
  }

  .seat {
    width: 80px;
    height: 40px;
  }

  .seat-name {
    font-size: 11px;
  }

  .seat-section {
    gap: 20px;
  }

  .seat-row {
    gap: 28px;
  }

  .stats-info :deep(.el-card__body) {
    flex-wrap: wrap;
    gap: 16px;
  }
}
</style>
