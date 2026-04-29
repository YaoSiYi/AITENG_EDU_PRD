# ✅ 测试用例管理 - 复现步骤模块完成

**完成时间**: 2026-04-23  
**功能状态**: ✅ 已实现

---

## 📋 功能概述

在测试用例管理中新增"复现步骤"模块，支持文字和图片混合添加，位于"冒烟"字段右侧。

---

## 🎯 核心功能

### 1. 支持内容类型
- ✅ **文字步骤** - 多行文本输入
- ✅ **图片步骤** - 支持拖拽上传或点击上传

### 2. 图片规格
- **支持格式**: JPG, PNG, GIF, WEBP, BMP
- **最大分辨率**: 2048 x 1280
- **存储方式**: Base64 编码（存储在 JSON 字段中）

### 3. 交互特性
- ✅ 添加文字/图片步骤
- ✅ 删除步骤
- ✅ 上移/下移步骤（调整顺序）
- ✅ 缩略图预览（200x150px）
- ✅ 鼠标悬停自动放大
- ✅ 点击任意位置关闭放大图

---

## 🔧 技术实现

### 1. 后端模型

**文件**: `backend/apps/testcases/models.py`

```python
reproduce_steps = models.JSONField(
    '复现步骤',
    default=list,
    blank=True,
    help_text='包含文字和图片的复现步骤'
)
```

**数据结构**:
```json
[
  {
    "type": "text",
    "content": "步骤描述文字"
  },
  {
    "type": "image",
    "content": "data:image/png;base64,iVBORw0KGgo..."
  }
]
```

### 2. 数据库迁移

- 迁移文件：`apps/testcases/migrations/0004_testcase_reproduce_steps.py`
- 状态：✅ 已应用

### 3. 后端序列化器

**文件**: `backend/apps/testcases/serializers.py`

- `TestCaseSerializer` 新增 `reproduce_steps` 字段
- `TestCaseCreateUpdateSerializer` 新增 `reproduce_steps` 字段

### 4. 前端实现

**文件**: `frontend-web/src/views/testcases/index.vue`

#### 4.1 列表列
```vue
<el-table-column prop="reproduce_steps" label="复现步骤" width="100" align="center">
  <template #default="{ row }">
    <el-button
      v-if="row.reproduce_steps && row.reproduce_steps.length > 0"
      type="primary"
      link
      size="small"
      @click="handleViewReproduceSteps(row)"
    >
      查看({{ row.reproduce_steps.length }})
    </el-button>
    <span v-else style="color: #909399">-</span>
  </template>
</el-table-column>
```

#### 4.2 编辑器（新建/编辑弹窗）
```vue
<el-form-item label="复现步骤">
  <div class="reproduce-steps-editor">
    <el-button type="primary" size="small" @click="addReproduceStep('text')">
      添加文字
    </el-button>
    <el-button type="success" size="small" @click="addReproduceStep('image')">
      添加图片
    </el-button>
    
    <!-- 步骤列表 -->
    <div v-for="(step, index) in formData.reproduce_steps" :key="index">
      <!-- 文字步骤 -->
      <el-input v-if="step.type === 'text'" type="textarea" />
      
      <!-- 图片步骤 -->
      <el-upload v-else-if="step.type === 'image'" />
    </div>
  </div>
</el-form-item>
```

#### 4.3 查看对话框
```vue
<el-dialog v-model="reproduceStepsVisible" title="复现步骤">
  <div class="reproduce-steps-viewer">
    <div v-for="(step, index) in currentReproduceSteps" :key="index">
      <!-- 文字内容 -->
      <div v-if="step.type === 'text'">{{ step.content }}</div>
      
      <!-- 图片内容（缩略图） -->
      <img
        v-else-if="step.type === 'image'"
        :src="step.content"
        class="step-thumbnail"
        @mouseenter="enlargedImage = step.content"
        @mouseleave="enlargedImage = null"
      />
    </div>
  </div>
</el-dialog>

<!-- 图片放大查看 -->
<div v-if="enlargedImage" class="image-overlay" @click="enlargedImage = null">
  <img :src="enlargedImage" class="enlarged-image" />
</div>
```

#### 4.4 核心函数

```javascript
// 添加步骤
const addReproduceStep = (type) => {
  formData.reproduce_steps.push({ type, content: '' })
}

// 删除步骤
const removeReproduceStep = (index) => {
  formData.reproduce_steps.splice(index, 1)
}

// 上移步骤
const moveStepUp = (index) => {
  if (index > 0) {
    const temp = formData.reproduce_steps[index]
    formData.reproduce_steps[index] = formData.reproduce_steps[index - 1]
    formData.reproduce_steps[index - 1] = temp
  }
}

// 下移步骤
const moveStepDown = (index) => {
  if (index < formData.reproduce_steps.length - 1) {
    const temp = formData.reproduce_steps[index]
    formData.reproduce_steps[index] = formData.reproduce_steps[index + 1]
    formData.reproduce_steps[index + 1] = temp
  }
}

// 处理图片上传
const handleImageChange = (file, index) => {
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
      formData.reproduce_steps[index].content = e.target.result
    }
  }

  reader.readAsDataURL(file.raw)
}

// 查看复现步骤
const handleViewReproduceSteps = (row) => {
  currentReproduceSteps.value = row.reproduce_steps || []
  reproduceStepsVisible.value = true
}
```

---

## 🎨 样式设计

### 1. 编辑器样式
- 步骤卡片：浅灰背景 + 边框
- 步骤编号：蓝色高亮
- 操作按钮：上移/下移/删除
- 图片上传区：拖拽区域 + 提示文字

### 2. 查看器样式
- 缩略图：最大 200x150px
- 悬停效果：轻微放大（scale 1.05）
- 放大图：黑色半透明遮罩 + 居中显示
- 最大尺寸：90vw x 90vh

### 3. 响应式设计
- 移动端：缩略图自适应
- 桌面端：放大图最大化显示

---

## 📊 字段位置

在测试用例列表中的顺序：

```
ID → 产品 → 模块 → 子模块 → 标题 → 严重程度 → 优先级 → 状态 → 冒烟 → 【复现步骤】→ 创建人 → 创建时间 → 操作
```

---

## ✅ 功能特性

### 1. 编辑功能
- ✅ 添加文字步骤
- ✅ 添加图片步骤
- ✅ 删除步骤
- ✅ 调整步骤顺序（上移/下移）
- ✅ 图片分辨率验证
- ✅ 图片格式验证

### 2. 查看功能
- ✅ 列表显示步骤数量
- ✅ 点击查看详细步骤
- ✅ 缩略图预览
- ✅ 鼠标悬停放大
- ✅ 点击关闭放大图

### 3. 存储方式
- ✅ JSON 格式存储
- ✅ Base64 编码图片
- ✅ 支持多步骤
- ✅ 保持步骤顺序

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

3. **测试新建功能**
   - 点击"新建"按钮
   - 填写必填字段（标题）
   - 在"复现步骤"区域点击"添加文字"
   - 输入步骤描述
   - 点击"添加图片"
   - 上传一张图片（测试分辨率验证）
   - 调整步骤顺序（上移/下移）
   - 点击"确定"保存

4. **测试查看功能**
   - 在列表中找到刚创建的测试用例
   - 点击"复现步骤"列的"查看(2)"按钮
   - 查看步骤详情
   - 鼠标悬停在图片上，观察放大效果
   - 点击任意位置关闭放大图

5. **测试编辑功能**
   - 点击"编辑"按钮
   - 修改复现步骤
   - 删除某个步骤
   - 保存修改

---

## 📝 注意事项

### 1. 图片大小限制
- 分辨率：最大 2048x1280
- 文件大小：建议不超过 2MB（Base64 编码后会增大约 33%）
- 过大的图片会导致数据库存储压力

### 2. 性能考虑
- Base64 编码会增大数据量
- 建议每个测试用例的复现步骤不超过 10 个
- 图片步骤不超过 5 个

### 3. 浏览器兼容性
- 现代浏览器均支持
- IE11 可能存在兼容性问题

---

## 📚 相关文档

- `CHANGELOG.md` - 已添加复现步骤模块的变更记录
- `docs/TESTCASE_SEVERITY_FIELD.md` - 严重程度字段说明
- `docs/TESTCASE_QUICK_UPDATE.md` - 快速更新功能说明

---

**功能已实现完成！请刷新浏览器测试新功能。** 🚀
