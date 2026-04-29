# BUG-006: 测试用例状态缺少“已关闭”

**日期**: 2026-04-23  
**严重程度**: 🟢 Low  
**状态**: ✅ 已解决  
**影响范围**: 测试用例管理状态流转

---

## 问题现象

测试用例管理中，状态仅包含：
- 草稿（draft）
- 有效（active）
- 已废弃（deprecated）

缺少“已关闭（closed）”状态，无法表达已完成并关闭的用例状态。

---

## 修复内容

### 1) 后端模型新增状态枚举

**文件**: `backend/apps/testcases/models.py`

```python
class Status(models.TextChoices):
    DRAFT = 'draft', '草稿'
    ACTIVE = 'active', '有效'
    DEPRECATED = 'deprecated', '已废弃'
    CLOSED = 'closed', '已关闭'
```

### 2) 数据库迁移

- 生成迁移: `apps/testcases/migrations/0002_alter_testcase_status.py`
- 执行迁移: `python manage.py migrate testcases`

### 3) 前端同步更新

**文件**: `frontend-web/src/views/testcases/index.vue`

- 筛选状态下拉新增：`已关闭`
- 列表状态快捷下拉新增：`已关闭`
- 新建/编辑弹窗状态下拉新增：`已关闭`
- 状态标签样式新增：`closed -> danger`
- 状态文案新增：`closed -> 已关闭`

---

## 验证结果

- ✅ 后端可保存 `closed` 状态
- ✅ 前端筛选可选择“已关闭”
- ✅ 前端编辑可设置“已关闭”
- ✅ 列表快捷修改支持“已关闭”
- ✅ 标签正确显示“已关闭”且样式为红色（danger）

---

**修复人**: Claude Sonnet 4.6  
**最后更新**: 2026-04-23
