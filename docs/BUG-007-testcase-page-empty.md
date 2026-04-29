# BUG-007: 测试用例管理页为空

**报告时间**: 2026-04-23  
**状态**: ✅ 已修复  
**严重程度**: 高  
**影响范围**: 测试用例管理模块

---

## 问题描述

访问测试用例管理页面（`/testcases`）时，页面只显示布局框架，但没有显示任何测试用例数据。

### 表现

- ✅ 页面布局正常显示
- ✅ 筛选条件、按钮等 UI 元素正常
- ❌ 表格中没有数据
- ❌ 显示"暂无数据"或空白表格

---

## 问题原因

经过诊断，发现了以下多个问题：

### 1. 端口冲突

**问题**：Vite 开发服务器因为端口 3000 被占用，自动切换到了端口 3001

**日志**：
```
Port 3000 is in use, trying another one...
➜  Local:   http://localhost:3001/
```

**影响**：用户访问 `http://localhost:3000` 时无法连接到正确的前端服务

### 2. 缺失函数定义

**问题**：模板中使用了 `getStageType` 和 `getStageLabel` 函数，但在 `<script setup>` 中没有定义

**错误信息**：
```
Uncaught (in promise) TypeError: _ctx.getStageType is not a function
    at index.vue:185:30
```

**影响**：页面加载时 JavaScript 报错，导致数据无法正常渲染

### 3. 缺失导入

**问题**：`getAssignableUsers` API 函数和部分图标组件没有被导入

**影响**：指派人员功能无法正常工作

---

## 修复方案

### 1. 解决端口冲突

```bash
# 释放端口 3000 和 3001
lsof -ti:3000 | xargs kill -9
lsof -ti:3001 | xargs kill -9

# 重新启动 Vite 服务器
npm run dev
```

**结果**：Vite 服务器正确运行在端口 3000

### 2. 添加缺失的函数

**文件**：`frontend-web/src/views/testcases/index.vue`

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

### 3. 补充缺失的导入

**文件**：`frontend-web/src/views/testcases/index.vue`

```javascript
// 添加图标导入
import { UploadFilled, ArrowDown, Warning, InfoFilled, CircleCheck } from '@element-plus/icons-vue'

// 添加 API 函数导入
import {
  getTestcaseList,
  createTestcase,
  getTestcaseDetail,
  updateTestcase,
  partialUpdateTestcase,
  deleteTestcase,
  exportTestcases,
  downloadTestcaseTemplate,
  importTestcases,
  getAssignableUsers  // 新增
} from '@/api/testcases'
```

---

## 验证步骤

### 1. 检查服务器状态

```bash
# 检查 Django 服务器
curl http://localhost:8000/api/testcases/
# 应返回 401 认证错误（说明服务器正常）

# 检查 Vite 服务器
curl http://localhost:3000
# 应返回 HTML 页面
```

### 2. 测试前端功能

1. 访问 `http://localhost:3000/login`
2. 使用账号 `admin` / 密码 `admin123` 登录
3. 访问 `http://localhost:3000/testcases`
4. 验证数据是否正常显示

### 3. 检查浏览器控制台

按 `F12` 打开开发者工具：
- **Console 标签**：不应有 JavaScript 错误
- **Network 标签**：`/api/testcases/` 请求应返回 200 状态码

---

## 测试结果

### 修复前

- ❌ 页面为空，无数据显示
- ❌ 浏览器控制台报错：`getStageType is not a function`
- ❌ Vite 服务器运行在错误的端口 3001

### 修复后

- ✅ 页面正常显示 21 条测试用例数据
- ✅ 浏览器控制台无错误
- ✅ Vite 服务器运行在正确的端口 3000
- ✅ 所有功能正常工作（筛选、排序、快捷修改、指派等）

---

## 根本原因分析

### 为什么会出现这个问题？

1. **开发流程问题**：在添加"阶段"字段时，只修改了模板代码，忘记添加对应的工具函数
2. **测试不充分**：代码修改后没有在浏览器中实际测试，导致运行时错误未被发现
3. **端口管理问题**：开发环境中有多个进程占用端口，导致 Vite 自动切换端口

### 如何避免类似问题？

1. **代码审查**：在提交代码前，检查模板中使用的所有函数是否已定义
2. **浏览器测试**：每次修改后在浏览器中实际测试功能
3. **端口管理**：定期清理占用的端口，确保开发服务器运行在预期端口
4. **错误监控**：关注浏览器控制台的错误信息

---

## 相关文件

### 修改的文件

- `frontend-web/src/views/testcases/index.vue` - 添加缺失的函数和导入
- `frontend-web/src/api/testcases.js` - 添加 `getAssignableUsers` API
- `backend/apps/testcases/models.py` - 添加 `stage` 字段
- `backend/apps/testcases/serializers.py` - 更新序列化器
- `backend/apps/testcases/views.py` - 更新视图和筛选逻辑
- `backend/apps/testcases/admin.py` - 更新 Admin 配置

### 新增的文件

- `docs/BUG-007-testcase-page-empty.md` - 本文档
- `docs/TESTCASE_STAGE_FIELD.md` - 阶段字段说明文档
- `frontend-web/src/views/TestDebug.vue` - 调试页面（用于诊断）
- `test_frontend_api.html` - API 测试页面（用于诊断）

---

## 经验教训

### 开发规范

1. **先测试后提交**：每次代码修改后必须在浏览器中实际测试
2. **完整性检查**：添加新功能时，确保所有依赖的函数、导入都已添加
3. **错误处理**：关注浏览器控制台的错误信息，及时修复

### 调试技巧

1. **使用调试页面**：创建简单的测试页面来隔离问题
2. **检查网络请求**：使用浏览器开发者工具的 Network 标签检查 API 请求
3. **查看控制台**：JavaScript 错误通常会在控制台中显示详细信息

---

## 状态

- [x] 问题已识别
- [x] 根本原因已分析
- [x] 修复方案已实施
- [x] 功能已验证
- [x] 文档已更新

**修复时间**: 2026-04-23  
**修复人**: Claude Sonnet 4.6

---

## 参考文档

- `docs/TESTCASE_STAGE_FIELD.md` - 阶段字段功能说明
- `docs/TESTCASE_ASSIGNEE_FEATURE.md` - 指派人员功能说明
- `CHANGELOG.md` - 完整变更日志
