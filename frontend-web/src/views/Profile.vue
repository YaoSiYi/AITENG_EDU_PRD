<template>
  <div class="profile-container">
    <PageBreadcrumb current-name="个人中心" />

    <div class="profile-header">
      <div class="profile-banner">
        <div class="banner-gradient"></div>
      </div>

      <div class="profile-info">
        <div class="avatar-section">
          <div class="avatar">
            <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="avatar" />
            <el-icon v-else><User /></el-icon>
          </div>
          <el-button size="small" class="edit-avatar-btn">
            <el-icon><Camera /></el-icon>
          </el-button>
        </div>

        <div class="user-details">
          <h1 class="username">{{ userInfo.name }}</h1>
          <p class="user-role">{{ userInfo.role }}</p>
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-value">{{ userInfo.level }}</span>
              <span class="stat-label">等级</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ userInfo.points }}</span>
              <span class="stat-label">积分</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ userInfo.streak }}</span>
              <span class="stat-label">连续天数</span>
            </div>
          </div>
        </div>

        <el-button type="primary" size="large" @click="showEditDialog = true">
          <el-icon><Edit /></el-icon>
          编辑资料
        </el-button>
      </div>
    </div>

    <div class="profile-content">
      <div class="content-sidebar">
        <div class="menu-card">
          <div
            v-for="item in menuItems"
            :key="item.key"
            :class="['menu-item', { active: activeMenu === item.key, 'logout-item': item.key === 'logout' }]"
            @click="handleMenuClick(item.key)"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </div>
        </div>
      </div>

      <div class="content-main">
        <div v-if="activeMenu === 'overview'" class="overview-section">
          <div class="section-card">
            <h3 class="section-title">学习概览</h3>
            <div class="overview-grid">
              <div class="overview-item">
                <div class="overview-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="overview-info">
                  <span class="overview-value">1,248</span>
                  <span class="overview-label">完成题目</span>
                </div>
              </div>
              <div class="overview-item">
                <div class="overview-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
                  <el-icon><Check /></el-icon>
                </div>
                <div class="overview-info">
                  <span class="overview-value">85%</span>
                  <span class="overview-label">正确率</span>
                </div>
              </div>
              <div class="overview-item">
                <div class="overview-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="overview-info">
                  <span class="overview-value">42h</span>
                  <span class="overview-label">学习时长</span>
                </div>
              </div>
              <div class="overview-item">
                <div class="overview-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%)">
                  <el-icon><Trophy /></el-icon>
                </div>
                <div class="overview-info">
                  <span class="overview-value">12</span>
                  <span class="overview-label">获得成就</span>
                </div>
              </div>
            </div>
          </div>

          <div class="section-card">
            <h3 class="section-title">最近活动</h3>
            <div class="activity-timeline">
              <div v-for="activity in recentActivities" :key="activity.id" class="timeline-item">
                <div class="timeline-dot" :style="{ background: activity.color }"></div>
                <div class="timeline-content">
                  <h4 class="timeline-title">{{ activity.title }}</h4>
                  <p class="timeline-desc">{{ activity.description }}</p>
                  <span class="timeline-time">{{ formatDateTime(activity.time) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeMenu === 'achievements'" class="achievements-section">
          <div class="section-card">
            <h3 class="section-title">我的成就</h3>
            <div class="achievements-grid">
              <div
                v-for="achievement in achievements"
                :key="achievement.id"
                :class="['achievement-card', { locked: !achievement.unlocked }]"
              >
                <div class="achievement-icon" :style="{ background: achievement.color }">
                  <el-icon><component :is="achievement.icon" /></el-icon>
                </div>
                <h4 class="achievement-name">{{ achievement.name }}</h4>
                <p class="achievement-desc">{{ achievement.description }}</p>
                <div v-if="achievement.unlocked" class="achievement-date">
                  {{ achievement.unlockedDate }}
                </div>
                <div v-else class="achievement-progress">
                  <el-progress :percentage="achievement.progress" :stroke-width="6" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeMenu === 'settings'" class="settings-section">
          <div class="section-card">
            <h3 class="section-title">账号设置</h3>
            <el-form :model="settingsForm" label-width="120px">
              <el-form-item label="用户名">
                <el-input v-model="settingsForm.username" disabled />
              </el-form-item>
              <el-form-item label="昵称">
                <el-input v-model="settingsForm.nickname" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="settingsForm.email" />
              </el-form-item>
              <el-form-item label="手机号">
                <el-input v-model="settingsForm.phone" />
              </el-form-item>
              <el-form-item label="籍贯">
                <el-input v-model="settingsForm.hometown" placeholder="格式：xx省xx市" />
              </el-form-item>
              <el-form-item label="性别">
                <el-radio-group v-model="settingsForm.gender">
                  <el-radio value="male" class="male-radio">男</el-radio>
                  <el-radio value="female" class="female-radio">女</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="密码提示">
                <el-input v-model="settingsForm.passwordHint" placeholder="用于找回密码的提示信息" />
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input v-model="settingsForm.bio" type="textarea" :rows="4" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveSettings">保存设置</el-button>
              </el-form-item>
            </el-form>
          </div>

          <!-- 密码修改模块 -->
          <div class="section-card" style="margin-top: 24px">
            <h3 class="section-title">修改密码</h3>
            <el-form
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              label-width="120px"
              style="max-width: 600px"
            >
              <el-form-item label="账号">
                <el-input
                  :value="userStore.user?.username || settingsForm.username"
                  disabled
                  placeholder="当前登录账号"
                />
              </el-form-item>
              <el-form-item label="原始密码" prop="oldPassword">
                <el-input
                  v-model="passwordForm.oldPassword"
                  type="password"
                  placeholder="请输入原始密码"
                  show-password
                  clearable
                />
              </el-form-item>
              <el-form-item label="新密码" prop="newPassword">
                <el-input
                  v-model="passwordForm.newPassword"
                  type="password"
                  placeholder="请输入新密码（6-20位）"
                  show-password
                  clearable
                />
              </el-form-item>
              <el-form-item label="确认新密码" prop="confirmPassword">
                <el-input
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  placeholder="请再次输入新密码"
                  show-password
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
                <el-button @click="resetPasswordForm">重置</el-button>
              </el-form-item>
            </el-form>
            <el-alert
              title="密码修改提示"
              type="info"
              :closable="false"
              style="margin-top: 8px"
            >
              <div style="font-size: 10px; line-height: 1.3; color: rgba(255, 255, 255, 0.7)">
                <span>• 密码长度为 6-20 位字符 </span>
                <span>• 新密码不能与原始密码相同 </span>
                <span>• 修改密码后需要重新登录 </span>
                <span>• 请妥善保管您的密码</span>
              </div>
            </el-alert>
          </div>

          <div class="section-card" style="margin-top: 24px">
            <h3 class="section-title">隐私设置</h3>
            <div class="privacy-options">
              <div class="privacy-item">
                <div class="privacy-info">
                  <h4>公开学习数据</h4>
                  <p>允许其他用户查看你的学习统计</p>
                </div>
                <el-switch v-model="privacySettings.publicStats" />
              </div>
              <div class="privacy-item">
                <div class="privacy-info">
                  <h4>显示在线状态</h4>
                  <p>让好友看到你的在线状态</p>
                </div>
                <el-switch v-model="privacySettings.showOnline" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog v-model="showEditDialog" title="编辑资料" width="520px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="昵称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="角色">
          <el-input v-model="editForm.role" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="editForm.phone" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input v-model="editForm.bio" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveProfile">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDateTime } from '@/utils/datetime'
import { useUserStore } from '@/stores/user'
import PageBreadcrumb from '@/components/PageBreadcrumb.vue'

const router = useRouter()
const userStore = useUserStore()
const showEditDialog = ref(false)
const activeMenu = ref('overview')
const passwordFormRef = ref(null)

// 当切换到设置页面时，从用户store加载数据
watch(activeMenu, (newVal) => {
  if (newVal === 'settings' && userStore.user) {
    settingsForm.value.username = userStore.user.username || ''
    settingsForm.value.nickname = userStore.user.nickname || ''
    settingsForm.value.phone = userStore.user.phone || ''
    settingsForm.value.hometown = userStore.user.hometown || ''
    settingsForm.value.gender = userStore.user.gender || ''
    settingsForm.value.passwordHint = userStore.user.password_hint || ''
  }
})

// 密码修改表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 密码验证规则
const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原始密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为 6-20 位字符', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value === passwordForm.value.oldPassword) {
          callback(new Error('新密码不能与原始密码相同'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const userInfo = ref({
  name: '张同学',
  role: '软件测试学员',
  avatar: '',
  level: 15,
  points: 8520,
  streak: 12
})

const menuItems = [
  { key: 'overview', label: '概览', icon: 'Grid' },
  { key: 'achievements', label: '成就', icon: 'Trophy' },
  { key: 'settings', label: '设置', icon: 'Setting' },
  { key: 'logout', label: '退出账号', icon: 'SwitchButton' }
]

const recentActivities = ref([
  {
    id: 1,
    title: '完成Python练习',
    description: '完成了20道Python编程题，正确率90%',
    time: '2026-04-23 14:30:00',
    color: '#667eea'
  },
  {
    id: 2,
    title: '获得新成就',
    description: '解锁成就：连续学习7天',
    time: '2026-04-22 10:15:00',
    color: '#f093fb'
  },
  {
    id: 3,
    title: '参与活动',
    description: '参加了UI自动化实战周活动',
    time: '2026-04-21 16:45:00',
    color: '#4facfe'
  }
])

const achievements = ref([
  {
    id: 1,
    name: '初出茅庐',
    description: '完成第一道测试题目',
    icon: 'Star',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    unlocked: true,
    unlockedDate: '2024-03-15'
  },
  {
    id: 2,
    name: '坚持不懈',
    description: '连续学习7天',
    icon: 'Calendar',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    unlocked: true,
    unlockedDate: '2024-04-10'
  },
  {
    id: 3,
    name: '测试达人',
    description: '完成100道测试题',
    icon: 'Medal',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    unlocked: false,
    progress: 68
  }
])

const settingsForm = ref({
  username: '张同学',
  nickname: '张同学',
  email: 'zhang@example.com',
  phone: '138****8888',
  hometown: '北京省北京市',
  gender: '',
  passwordHint: '',
  bio: '热爱学习，追求进步'
})

const editForm = ref({
  name: userInfo.value.name,
  role: userInfo.value.role,
  nickname: settingsForm.value.nickname,
  email: settingsForm.value.email,
  phone: settingsForm.value.phone,
  hometown: settingsForm.value.hometown,
  gender: settingsForm.value.gender,
  passwordHint: settingsForm.value.passwordHint,
  bio: settingsForm.value.bio
})

const privacySettings = ref({
  publicStats: true,
  showOnline: true
})

const saveSettings = async () => {
  try {
    await userStore.updateProfile({
      nickname: settingsForm.value.nickname,
      hometown: settingsForm.value.hometown,
      gender: settingsForm.value.gender,
      password_hint: settingsForm.value.passwordHint
    })
    ElMessage.success('设置已保存')
  } catch (error) {
    ElMessage.error('保存失败：' + (error.response?.data?.detail || '请重试'))
  }
}

const saveProfile = () => {
  userInfo.value.name = editForm.value.name
  userInfo.value.role = editForm.value.role
  settingsForm.value.username = editForm.value.name
  settingsForm.value.email = editForm.value.email
  settingsForm.value.phone = editForm.value.phone
  settingsForm.value.bio = editForm.value.bio
  showEditDialog.value = false
  ElMessage.success('个人资料已更新')
}

// 处理菜单点击
const handleMenuClick = (key) => {
  if (key === 'logout') {
    handleLogout()
  } else {
    activeMenu.value = key
  }
}

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm(
    '确定要退出当前账号吗？',
    '退出确认',
    {
      confirmButtonText: '确定退出',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }).catch(() => {
    // 用户取消
  })
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    // 验证表单
    await passwordFormRef.value.validate()

    // 二次确认
    await ElMessageBox.confirm(
      '修改密码后需要重新登录，确定要继续吗？',
      '确认修改密码',
      {
        confirmButtonText: '确定修改',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 调用修改密码 API
    const response = await fetch('/api/users/change-password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        old_password: passwordForm.value.oldPassword,
        new_password: passwordForm.value.newPassword
      })
    })

    const data = await response.json()

    if (response.ok) {
      ElMessage.success('密码修改成功，请重新登录')
      // 清空表单
      resetPasswordForm()
      // 延迟退出登录
      setTimeout(() => {
        userStore.logout()
        router.push('/login')
      }, 1500)
    } else {
      // 处理错误
      if (data.old_password) {
        ElMessage.error('原始密码不正确')
      } else if (data.error) {
        ElMessage.error(data.error)
      } else {
        ElMessage.error('密码修改失败，请重试')
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('修改密码失败:', error)
    }
  }
}

// 重置密码表单
const resetPasswordForm = () => {
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  if (passwordFormRef.value) {
    passwordFormRef.value.clearValidate()
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
}

.profile-header {
  position: relative;
}

.profile-banner {
  height: 240px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  position: relative;
  overflow: hidden;
}

.banner-gradient {
  position: absolute;
  inset: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240"><path fill="rgba(255,255,255,0.05)" d="M0,96L48,112C96,128,192,160,288,165.3C384,171,480,149,576,128C672,107,768,85,864,90.7C960,96,1056,128,1152,133.3L1200,139L1200,240L1152,240C1056,240,960,240,864,240C768,240,672,240,576,240C480,240,384,240,288,240C192,240,96,240,48,240L0,240Z"></path></svg>');
  background-size: cover;
  opacity: 0.3;
}

.profile-info {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
  display: flex;
  align-items: flex-end;
  gap: 32px;
  transform: translateY(-60px);
}

.avatar-section {
  position: relative;
}

.avatar {
  width: 140px;
  height: 140px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 4px solid #1a1f3a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 64px;
  color: rgba(255, 255, 255, 0.6);
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.edit-avatar-btn {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-details {
  flex: 1;
}

.username {
  font-size: 36px;
  font-weight: 900;
  color: #fff;
  margin-bottom: 8px;
}

.user-role {
  color: rgba(255, 255, 255, 0.5);
  font-size: 16px;
  margin-bottom: 20px;
}

.user-stats {
  display: flex;
  gap: 40px;
}

.user-stats .stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-stats .stat-value {
  font-size: 28px;
  font-weight: 800;
  color: #667eea;
}

.user-stats .stat-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
}

.profile-content {
  max-width: 1400px;
  margin: -20px auto 0;
  padding: 0 40px 40px;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
}

.menu-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 16px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.menu-item.logout-item {
  color: #f56c6c;
  margin-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 20px;
}

.menu-item.logout-item:hover {
  background: rgba(245, 108, 108, 0.1);
  color: #f56c6c;
}

.menu-item.active {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
}

.content-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 32px;
}

.section-title {
  color: #fff;
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 28px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.overview-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 16px;
}

.overview-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  flex-shrink: 0;
}

.overview-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.overview-value {
  font-size: 28px;
  font-weight: 800;
  color: #fff;
}

.overview-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
}

.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.timeline-item {
  display: flex;
  gap: 20px;
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 11px;
  top: 32px;
  bottom: -24px;
  width: 2px;
  background: rgba(255, 255, 255, 0.05);
}

.timeline-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
}

.timeline-content {
  flex: 1;
}

.timeline-title {
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 6px;
}

.timeline-desc {
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  margin-bottom: 8px;
}

.timeline-time {
  color: rgba(255, 255, 255, 0.3);
  font-size: 12px;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.achievement-card {
  padding: 28px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s;
}

.achievement-card:hover {
  transform: translateY(-4px);
  border-color: rgba(102, 126, 234, 0.3);
}

.achievement-card.locked {
  opacity: 0.4;
}

.achievement-icon {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: #fff;
  margin: 0 auto 16px;
}

.achievement-name {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
}

.achievement-desc {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  margin-bottom: 12px;
}

.achievement-date {
  color: rgba(255, 255, 255, 0.3);
  font-size: 12px;
}

.settings-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-section :deep(.el-form-item__label) {
  color: rgba(255, 255, 255, 0.6);
}

.settings-section :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.settings-section :deep(.el-input__inner),
.settings-section :deep(.el-textarea__inner) {
  color: #fff;
}

.settings-section :deep(.el-radio__label) {
  color: rgba(255, 255, 255, 0.8);
}

.settings-section :deep(.el-radio__inner) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.3);
}

/* 男生选中颜色 - 湖蓝色 */
.settings-section :deep(.male-radio .el-radio__input.is-checked .el-radio__inner) {
  background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
  border-color: #22d3ee;
}

.settings-section :deep(.male-radio .el-radio__input.is-checked + .el-radio__label) {
  color: #22d3ee;
}

/* 女生选中颜色 - 粉色 */
.settings-section :deep(.female-radio .el-radio__input.is-checked .el-radio__inner) {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  border-color: #f472b6;
}

.settings-section :deep(.female-radio .el-radio__input.is-checked + .el-radio__label) {
  color: #f472b6;
}

.privacy-options {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.privacy-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
}

.privacy-info h4 {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
}

.privacy-info p {
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

@media (max-width: 1024px) {
  .profile-content {
    grid-template-columns: 1fr;
    padding: 0 20px 40px;
  }

  .content-sidebar {
    display: flex;
    overflow-x: auto;
    gap: 8px;
    padding-bottom: 4px;
  }

  .menu-card {
    display: flex;
    gap: 8px;
    padding: 12px;
    white-space: nowrap;
    width: max-content;
  }

  .menu-item {
    padding: 10px 16px;
    margin-bottom: 0;
    flex-shrink: 0;
  }

  .overview-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .achievements-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .profile-info {
    flex-direction: column;
    padding: 0 20px;
    transform: translateY(-40px);
  }

  .username {
    font-size: 26px;
  }

  .user-stats {
    gap: 24px;
  }

  .profile-info > .el-button {
    width: 100%;
  }

  .profile-content {
    margin-top: 0;
    padding: 0 16px 40px;
  }

  .section-card {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .profile-banner {
    height: 140px;
  }

  .avatar {
    width: 100px;
    height: 100px;
    font-size: 48px;
  }

  .username {
    font-size: 22px;
  }

  .user-stats .stat-value {
    font-size: 22px;
  }

  .overview-grid {
    grid-template-columns: 1fr;
  }

  .achievements-grid {
    grid-template-columns: 1fr;
  }
}
</style>
