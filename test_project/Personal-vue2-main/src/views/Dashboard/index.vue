<template>
  <div class="dashboard-container">
    <el-row :gutter="40" class="panel-group">
      <el-col v-for="(item, index) in cardData" :key="index" @click.native="handleCardClick(index)"
        :class="{ active: activeCardIndex === index }" :xs="24" :sm="12" :md="8" :lg="8" class="card-panel-col">
        <div class="card-panel">
          <div class="card-panel-icon-wrapper" :class="item.iconClass">
            <i class="card-panel-icon" :class="item.icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">{{ item.title }}</div>
            <span class="card-panel-num">{{ item.value }}{{ item.unit }}</span>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-group">
      <el-col :xs="24" :sm="12" class="chart-col">
        <el-card class="chart-card">
          <EChart :option="barChartOptions" height="400px"></EChart>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" class="chart-col">
        <el-card class="chart-card">
          <EChart :option="pieChartOptions" height="400px"></EChart>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-group">
      <el-col :xs="24" :sm="12" class="chart-col">
        <el-card class="chart-card">
          <EChart :option="lineChartOptions" height="400px"></EChart>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" class="chart-col">
        <el-card class="chart-card">
          <EChart :option="areaChartOptions" height="400px"></EChart>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import EChart from '@/components/EChart.vue'

export default {
  name: 'Dashboard',
  components: {
    EChart
  },
  data() {
    return {
      // 当前激活的卡片索引
      activeCardIndex: -1,

      // 卡片数据
      cardData: [
        {
          title: '登录平台次数',
          value: 128,
          unit: '次',
          icon: 'el-icon-s-data',
          iconClass: 'icon-people',
          chartSeriesIndex: 0,
          chartDataIndex: 0
        },
        {
          title: '成功登录次数',
          value: 122,
          unit: '次',
          icon: 'el-icon-success',
          iconClass: 'icon-message',
          chartSeriesIndex: 0,
          chartDataIndex: 1
        },
        {
          title: '登录成功率',
          value: 95.5,
          unit: '%',
          icon: 'el-icon-s-marketing',
          iconClass: 'icon-money',
          chartSeriesIndex: 1,
          chartDataIndex: 0
        },
        {
          title: '展品数量',
          value: 67,
          unit: '条',
          icon: 'el-icon-s-comment',
          iconClass: 'icon-shopping',
          chartSeriesIndex: 0,
          chartDataIndex: 2
        },
        {
          title: '问题反馈数量',
          value: 245,
          unit: '条',
          icon: 'el-icon-user',
          iconClass: 'icon-shopping',
          chartSeriesIndex: 1,
          chartDataIndex: 1
        },
        {
          title: '展台使用次数',
          value: 89,
          unit: '次',
          icon: 'el-icon-s-platform',
          iconClass: 'icon-shopping',
          chartSeriesIndex: 0,
          chartDataIndex: 3
        }
      ],

      // 柱状图配置
      barChartOptions: {
        title: {
          text: '数据统计'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['访问量', '反馈量']
        },
        xAxis: {
          type: 'category',
          data: ['登录平台', '成功登录', '展品数', '展台使用']
        },
        yAxis: {},
        series: [
          {
            name: '访问量',
            type: 'bar',
            color: '#40c9c6',
            data: [128, 122, 67, 89],
            barGap: '20%'
          },
          {
            name: '反馈量',
            type: 'bar',
            color: '#36a3f7',
            data: [245, 95, 120, 150]
          }
        ],
        grid: {
          left: '35px',
          right: '35px',
          bottom: '35px'
        }
      },

      // 饼图配置
      pieChartOptions: {
        title: {
          text: '用户分布',
          left: 'center',
          top: '10%',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          }
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'horizontal',
          left: 'center',
          top: 'bottom',
          data: ['普通用户', 'VIP用户', '管理员']
        },
        series: [
          {
            name: '用户分布',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: [
              { value: 1200, name: '普通用户' },
              { value: 150, name: 'VIP用户' },
              { value: 25, name: '管理员' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },

      // 折线图配置
      lineChartOptions: {
        title: {
          text: '趋势分析'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['用户增长', '活跃度']
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '用户增长',
            type: 'line',
            data: [120, 132, 101, 134, 90, 230, 210],
            color: '#40c9c6'
          },
          {
            name: '活跃度',
            type: 'line',
            data: [220, 182, 191, 234, 290, 330, 310],
            color: '#36a3f7'
          }
        ],
        grid: {
          left: '35px',
          right: '35px',
          bottom: '35px'
        }
      },

      // 区域图配置
      areaChartOptions: {
        title: {
          text: '月度统计'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['新增用户', '订单量', '收入']
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['1月', '2月', '3月', '4月', '5月', '6月']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '新增用户',
            type: 'line',
            stack: '总量',
            areaStyle: {
              color: '#40c9c6'
            },
            data: [120, 230, 340, 260, 310, 440],
            color: '#40c9c6'
          },
          {
            name: '订单量',
            type: 'line',
            stack: '总量',
            areaStyle: {
              color: '#36a3f7'
            },
            data: [80, 120, 180, 150, 170, 220],
            color: '#36a3f7'
          },
          {
            name: '收入',
            type: 'line',
            stack: '总量',
            areaStyle: {
              color: '#f4516c'
            },
            data: [60, 90, 130, 100, 120, 180],
            color: '#f4516c'
          }
        ],
        grid: {
          left: '35px',
          right: '35px',
          bottom: '35px'
        }
      }
    }
  },

  methods: {
    // 点击卡片
    handleCardClick(cardIndex) {
      // 切换选中状态
      if (this.activeCardIndex === cardIndex) {
        // 如果点击的是已选中的卡片，则取消选中
        this.activeCardIndex = -1
      } else {
        // 设置新的选中卡片
        this.activeCardIndex = cardIndex
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
}

.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 25px;

    &.active {
      .card-panel {
        border: 2px solid #40c9c6;
      }
    }
  }

  .card-panel {
    height: 100px;
    cursor: pointer;
    font-size: 12px;
    margin-right: 10px;
    margin-left: 10px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: white;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 0, 0, 0.05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3;
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3;
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      font-weight: bold;
      margin: 30px;
      margin-left: 190px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 10px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

.chart-group {
  margin-top: 20px;
  width: 100%;

  .chart-card {
    margin-bottom: 20px;
  }

  .chart-col {
    padding-left: 0;
    padding-right: 0;
  }
}

@media (max-width: 550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
