# 前台登出功能实现文档

## 功能概述

为前台界面添加了两处登出功能：
1. **个人中心页面**：在左侧菜单底部新增"退出账号"选项
2. **主页导航栏**：将"个人中心"改为下拉菜单，包含多个选项

---

## 功能详情

### 1. 个人中心页面 - 退出账号

**位置**：`/profile` 页面左侧菜单底部

**功能**：
- 显示红色的"退出账号"菜单项
- 点击后弹出确认对话框
- 确认后退出登录并跳转到登录页

**样式特点**：
- 红色文字和图标
- 与其他菜单项用分隔线隔开
- 悬停时显示浅红色背景

### 2. 主页导航栏 - 个人中心下拉菜单

**位置**：主页顶部导航栏

**下拉菜单选项**：
1. **个人资料**：跳转到个人中心页面
2. **显示/隐藏在线状态**：切换在线状态显示
3. **公开/隐藏学习数据**：切换学习数据公开状态
4. **退出账号**：退出登录（红色高亮）

**交互方式**：
- 鼠标悬停触发下拉菜单
- 点击选项执行对应操作
- 退出账号需要二次确认

---

## 技术实现

### 修改的文件

#### 1. `frontend-web/src/views/Profile.vue`

**新增内容**：
- 导入 `useRouter` 和 `ElMessageBox`
- 导入 `useUserStore`
- 添加 `handleMenuClick` 函数
- 添加 `handleLogout` 函数
- 更新 `menuItems` 数组，添加"退出账号"项
- 更新菜单点击事件处理
- 添加 `.logout-item` 样式

**关键代码**：
```javascript
// 菜单项配置
const menuItems = [
  { key: 'overview', label: '概览', icon: 'Grid' },
  { key: 'achievements', label: '成就', icon: 'Trophy' },
  { key: 'settings', label: '设置', icon: 'Setting' },
  { key: 'logout', label: '退出账号', icon: 'SwitchButton' }
]

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
```

#### 2. `frontend-web/src/views/Home.vue`

**新增内容**：
- 导入 `ref`、`useRouter`、`ElMessageBox`
- 添加用户设置状态变量
- 将"个人中心"链接改为下拉菜单
- 添加 `handleCommand` 函数
- 添加 `handleLogout` 函数
- 添加 `.profile-dropdown` 样式

**关键代码**：
```vue
<!-- 个人中心下拉菜单 -->
<el-dropdown v-if="userStore.isAuthenticated" trigger="hover" @command="handleCommand">
  <span class="nav-link profile-dropdown">
    个人中心
    <el-icon class="el-icon--right"><arrow-down /></el-icon>
  </span>
  <template #dropdown>
    <el-dropdown-menu>
      <el-dropdown-item command="profile">
        <el-icon><User /></el-icon>
        <span>个人资料</span>
      </el-dropdown-item>
      <el-dropdown-item command="online" divided>
        <el-icon><View /></el-icon>
        <span>{{ showOnlineStatus ? '隐藏' : '显示' }}在线状态</span>
      </el-dropdown-item>
      <el-dropdown-item command="public">
        <el-icon><DataAnalysis /></el-icon>
        <span>{{ publicLearningData ? '隐藏' : '公开' }}学习数据</span>
      </el-dropdown-item>
      <el-dropdown-item command="logout" divided>
        <el-icon style="color: #f56c6c"><SwitchButton /></el-icon>
        <span style="color: #f56c6c">退出账号</span>
      </el-dropdown-item>
    </el-dropdown-menu>
  </template>
</el-dropdown>
```

---

## 使用说明

### 方式一：个人中心页面退出

1. 访问 `http://localhost:3000/profile`
2. 在左侧菜单底部找到"退出账号"（红色）
3. 点击"退出账号"
4. 在弹出的确认对话框中点击"确定退出"
5. 系统提示"已退出登录"
6. 自动跳转到登录页面

### 方式二：主页下拉菜单退出

1. 访问 `http://localhost:3000/`
2. 将鼠标悬停在顶部导航栏的"个人中心"上
3. 在下拉菜单中点击"退出账号"（红色）
4. 在弹出的确认对话框中点击"确定退出"
5. 系统提示"已退出登录"
6. 自动跳转到登录页面

### 隐私设置功能

在主页下拉菜单中还可以：

1. **显示/隐藏在线状态**
   - 点击后切换在线状态显示
   - 显示成功提示

2. **公开/隐藏学习数据**
   - 点击后切换学习数据公开状态
   - 显示成功提示

---

## 安全特性

### 1. 二次确认
- 退出登录前弹出确认对话框
- 防止误操作
- 用户可以取消操作

### 2. 清除认证信息
- 调用 `userStore.logout()` 清除 token
- 清除用户状态
- 确保安全退出

### 3. 自动跳转
- 退出后自动跳转到登录页
- 防止未授权访问

---

## 样式设计

### 个人中心页面

```css
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
```

### 主页导航栏

```css
.profile-dropdown {
  display: flex;
  align-items: center;
  gap: 4px;
}
```

---

## 测试步骤

### 1. 测试个人中心退出

- [ ] 访问个人中心页面
- [ ] 验证左侧菜单显示"退出账号"（红色）
- [ ] 点击"退出账号"
- [ ] 验证弹出确认对话框
- [ ] 点击"取消"，验证对话框关闭且未退出
- [ ] 再次点击"退出账号"
- [ ] 点击"确定退出"
- [ ] 验证显示"已退出登录"提示
- [ ] 验证跳转到登录页面
- [ ] 验证无法访问需要登录的页面

### 2. 测试主页下拉菜单

- [ ] 访问主页
- [ ] 将鼠标悬停在"个人中心"上
- [ ] 验证显示下拉菜单
- [ ] 验证菜单包含4个选项
- [ ] 点击"个人资料"，验证跳转到个人中心
- [ ] 返回主页，悬停"个人中心"
- [ ] 点击"显示/隐藏在线状态"，验证提示信息
- [ ] 点击"公开/隐藏学习数据"，验证提示信息
- [ ] 点击"退出账号"（红色）
- [ ] 验证弹出确认对话框
- [ ] 点击"确定退出"
- [ ] 验证退出成功并跳转到登录页

### 3. 测试样式

- [ ] 验证"退出账号"显示为红色
- [ ] 验证悬停时背景变为浅红色
- [ ] 验证下拉菜单样式正常
- [ ] 验证图标显示正常

---

## 已更新的文档

1. ✅ `README.md` - 添加前台登出功能说明
2. ✅ `CHANGELOG.md` - 记录新增功能
3. ✅ `docs/LOGOUT_FEATURE.md` - 本文档

---

## 功能对比

| 功能 | 修改前 | 修改后 |
|------|--------|--------|
| 个人中心退出 | ❌ 无退出选项 | ✅ 左侧菜单底部有退出选项 |
| 主页退出 | ❌ 无退出选项 | ✅ 下拉菜单中有退出选项 |
| 隐私设置 | ❌ 无隐私设置 | ✅ 可设置在线状态和数据公开 |
| 退出确认 | - | ✅ 二次确认防止误操作 |
| 样式区分 | - | ✅ 退出选项红色高亮 |

---

## 注意事项

1. **退出确认**：退出操作需要用户确认，防止误操作
2. **状态清除**：退出后会清除所有登录状态
3. **自动跳转**：退出后自动跳转到登录页面
4. **隐私设置**：在线状态和学习数据设置仅为前端状态，需要后端支持才能真正生效

---

## 后续优化建议

1. **后端支持**：
   - 添加在线状态 API
   - 添加学习数据公开设置 API
   - 记录用户隐私设置偏好

2. **功能增强**：
   - 添加"记住我"功能
   - 添加自动登出（超时）
   - 添加多设备登录管理

3. **用户体验**：
   - 添加退出动画效果
   - 优化下拉菜单交互
   - 添加快捷键支持

---

**功能已完成！** 🎉
