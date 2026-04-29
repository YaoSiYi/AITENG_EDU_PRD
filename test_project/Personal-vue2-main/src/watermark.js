const watermark = {}

let MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver
let watermarkDom = null

const setWatermark = (str) => {
  const id = '1.23452384164.123412415'

  if (document.getElementById(id) !== null) {
    document.body.removeChild(document.getElementById(id))
  }

  const can = document.createElement('canvas')
  // 设置canvas的长宽
  can.width = 200
  can.height = 150

  const cans = can.getContext('2d')
  // 旋转角度
  cans.rotate(-20 * Math.PI / 180)
  cans.font = '16px Microsoft JhengHei'
  // 设置字体填充颜色
  cans.fillStyle = 'rgba(200, 200, 200, 0.3)'
  // 设置字体内容
  cans.textAlign = 'left'
  cans.textBaseline = 'middle'
  cans.fillText(str, can.width / 10, can.height / 2)

  const div = document.createElement('div')
  div.id = id
  div.style.pointerEvents = 'none'
  div.style.top = '0px'
  div.style.left = '0px'
  div.style.opacity = '0.2'
  div.style.position = 'fixed'
  div.style.zIndex = '100000'
  div.style.width = document.documentElement.clientWidth + 'px'
  div.style.height = document.documentElement.clientHeight + 'px'
  div.style.background = 'url(' + can.toDataURL('image/png') + ') left top repeat'
  div.style.display = 'block'
  document.body.appendChild(div)
  
  // 创建防篡改检测
  watermarkDom = div
  
  return id
}

// 加强版水印，防止被删除
watermark.set = (str) => {
  let id = setWatermark(str)
  
  // 启动防篡改检测
  const observer = new MutationObserver(function (mutations) {
    if (watermarkDom && !watermarkDom.parentNode) {
      // 如果水印被删除，则重新创建
      setWatermark(str)
    }
  })
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  })
  
  // 定期检查水印是否存在
  setInterval(() => {
    if (document.getElementById(id) === null) {
      id = setWatermark(str)
    }
  }, 1000)
  
  return id
}

module.exports = watermark