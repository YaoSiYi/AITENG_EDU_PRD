# 时间格式统一更新

**更新时间**: 2026-04-23  
**状态**: ✅ 已完成

---

## 📋 更新内容

### 统一时间格式

所有模块的时间显示统一为标准格式：**YYYY-MM-DD HH:mm:ss**

例如：`2026-04-23 14:30:00`

---

## 🔧 技术实现

### 1. 创建全局时间格式化工具

**文件**: `frontend-web/src/utils/datetime.js`

```javascript
/**
 * 格式化日期时间
 * @param {string|Date} dateTime - 日期时间字符串或 Date 对象
 * @param {string} format - 格式化模板，默认 'YYYY-MM-DD HH:mm:ss'
 * @returns {string} 格式化后的时间字符串
 */
export function formatDateTime(dateTime, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!dateTime) return '-'

  const date = new Date(dateTime)
  
  // 检查日期是否有效
  if (isNaN(date.getTime())) return '-'

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}
```

### 2. 更新的页面

| 页面 | 更新内容 | 字段 |
|------|----------|------|
| **测试用例管理** | 列表创建时间、详情创建/更新时间 | `created_at`, `updated_at` |
| **个人中心** | 最近活动时间 | `activity.time` |
| **活动中心** | 活动开始/结束时间 | `startDate`, `endDate` |

### 3. 使用方式

**在 Vue 组件中**：

```vue
<script setup>
import { formatDateTime } from '@/utils/datetime'
</script>

<template>
  <!-- 显示完整日期时间 -->
  <span>{{ formatDateTime(row.created_at) }}</span>
  
  <!-- 显示日期（不含时间） -->
  <span>{{ formatDate(row.created_at) }}</span>
  
  <!-- 显示时间（不含日期） -->
  <span>{{ formatTime(row.created_at) }}</span>
</template>
```

---

## 📊 更新统计

| 文件 | 更新内容 |
|------|----------|
| `utils/datetime.js` | ✅ 新增时间格式化工具 |
| `views/testcases/index.vue` | ✅ 列表和详情时间格式化 |
| `views/Profile.vue` | ✅ 最近活动时间格式化 |
| `views/Activities.vue` | ✅ 活动日期格式化 |

---

## ✅ 格式化效果

### 修改前
- `2024-04-22T14:30:00Z`
- `2小时前`
- `2024-04-22`

### 修改后
- `2026-04-23 14:30:00` ✅
- `2026-04-23 14:30:00` ✅
- `2026-04-23 14:30:00` ✅

---

## 🎯 工具函数说明

### formatDateTime(dateTime, format)
- **功能**: 格式化日期时间
- **参数**: 
  - `dateTime`: 日期时间字符串或 Date 对象
  - `format`: 格式化模板（默认 'YYYY-MM-DD HH:mm:ss'）
- **返回**: 格式化后的时间字符串
- **示例**: `formatDateTime('2026-04-23T14:30:00Z')` → `'2026-04-23 14:30:00'`

### formatDate(dateTime)
- **功能**: 格式化日期（不含时间）
- **返回**: `YYYY-MM-DD` 格式
- **示例**: `formatDate('2026-04-23T14:30:00Z')` → `'2026-04-23'`

### formatTime(dateTime)
- **功能**: 格式化时间（不含日期）
- **返回**: `HH:mm:ss` 格式
- **示例**: `formatTime('2026-04-23T14:30:00Z')` → `'14:30:00'`

### formatRelativeTime(dateTime)
- **功能**: 获取相对时间描述
- **返回**: `刚刚`、`5分钟前`、`2小时前` 等
- **示例**: `formatRelativeTime(new Date())` → `'刚刚'`

---

## 📝 注意事项

### 1. 时区处理
- 工具函数使用本地时区
- 后端返回的 UTC 时间会自动转换为本地时间

### 2. 空值处理
- 如果传入 `null`、`undefined` 或无效日期，返回 `'-'`

### 3. 兼容性
- 支持字符串和 Date 对象
- 支持 ISO 8601 格式（`2026-04-23T14:30:00Z`）
- 支持时间戳（`1713878400000`）

---

## 🚀 使用建议

### 1. 列表显示
使用完整格式 `YYYY-MM-DD HH:mm:ss`：
```vue
<el-table-column label="创建时间">
  <template #default="{ row }">
    {{ formatDateTime(row.created_at) }}
  </template>
</el-table-column>
```

### 2. 详情页面
使用完整格式 `YYYY-MM-DD HH:mm:ss`：
```vue
<el-descriptions-item label="创建时间">
  {{ formatDateTime(detail.created_at) }}
</el-descriptions-item>
```

### 3. 动态列表（如最近活动）
可选择使用相对时间或完整格式：
```vue
<!-- 相对时间 -->
<span>{{ formatRelativeTime(activity.time) }}</span>

<!-- 完整格式 -->
<span>{{ formatDateTime(activity.time) }}</span>
```

---

## 📚 相关文档

- `CHANGELOG.md` - 变更日志
- `README.md` - 项目文档

---

**时间格式统一更新完成！** ✅
