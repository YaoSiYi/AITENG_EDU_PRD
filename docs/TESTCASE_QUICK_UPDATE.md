# 测试用例管理 - 快速更新功能说明

## 功能概述

在测试用例列表中，可以直接点击"优先级"、"状态"、"冒烟"标签快速修改，无需打开编辑对话框。

---

## 使用方法

### 1. 修改优先级

**操作**: 点击优先级标签（紧急/高/中/低）

**效果**: 弹出下拉菜单，选择新的优先级

**选项**:
- 紧急（critical）
- 高（high）
- 中（medium）
- 低（low）

### 2. 修改状态

**操作**: 点击状态标签（草稿/有效/已废弃）

**效果**: 弹出下拉菜单，选择新的状态

**选项**:
- 草稿（draft）
- 有效（active）
- 已废弃（deprecated）

### 3. 切换冒烟用例

**操作**: 直接点击冒烟标签（是/否）

**效果**: 立即切换状态（是 ↔ 否）

---

## 技术实现

### 前端实现

**文件**: `frontend-web/src/views/testcases/index.vue`

#### 1. 优先级和状态（下拉菜单）

```vue
<el-dropdown @command="(val) => handleQuickUpdate(row, 'priority', val)">
  <el-tag :type="getPriorityType(row.priority)" size="small" style="cursor: pointer">
    {{ getPriorityLabel(row.priority) }}
    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
  </el-tag>
  <template #dropdown>
    <el-dropdown-menu>
      <el-dropdown-item command="critical">紧急</el-dropdown-item>
      <el-dropdown-item command="high">高</el-dropdown-item>
      <el-dropdown-item command="medium">中</el-dropdown-item>
      <el-dropdown-item command="low">低</el-dropdown-item>
    </el-dropdown-menu>
  </template>
</el-dropdown>
```

#### 2. 冒烟用例（直接点击切换）

```vue
<el-tag 
  :type="row.is_smoke ? 'success' : 'info'" 
  size="small" 
  style="cursor: pointer"
  @click="handleQuickUpdate(row, 'is_smoke', !row.is_smoke)"
>
  {{ row.is_smoke ? '是' : '否' }}
</el-tag>
```

#### 3. 快速更新函数

```javascript
const handleQuickUpdate = async (row, field, value) => {
  try {
    const updateData = { [field]: value }
    await partialUpdateTestcase(row.id, updateData)
    
    // 更新本地数据
    row[field] = value
    
    const fieldLabels = {
      priority: '优先级',
      status: '状态',
      is_smoke: '冒烟用例'
    }
    ElMessage.success(`${fieldLabels[field]}已更新`)
  } catch (error) {
    ElMessage.error('更新失败')
  }
}
```

### 后端支持

使用 Django REST Framework 的 `PATCH` 方法进行部分更新：

**API**: `PATCH /api/testcases/{id}/`

**请求体示例**:
```json
{
  "priority": "high"
}
```

或

```json
{
  "status": "active"
}
```

或

```json
{
  "is_smoke": true
}
```

---

## 用户体验优化

### 1. 视觉反馈
- ✅ 标签显示鼠标指针样式（`cursor: pointer`）
- ✅ 下拉菜单带有箭头图标提示
- ✅ 更新成功显示提示消息
- ✅ 更新失败显示错误消息

### 2. 交互流程
- ✅ 点击即更新，无需确认
- ✅ 本地数据立即更新，无需刷新页面
- ✅ 后台异步保存到数据库

### 3. 性能优化
- ✅ 使用 PATCH 部分更新，只传输修改的字段
- ✅ 本地数据立即更新，提升响应速度
- ✅ 异步请求，不阻塞用户操作

---

## 使用场景

### 场景1: 批量调整优先级
测试经理在评审测试用例时，可以快速调整多个用例的优先级，无需逐个打开编辑对话框。

### 场景2: 快速标记冒烟用例
测试人员在整理测试用例时，可以快速标记哪些是冒烟用例，一键切换。

### 场景3: 更新用例状态
当测试用例需要废弃或重新激活时，可以直接在列表中修改状态。

---

## 注意事项

1. **权限控制**: 确保用户有修改测试用例的权限
2. **数据一致性**: 更新失败时会显示错误提示，本地数据不会改变
3. **审计追踪**: 后端会自动记录修改人和修改时间

---

## 扩展建议

### 可以添加的其他快速操作
- 快速修改用例类型
- 快速分配创建人/修改人
- 批量快速更新（选中多条后统一修改）

---

**创建时间**: 2026-04-23  
**功能状态**: ✅ 已实现
