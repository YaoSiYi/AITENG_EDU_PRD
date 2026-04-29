/**
 * 工具函数集合
 */

/**
 * 格式化日期时间
 * @param {Date|String|Number} date - 日期对象、时间戳或日期字符串
 * @param {String} format - 格式化模板，默认 'YYYY-MM-DD HH:mm:ss'
 * @returns {String}
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hour = String(d.getHours()).padStart(2, '0')
  const minute = String(d.getMinutes()).padStart(2, '0')
  const second = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second)
}

/**
 * 防抖函数
 * @param {Function} func - 要执行的函数
 * @param {Number} wait - 等待时间（毫秒）
 * @returns {Function}
 */
export function debounce(func, wait = 500) {
  let timeout
  return function(...args) {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      func.apply(this, args)
    }, wait)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要执行的函数
 * @param {Number} wait - 等待时间（毫秒）
 * @returns {Function}
 */
export function throttle(func, wait = 500) {
  let previous = 0
  return function(...args) {
    const now = Date.now()
    if (now - previous > wait) {
      func.apply(this, args)
      previous = now
    }
  }
}

/**
 * 深拷贝
 * @param {Any} obj - 要拷贝的对象
 * @returns {Any}
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof Array) return obj.map(item => deepClone(item))

  const cloneObj = {}
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      cloneObj[key] = deepClone(obj[key])
    }
  }
  return cloneObj
}

/**
 * 显示Toast提示
 * @param {String} title - 提示文字
 * @param {String} icon - 图标类型：success/error/none
 * @param {Number} duration - 持续时间（毫秒）
 */
export function showToast(title, icon = 'none', duration = 2000) {
  uni.showToast({
    title,
    icon,
    duration,
    mask: true
  })
}

/**
 * 显示加载提示
 * @param {String} title - 提示文字
 */
export function showLoading(title = '加载中...') {
  uni.showLoading({
    title,
    mask: true
  })
}

/**
 * 隐藏加载提示
 */
export function hideLoading() {
  uni.hideLoading()
}

/**
 * 显示确认对话框
 * @param {String} content - 提示内容
 * @param {String} title - 标题
 * @returns {Promise<Boolean>}
 */
export function showConfirm(content, title = '提示') {
  return new Promise((resolve) => {
    uni.showModal({
      title,
      content,
      success: (res) => {
        resolve(res.confirm)
      }
    })
  })
}

/**
 * 获取课程阶段名称
 * @param {Number} stage - 阶段编号（1-10）
 * @returns {String}
 */
export function getStageName(stage) {
  const stageNames = {
    1: '第一阶段：软件测试基础',
    2: '第二阶段：功能与非功能测试',
    3: '第三阶段：Linux和MySQL',
    4: '第四阶段：Python课程',
    5: '第五阶段：UI自动化',
    6: '第六阶段：接口测试',
    7: '第七阶段：性能测试',
    8: '第八阶段：接口自动化',
    9: '第九阶段：项目实战',
    10: '第十阶段：AI大模型与Agent'
  }
  return stageNames[stage] || `第${stage}阶段`
}

/**
 * 获取难度标签
 * @param {String} difficulty - 难度：easy/medium/hard
 * @returns {Object} { text, color }
 */
export function getDifficultyLabel(difficulty) {
  const labels = {
    easy: { text: '简单', color: '#67C23A' },
    medium: { text: '中等', color: '#E6A23C' },
    hard: { text: '困难', color: '#F56C6C' }
  }
  return labels[difficulty] || { text: '未知', color: '#909399' }
}
