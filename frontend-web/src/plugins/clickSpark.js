// 鼠标点击火花效果插件
export default {
  install(app) {
    // 只添加一次样式
    const styleId = 'click-spark-style'
    if (!document.getElementById(styleId)) {
      const style = document.createElement('style')
      style.id = styleId
      style.textContent = `
        .click-spark {
          position: fixed;
          pointer-events: none;
          z-index: 99999;
        }
        .click-spark .spark {
          position: absolute;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #fff;
          box-shadow: 0 0 6px currentColor;
          animation: sparkFly 0.8s ease-out forwards;
        }
        @keyframes sparkFly {
          0% { opacity: 1; transform: translate(0, 0) scale(1); }
          100% { opacity: 0; transform: translate(var(--tx), var(--ty)) scale(0); }
        }
      `
      document.head.appendChild(style)
    }

    const colors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#c084fc', '#f472b6']

    const createSparks = (x, y) => {
      const container = document.createElement('div')
      container.className = 'click-spark'
      container.style.left = x + 'px'
      container.style.top = y + 'px'

      const numSparks = 10
      for (let i = 0; i < numSparks; i++) {
        const spark = document.createElement('div')
        spark.className = 'spark'
        const angle = (i / numSparks) * 360
        const distance = 40 + Math.random() * 60
        const tx = Math.cos(angle * Math.PI / 180) * distance
        const ty = Math.sin(angle * Math.PI / 180) * distance
        spark.style.setProperty('--tx', tx + 'px')
        spark.style.setProperty('--ty', ty + 'px')
        spark.style.background = colors[Math.floor(Math.random() * colors.length)]
        container.appendChild(spark)
      }

      document.body.appendChild(container)
      setTimeout(() => container.remove(), 800)
    }

    // 挂载到全局，方便在组件内调用
    app.config.globalProperties.$clickSpark = createSparks

    // 全局监听点击事件
    document.addEventListener('click', (e) => {
      createSparks(e.clientX, e.clientY)
    })
  }
}