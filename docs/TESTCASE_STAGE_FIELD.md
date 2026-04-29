# 测试用例管理 - 阶段字段更新

**更新时间**: 2026-04-23  
**功能状态**: ✅ 已实现

---

## 📋 更新内容

### 字段替换

将"冒烟用例"（`is_smoke`）字段替换为"阶段"（`stage`）字段，提供更细粒度的测试阶段管理。

---

## 🎯 核心变更

### 1. 字段类型变更

**修改前**:
- 字段名：`is_smoke`
- 类型：布尔型（Boolean）
- 值：是/否

**修改后**:
- 字段名：`stage`
- 类型：枚举型（Enum）
- 值：冒烟测试/预发环境/生产环境/未设置

### 2. 阶段选项

| 值 | 标签 | 颜色 | 说明 |
|------|------|------|------|
| `smoke` | 冒烟测试 | 橙色（warning） | 基础功能验证 |
| `pre_prod` | 预发环境 | 蓝色（primary） | 预发布环境测试 |
| `production` | 生产环境 | 红色（danger） | 生产环境验证 |
| `null` | 未设置 | 灰色（info） | 未指定阶段 |

### 3. 列表快捷修改

- ✅ 点击阶段标签下拉选择
- ✅ 支持设置为"未设置"（清空）
- ✅ 实时保存（PATCH 部分更新）
- ✅ 本地数据立即更新

---

## 🔧 技术实现

### 1. 后端模型

**文件**: `backend/apps/testcases/models.py`

```python
class Stage(models.TextChoices):
    SMOKE = 'smoke', '冒烟测试'
    PRE_PROD = 'pre_prod', '预发环境'
    PRODUCTION = 'production', '生产环境'

stage = models.CharField(
    '阶段',
    max_length=20,
    choices=Stage.choices,
    blank=True,
    null=True,
)
```

### 2. 数据库迁移

**迁移文件**: `apps/testcases/migrations/0006_remove_testcase_is_smoke_testcase_stage.py`

```python
operations = [
    migrations.RemoveField(
        model_name='testcase',
        name='is_smoke',
    ),
    migrations.AddField(
        model_name='testcase',
        name='stage',
        field=models.CharField(
            blank=True,
            choices=[
                ('smoke', '冒烟测试'),
                ('pre_prod', '预发环境'),
                ('production', '生产环境')
            ],
            max_length=20,
            null=True,
            verbose_name='阶段'
        ),
    ),
]
```

**状态**: ✅ 已应用

### 3. 后端序列化器

**文件**: `backend/apps/testcases/serializers.py`

- 已将所有 `is_smoke` 替换为 `stage`

### 4. 后端 Admin

**文件**: `backend/apps/testcases/admin.py`

```python
@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['public_id', 'title', 'product', 'module', 'priority', 'status', 'stage', 'creator', 'created_at']
    list_filter = ['priority', 'status', 'stage', 'product', 'module']
    fieldsets = (
        # ...
        ('属性', {
            'fields': ('priority', 'status', 'stage', 'case_type', 'remark')
        }),
        # ...
    )
```

### 5. 前端实现

**文件**: `frontend-web/src/views/testcases/index.vue`

**列表列**:
```vue
<el-table-column prop="stage" label="阶段" width="110" align="center">
  <template #default="{ row }">
    <el-dropdown @command="(val) => handleQuickUpdate(row, 'stage', val)">
      <el-tag :type="getStageType(row.stage)" size="small" style="cursor: pointer">
        {{ getStageLabel(row.stage) }}
        <el-icon class="el-icon--right"><ArrowDown /></el-icon>
      </el-tag>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item :command="null">未设置</el-dropdown-item>
          <el-dropdown-item command="smoke">冒烟测试</el-dropdown-item>
          <el-dropdown-item command="pre_prod">预发环境</el-dropdown-item>
          <el-dropdown-item command="production">生产环境</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </template>
</el-table-column>
```

**新建/编辑弹窗**:
```vue
<el-form-item label="阶段">
  <el-select v-model="formData.stage" placeholder="请选择" clearable>
    <el-option label="冒烟测试" value="smoke" />
    <el-option label="预发环境" value="pre_prod" />
    <el-option label="生产环境" value="production" />
  </el-select>
</el-form-item>
```

**工具函数**:
```javascript
const getStageType = (stage) => {
  const map = { smoke: 'warning', pre_prod: 'primary', production: 'success' }
  return map[stage] || 'info'
}

const getStageLabel = (stage) => {
  const map = { smoke: '冒烟测试', pre_prod: '预发环境', production: '生产环境' }
  return map[stage] || '未设置'
}
```

---

## 📊 字段位置

在测试用例列表中的顺序：

```
ID → 产品 → 模块 → 子模块 → 标题 → 严重程度 → 优先级 → 状态 → 【阶段】→ 复现步骤 → 指派人员 → 创建人 → 创建时间 → 操作
```

---

## 🎨 视觉效果

### 阶段标签样式

| 阶段 | 颜色 | 标签类型 |
|------|------|----------|
| 冒烟测试 | 橙色 | warning |
| 预发环境 | 蓝色 | primary |
| 生产环境 | 红色 | danger |
| 未设置 | 灰色 | info |

### 下拉菜单
- 第一项：未设置（清空阶段）
- 其他项：冒烟测试、预发环境、生产环境

---

## ✅ 完成清单

- [x] 后端模型新增 `Stage` 枚举类
- [x] 后端模型新增 `stage` 字段
- [x] 后端模型删除 `is_smoke` 字段
- [x] 数据库迁移已创建并应用
- [x] 后端序列化器已更新（2个）
- [x] 后端 Admin 已更新
- [x] 前端列表列已更新（带快捷修改）
- [x] 前端新建/编辑弹窗已更新
- [x] 前端详情对话框已更新
- [x] 前端工具函数已添加（2个）
- [x] CHANGELOG 已更新
- [x] 功能说明文档已创建
- [ ] **浏览器已刷新**（请你操作）
- [ ] **功能已测试**（请你验证）

---

## 🚀 测试步骤

### 1. 刷新浏览器
```
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

### 2. 访问测试用例管理
```
http://localhost:3000/testcases
```

### 3. 测试列表快捷修改
- 找到任意一条测试用例
- 点击"阶段"列的标签（显示"未设置"或阶段名称）
- 从下拉菜单选择阶段
- 验证是否立即更新

### 4. 测试新建用例
- 点击"新建"按钮
- 填写必填字段
- 在"阶段"下拉框选择阶段
- 点击"确定"
- 验证新建的用例是否包含阶段信息

### 5. 测试清空阶段
- 点击已设置阶段的用例标签
- 选择"未设置"
- 验证是否变为"未设置"状态

---

## 📝 注意事项

### 1. 数据兼容性
- 旧的 `is_smoke` 字段已删除
- 新的 `stage` 字段默认为 `null`（未设置）
- 已有数据的 `is_smoke` 值已丢失，需要重新设置阶段

### 2. API 变更
- 请求参数：使用 `stage` 替代 `is_smoke`
- 响应数据：返回 `stage` 字段（枚举值）

### 3. 前端兼容
- 已移除所有 `is_smoke` 相关代码
- 新增 `stage` 相关工具函数
- 表单数据结构已更新

---

**功能已实现完成！请刷新浏览器测试新功能。** 🚀
