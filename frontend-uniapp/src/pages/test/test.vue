<template>
  <view class="test-container">
    <view class="test-header">
      <text class="test-title">测试页面</text>
    </view>

    <view class="test-section">
      <text class="section-title">基础测试</text>
      <view class="test-item">
        <text>✅ Vue组件渲染正常</text>
      </view>
      <view class="test-item">
        <text>✅ 响应式数据: {{ count }}</text>
      </view>
      <view class="test-item">
        <button @click="increment">点击测试 ({{ count }})</button>
      </view>
    </view>

    <view class="test-section">
      <text class="section-title">数据测试</text>
      <view class="test-item" v-for="item in testData" :key="item.id">
        <text>{{ item.name }}: {{ item.value }}</text>
      </view>
    </view>

    <view class="test-section">
      <text class="section-title">导航测试</text>
      <button @click="goToIndex">跳转到首页</button>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)
const testData = ref([
  { id: 1, name: '测试1', value: '正常' },
  { id: 2, name: '测试2', value: '正常' },
  { id: 3, name: '测试3', value: '正常' }
])

const increment = () => {
  count.value++
  console.log('Count:', count.value)
}

const goToIndex = () => {
  uni.switchTab({
    url: '/pages/index/index'
  })
}

console.log('Test page loaded')
</script>

<style scoped>
.test-container {
  padding: 32rpx;
  background: #f5f7fa;
  min-height: 100vh;
}

.test-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40rpx;
  border-radius: 12rpx;
  margin-bottom: 32rpx;
}

.test-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #ffffff;
}

.test-section {
  background: #ffffff;
  padding: 32rpx;
  border-radius: 12rpx;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
  margin-bottom: 24rpx;
  display: block;
}

.test-item {
  padding: 16rpx 0;
  font-size: 28rpx;
  color: #666666;
}

button {
  width: 100%;
  padding: 24rpx;
  background: #667eea;
  color: #ffffff;
  border: none;
  border-radius: 8rpx;
  font-size: 28rpx;
  margin-top: 16rpx;
}
</style>
