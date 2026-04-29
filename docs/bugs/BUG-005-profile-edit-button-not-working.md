# BUG-005: 个人中心编辑资料按钮无效

**日期**: 2026-04-23  
**严重程度**: 🟡 Medium  
**状态**: ✅ 已解决  
**影响范围**: `/profile` 个人中心页面编辑资料功能

---

## 问题现象

用户在个人中心页面点击"编辑资料"按钮后，没有任何反应，无法编辑个人信息。

---

## 根因分析

`frontend-web/src/views/Profile.vue` 中：

1. "编辑资料"按钮绑定了点击事件 `@click="showEditDialog = true"`
2. 定义了响应式变量 `const showEditDialog = ref(false)`
3. **但页面中缺少对应的编辑弹窗组件**（`el-dialog`）
4. 导致按钮点击后虽然状态改变了，但用户看不到任何界面变化

**问题代码**：
```vue
<!-- 按钮存在 -->
<el-button type="primary" size="large" @click="showEditDialog = true">
  <el-icon><Edit /></el-icon>
  编辑资料
</el-button>

<!-- 但缺少对应的弹窗 -->
<!-- 没有 <el-dialog v-model="showEditDialog"> -->
```

---

## 修复内容

### 1) 新增编辑资料弹窗

**文件**: `frontend-web/src/views/Profile.vue`

在 `</div>` 结束标签前添加编辑弹窗：

```vue
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
```

### 2) 新增编辑表单数据

```javascript
const editForm = ref({
  name: userInfo.value.name,
  role: userInfo.value.role,
  email: settingsForm.value.email,
  phone: settingsForm.value.phone,
  bio: settingsForm.value.bio
})
```

### 3) 实现保存功能

```javascript
const saveProfile = () => {
  // 更新用户信息
  userInfo.value.name = editForm.value.name
  userInfo.value.role = editForm.value.role
  
  // 同步到设置表单
  settingsForm.value.username = editForm.value.name
  settingsForm.value.email = editForm.value.email
  settingsForm.value.phone = editForm.value.phone
  settingsForm.value.bio = editForm.value.bio
  
  // 关闭弹窗并提示
  showEditDialog.value = false
  ElMessage.success('个人资料已更新')
}
```

### 4) 引入 ElMessage 组件

```javascript
import { ElMessage } from 'element-plus'
```

### 5) 优化设置保存功能

同时修复了"设置"标签页中的保存功能，添加了成功提示：

```javascript
const saveSettings = () => {
  userInfo.value.name = settingsForm.value.username
  ElMessage.success('设置已保存')
}
```

---

## 验证结果

- ✅ 点击"编辑资料"按钮弹出编辑对话框
- ✅ 可以编辑昵称、角色、邮箱、手机号、个人简介
- ✅ 点击"保存"按钮更新个人信息
- ✅ 显示成功提示消息
- ✅ 弹窗自动关闭
- ✅ 页面头部信息实时更新
- ✅ 设置页面的保存功能也正常工作

---

## 预防措施

1. 在开发阶段，确保所有按钮的点击事件都有对应的处理逻辑和UI反馈
2. 对于弹窗类交互，应该在实现按钮的同时实现对应的弹窗组件
3. 添加代码审查检查点：检查 `v-model` 绑定的变量是否有对应的UI组件使用
4. 使用 Vue DevTools 检查响应式数据变化是否正确触发UI更新

---

## 相关问题

- 类似问题可能存在于其他页面的编辑/新增功能中
- 建议全面检查所有带有"编辑"、"新增"按钮的页面

---

**修复人**: Claude Sonnet 4.6  
**最后更新**: 2026-04-23
