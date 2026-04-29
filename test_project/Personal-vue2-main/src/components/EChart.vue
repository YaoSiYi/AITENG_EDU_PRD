<template>
  <div :id="chartId" :style="{ width: '100%', height: height }" />
</template>

<script>
import * as echarts from 'echarts'

export default {
  props: {
    option: {
      type: Object,
      default: () => {}
    },
    height: {
      type: String,
      default: '400px'
    }
  },
  data() {
    return {
      chartId: 'chart_' + Date.now() + '_' + Math.floor(Math.random() * 1000)
    }
  },
  watch: {
    option: {
      deep: true,
      handler(newOption) {
        this.updateOption(newOption)
      }
    }
  },
  mounted() {
    this.initChart()
    // 添加窗口大小改变时自适应
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    // 销毁前清除事件监听器和图表实例
    if (this.chart) {
      window.removeEventListener('resize', this.handleResize)
      this.chart.dispose()
    }
  },
  methods: {
    initChart() {
      const chartDom = document.getElementById(this.chartId)
      if (chartDom) {
        this.chart = echarts.init(chartDom)
        if (this.option) {
          this.chart.setOption(this.option, true) // 使用 notMerge: true
        }
      }
    },
    updateOption(newOption) {
      if (this.chart && newOption) {
        this.chart.setOption(newOption, true) // 使用 notMerge: true
      }
    },
    handleResize() {
      if (this.chart) {
        // 使用 setTimeout 确保 resize 在下次 DOM 更新周期后执行
        this.$nextTick(() => {
          this.chart.resize({
            animation: {
              duration: 300
            }
          })
        })
      }
    }
  }
}
</script>