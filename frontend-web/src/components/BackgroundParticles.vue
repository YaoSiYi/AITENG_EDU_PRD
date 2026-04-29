<template>
  <div class="antigravity-bg" ref="container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const container = ref(null)
const canvas = ref(null)
let animationId = null
let particles = []
let mouse = { x: -9999, y: -9999 }

// 粒子配置
const CONFIG = {
  particleCount: 150,
  minRadius: 3,
  maxRadius: 8,
  floatSpeed: 0.15,
  mouseInfluence: 80,      // 鼠标影响半径
  mouseForce: 0.6,         // 排斥力强度
  colors: [
    'rgba(77, 150, 255, 0.3)',
    'rgba(107, 203, 119, 0.25)',
    'rgba(255, 107, 107, 0.2)',
    'rgba(192, 132, 252, 0.3)',
    'rgba(255, 217, 61, 0.25)',
    'rgba(244, 114, 182, 0.2)'
  ]
}

class Particle {
  constructor(w, h) {
    this.reset(w, h)
  }

  reset(w, h) {
    this.x = Math.random() * w
    this.y = Math.random() * h
    this.radius = CONFIG.minRadius + Math.random() * (CONFIG.maxRadius - CONFIG.minRadius)
    this.color = CONFIG.colors[Math.floor(Math.random() * CONFIG.colors.length)]
    this.vx = (Math.random() - 0.5) * 0.3
    this.vy = -CONFIG.floatSpeed - Math.random() * 0.2  // 向上飘
    this.rotation = Math.random() * Math.PI * 2
    this.rotationSpeed = (Math.random() - 0.5) * 0.02
    this.pulse = Math.random() * Math.PI * 2
    this.pulseSpeed = 0.02 + Math.random() * 0.02
  }

  update(w, h, mouseX, mouseY) {
    // 向上漂浮
    this.y += this.vy
    // 水平微摆
    this.x += this.vx
    this.vx += (Math.random() - 0.5) * 0.02
    this.vx = Math.max(-0.5, Math.min(0.5, this.vx))

    // 边界循环
    if (this.y < -this.radius) {
      this.y = h + this.radius
      this.x = Math.random() * w
    }
    if (this.x < -this.radius) this.x = w + this.radius
    if (this.x > w + this.radius) this.x = -this.radius

    // 鼠标交互 - 排斥力
    const dx = this.x - mouseX
    const dy = this.y - mouseY
    const dist = Math.sqrt(dx * dx + dy * dy)
    if (dist < CONFIG.mouseInfluence && dist > 0) {
      const force = (CONFIG.mouseInfluence - dist) / CONFIG.mouseInfluence * CONFIG.mouseForce
      const angle = Math.atan2(dy, dx)
      this.vx += Math.cos(angle) * force
      this.vy += Math.sin(angle) * force
    }

    // 旋转
    this.rotation += this.rotationSpeed
    // 呼吸脉动
    this.pulse += this.pulseSpeed
  }

  draw(ctx) {
    ctx.save()
    ctx.translate(this.x, this.y)
    ctx.rotate(this.rotation)
    const scale = 0.8 + 0.2 * Math.sin(this.pulse)
    ctx.scale(scale, scale)

    ctx.beginPath()
    ctx.arc(0, 0, this.radius, 0, Math.PI * 2)
    ctx.fillStyle = this.color
    ctx.fill()

    // 高光小圆点
    ctx.beginPath()
    ctx.arc(-this.radius * 0.3, -this.radius * 0.3, this.radius * 0.3, 0, Math.PI * 2)
    ctx.fillStyle = 'rgba(255,255,255,0.15)'
    ctx.fill()

    ctx.restore()
  }
}

function initParticles(w, h) {
  particles = []
  for (let i = 0; i < CONFIG.particleCount; i++) {
    particles.push(new Particle(w, h))
  }
}

function resize() {
  if (!canvas.value || !container.value) return
  const rect = container.value.getBoundingClientRect()
  canvas.value.width = rect.width * window.devicePixelRatio
  canvas.value.height = rect.height * window.devicePixelRatio
  canvas.value.style.width = rect.width + 'px'
  canvas.value.style.height = rect.height + 'px'
}

function animate() {
  if (!canvas.value) return
  const ctx = canvas.value.getContext('2d')
  const w = canvas.value.width
  const h = canvas.value.height

  ctx.clearRect(0, 0, w, h)

  const scale = window.devicePixelRatio || 1
  const mouseX = mouse.x * scale
  const mouseY = mouse.y * scale

  for (const p of particles) {
    p.update(w, h, mouseX, mouseY)
    p.draw(ctx)
  }

  animationId = requestAnimationFrame(animate)
}

function handleMouseMove(e) {
  mouse.x = e.clientX
  mouse.y = e.clientY
}

function handleMouseLeave() {
  mouse.x = -9999
  mouse.y = -9999
}

onMounted(() => {
  if (!canvas.value || !container.value) return
  resize()
  initParticles(canvas.value.width, canvas.value.height)
  animate()

  window.addEventListener('resize', resize)
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseleave', handleMouseLeave)
})

onBeforeUnmount(() => {
  if (animationId) cancelAnimationFrame(animationId)
  window.removeEventListener('resize', resize)
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseleave', handleMouseLeave)
})
</script>

<style scoped>
.antigravity-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;  /* 不干扰操作 */
  overflow: hidden;
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
```