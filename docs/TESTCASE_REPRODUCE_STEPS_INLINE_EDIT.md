# 测试用例复现步骤 - 主页面实时编辑功能

**更新时间**: 2026-04-23  
**功能状态**: ✅ 已实现

---

## 📋 功能概述

在测试用例管理列表中，可以直接点击"复现步骤"列的"编辑"或"添加"按钮，在弹窗中实时编辑复现步骤，无需进入完整的编辑表单。

---

## 🎯 核心功能

### 1. 主页面快捷入口

**列表列显示**：
- 有步骤：显示"编辑(N)"按钮（N为步骤数量）
- 无步骤：显示"添加"按钮

### 2. 独立编辑对话框

**功能特性**：
- ✅ 独立的编辑对话框（不影响其他字段）
- ✅ 完整的编辑功能（添加/删除/排序）
- ✅ 支持文字和图片步骤
- ✅ 图片分辨率验证
- ✅ 实时保存到数据库
- ✅ 本地数据立即更新

### 3. 操作流程

```
点击"编辑(N)"或"添加" 
    ↓
打开编辑对话框
    ↓
添加/修改/删除步骤
    ↓
点击"保存"
    ↓
PATCH 请求更新数据库
    ↓
列表数据实时更新
```

---

## 🔧 技术实现

### 1. 列表列更新

**文件**: `frontend-web/src/views/testcases/index.vue`

```vue
<el-table-column prop="reproduce_steps" label="复现步骤" width="120" align="center">
  <template #default="{ row }">
    <el-button
      type="primary"
      link
      size="small"
      @click="handleEditReproduceSteps(row)"
    >
      <span v-if="row.reproduce_steps && row.reproduce_steps.length > 0">
        编辑({{ row.reproduce_steps.length }})
      </span>
      <span v-else>添加</span>
    </el-button>
  </template>
</el-table-column>
```

### 2. 编辑对话框

```vue
<el-dialog v-model="reproduceStepsEditVisible" title="编辑复现步骤" width="700px">
  <div class="reproduce-steps-editor">
    <!-- 添加按钮 -->
    <el-button type="primary" size="small" @click="addEditingStep('text')">
      添加文字
    </el-button>
    <el-button type="success" size="small" @click="addEditingStep('image')">
      添加图片
    </el-button>
    
    <!-- 步骤列表 -->
    <div v-for="(step, index) in editingReproduceSteps" :key="index">
      <!-- 步骤编辑器 -->
    </div>
  </div>
  <template #footer>
    <el-button @click="reproduceStepsEditVisible = false">取消</el-button>
    <el-button type="primary" @click="saveReproduceSteps">保存</el-button>
  </template>
</el-dialog>
```

### 3. 核心函数

```javascript
// 打开编辑对话框
const handleEditReproduceSteps = (row) => {
  currentEditingRow.value = row
  // 深拷贝，避免直接修改原数据
  editingReproduceSteps.value = JSON.parse(JSON.stringify(row.reproduce_steps || []))
  reproduceStepsEditVisible.value = true
}

// 保存复现步骤
const saveReproduceSteps = async () => {
  if (!currentEditingRow.value) return

  try {
    // PATCH 请求，只更新 reproduce_steps 字段
    await partialUpdateTestcase(currentEditingRow.value.id, {
      reproduce_steps: editingReproduceSteps.value
    })

    // 更新本地数据
    currentEditingRow.value.reproduce_steps = editingReproduceSteps.value

    reproduceStepsEditVisible.value = false
    ElMessage.success('复现步骤已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 添加步骤
const addEditingStep = (type) => {
  editingReproduceSteps.value.push({ type, content: '' })
}

// 删除步骤
const removeEditingStep = (index) => {
  editingReproduceSteps.value.splice(index, 1)
}

// 上移步骤
const moveEditingStepUp = (index) => {
  if (index > 0) {
    const temp = editingReproduceSteps.value[index]
    editingReproduceSteps.value[index] = editingReproduceSteps.value[index - 1]
    editingReproduceSteps.value[index - 1] = temp
  }
}

// 下移步骤
const moveEditingStepDown = (index) => {
  if (index < editingReproduceSteps.value.length - 1) {
    const temp = editingReproduceSteps.value[index]
    editingReproduceSteps.value[index] = editingReproduceSteps.value[index + 1]
    editingReproduceSteps.value[index + 1] = temp
  }
}

// 处理图片上传
const handleEditingImageChange = (file, index) => {
  const reader = new FileReader()
  const img = new Image()

  reader.onload = (e) => {
    img.src = e.target.result
    img.onload = () => {
      // 检查分辨率
      if (img.width > 2048 || img.height > 1280) {
        ElMessage.warning(`图片分辨率过大（${img.width}x${img.height}），最大支持 2048x1280`)
        return
      }
      // 保存 base64 图片
      editingReproduceSteps.value[index].content = e.target.result
    }
  }

  reader.readAsDataURL(file.raw)
}
```

---

## 🎨 用户体验优化

### 1. 快捷入口
- 列表中直接显示"编辑"或"添加"按钮
- 一键打开编辑对话框
- 无需进入完整编辑表单

### 2. 独立编辑
- 只编辑复现步骤，不影响其他字段
- 编辑过程中可以取消，不会影响原数据
- 保存后立即更新列表显示

### 3. 视觉反馈
- 按钮显示步骤数量
- 保存成功显示提示消息
- 保存失败显示错误提示

---

## 📊 对比：编辑方式

| 编辑方式 | 入口 | 优点 | 适用场景 |
|----------|------|------|----------|
| 主页面实时编辑 | 列表"编辑"按钮 | 快速、专注、不影响其他字段 | 只需修改复现步骤 |
| 完整编辑表单 | 列表"编辑"按钮 | 可同时修改所有字段 | 需要修改多个字段 |

---

## ✅ 功能特性

### 1. 编辑功能
- ✅ 添加文字步骤
- ✅ 添加图片步骤
- ✅ 删除步骤
- ✅ 调整步骤顺序（上移/下移）
- ✅ 图片分辨率验证
- ✅ 图片格式验证

### 2. 保存机制
- ✅ PATCH 部分更新（只更新 reproduce_steps 字段）
- ✅ 本地数据立即更新
- ✅ 成功/失败提示
- ✅ 取消操作不影响原数据

### 3. 数据安全
- ✅ 深拷贝编辑数据，避免直接修改原数据
- ✅ 取消操作丢弃修改
- ✅ 保存失败不影响原数据

---

## 🚀 使用方法

### 测试步骤

1. **刷新浏览器**
   ```
   Ctrl + Shift + R (Windows/Linux)
   Cmd + Shift + R (Mac)
   ```

2. **访问测试用例管理**
   ```
   http://localhost:3000/testcases
   ```

3. **测试实时编辑**
   - 找到任意一条测试用例
   - 点击"复现步骤"列的"编辑(N)"或"添加"按钮
   - 在弹窗中添加/修改步骤
   - 点击"保存"
   - 验证列表中的步骤数量是否更新

4. **测试取消操作**
   - 点击"编辑"按钮
   - 修改步骤
   - 点击"取消"
   - 验证原数据是否保持不变

---

## 📝 注意事项

### 1. 数据一致性
- 编辑时使用深拷贝，避免直接修改原数据
- 取消操作丢弃所有修改
- 保存成功后才更新本地数据

### 2. 性能考虑
- 使用 PATCH 部分更新，只传输修改的字段
- 本地数据立即更新，无需重新加载列表

### 3. 用户体验
- 按钮文案清晰（"编辑(N)" / "添加"）
- 保存成功显示提示消息
- 保存失败显示错误提示

---

## 📚 相关文档

- `docs/TESTCASE_REPRODUCE_STEPS.md` - 复现步骤模块完整说明
- `docs/TESTCASE_QUICK_UPDATE.md` - 快速更新功能说明
- `CHANGELOG.md` - 变更日志

---

**功能已实现完成！请刷新浏览器测试新功能。** 🚀
