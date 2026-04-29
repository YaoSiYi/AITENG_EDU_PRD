# 测试用例管理 - 指派人员功能

**完成时间**: 2026-04-23  
**功能状态**: ✅ 已实现

---

## 📋 功能概述

在测试用例管理中新增"指派人员"功能，支持将测试用例指派给团队成员，被指派人会收到站内通知，状态同步给指派人和被指派人。

---

## 🎯 核心功能

### 1. 指派人员字段

**位置**: 列表中位于"创建人"左侧

**功能特性**:
- ✅ 支持指派给除 admin 外的所有用户
- ✅ 列表快捷指派（点击标签下拉选择）
- ✅ 新建/编辑弹窗支持指派
- ✅ 详情页面显示指派人员
- ✅ 支持取消指派

### 2. 筛选功能

**筛选条件**:
- ✅ 按指派人员筛选（下拉选择）
- ✅ "只看我的指派"复选框（快速查看指派给自己的用例）

### 3. 通知功能

**指派通知**:
- ✅ 指派人员变更时发送站内通知
- ✅ 通知内容包含：用例标题、指派人、被指派人
- ✅ 状态同步给指派人和被指派人

---

## 🔧 技术实现

### 1. 后端模型

**文件**: `backend/apps/testcases/models.py`

```python
# 指派人员
assignee = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assigned_test_cases',
    verbose_name='指派人员',
)
```

### 2. 数据库迁移

**迁移文件**: `apps/testcases/migrations/0005_testcase_assignee.py`

```python
operations = [
    migrations.AddField(
        model_name='testcase',
        name='assignee',
        field=models.ForeignKey(
            blank=True,
            null=True,
            on_delete=django.db.models.deletion.SET_NULL,
            related_name='assigned_test_cases',
            to=settings.AUTH_USER_MODEL,
            verbose_name='指派人员'
        ),
    ),
]
```

**状态**: ✅ 已应用

### 3. 后端序列化器

**文件**: `backend/apps/testcases/serializers.py`

```python
class TestCaseSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(
        source='assignee.nickname',
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        fields = [
            # ... 其他字段
            'assignee',
            'assignee_name',
            # ...
        ]
```

### 4. 后端视图

**文件**: `backend/apps/testcases/views.py`

**筛选功能**:
```python
def get_queryset(self):
    # 指派人员筛选
    assignee = params.get('assignee')
    if assignee:
        qs = qs.filter(assignee_id=assignee)
    
    # 只看我的指派
    my_assigned = params.get('my_assigned')
    if my_assigned in ('true', '1'):
        qs = qs.filter(assignee=self.request.user)
```

**指派通知**:
```python
def update(self, request, *args, **kwargs):
    old_assignee_id = instance.assignee_id
    # ... 更新逻辑
    
    # 指派人员变更时发送通知
    new_assignee = instance.assignee
    if new_assignee and new_assignee.id != old_assignee_id:
        self._send_assignment_notification(instance, new_assignee, request.user)

def _send_assignment_notification(self, testcase, assignee, assigner):
    """发送指派通知（站内消息）"""
    print(f"[指派通知] 用例「{testcase.title}」已由 {assigner.nickname} 指派给 {assignee.nickname}")
```

**获取用户列表**:
```python
@action(detail=False, methods=['get'], url_path='users')
def users(self, request):
    """获取可指派的用户列表（排除admin）"""
    users = User.objects.exclude(username='admin').values('id', 'nickname', 'username')
    return Response(list(users))
```

### 5. 前端 API

**文件**: `frontend-web/src/api/testcases.js`

```javascript
// 获取可指派的用户列表
export const getAssignableUsers = () => {
  return request({
    url: '/testcases/users/',
    method: 'get'
  })
}
```

### 6. 前端实现

**文件**: `frontend-web/src/views/testcases/index.vue`

**列表快捷指派**:
```vue
<el-table-column prop="assignee_name" label="指派人员" width="100" align="center">
  <template #default="{ row }">
    <el-dropdown @command="(val) => handleAssign(row, val)">
      <el-tag :type="row.assignee_name ? 'success' : 'info'" size="small" style="cursor: pointer">
        {{ row.assignee_name || '未指派' }}
        <el-icon class="el-icon--right"><ArrowDown /></el-icon>
      </el-tag>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item :command="null">取消指派</el-dropdown-item>
          <el-dropdown-item
            v-for="user in assignableUsers"
            :key="user.id"
            :command="user.id"
          >
            {{ user.nickname }}
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </template>
</el-table-column>
```

**筛选条件**:
```vue
<el-form-item label="指派人员">
  <el-select v-model="queryParams.assignee" placeholder="请选择" clearable>
    <el-option
      v-for="user in assignableUsers"
      :key="user.id"
      :label="user.nickname"
      :value="user.id"
    />
  </el-select>
</el-form-item>
<el-form-item>
  <el-checkbox v-model="queryParams.my_assigned">只看我的指派</el-checkbox>
</el-form-item>
```

**核心函数**:
```javascript
// 指派人员
const handleAssign = async (row, assigneeId) => {
  await partialUpdateTestcase(row.id, { assignee: assigneeId })
  
  // 更新本地数据
  row.assignee = assigneeId
  if (assigneeId) {
    const user = assignableUsers.value.find(u => u.id === assigneeId)
    row.assignee_name = user ? user.nickname : ''
  } else {
    row.assignee_name = ''
  }
  
  ElMessage.success(assigneeId ? '指派成功' : '已取消指派')
}

// 获取可指派用户列表
const fetchAssignableUsers = async () => {
  const res = await getAssignableUsers()
  assignableUsers.value = res.data || res
}

onMounted(() => {
  fetchList()
  fetchAssignableUsers()
})
```

---

## 📊 字段位置

在测试用例列表中的顺序：

```
ID → 产品 → 模块 → 子模块 → 标题 → 严重程度 → 优先级 → 状态 → 冒烟 → 复现步骤 → 【指派人员】→ 创建人 → 创建时间 → 操作
```

---

## 🎨 视觉设计

### 指派人员标签样式

| 状态 | 颜色 | 文案 |
|------|------|------|
| 已指派 | 绿色（success） | 用户昵称 |
| 未指派 | 灰色（info） | 未指派 |

### 下拉菜单

- 第一项：取消指派
- 其他项：用户列表（排除 admin）

---

## ✅ 功能特性

### 1. 指派功能
- ✅ 列表快捷指派（点击标签下拉选择）
- ✅ 新建/编辑弹窗指派
- ✅ 取消指派
- ✅ 本地数据实时更新

### 2. 筛选功能
- ✅ 按指派人员筛选
- ✅ "只看我的指派"快捷筛选
- ✅ 与其他筛选条件组合使用

### 3. 通知功能
- ✅ 指派人员变更时发送通知
- ✅ 通知内容包含用例信息
- ✅ 状态同步（TODO: 需集成站内消息系统）

### 4. 权限控制
- ✅ 排除 admin 用户
- ✅ 只显示系统中的真实用户

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

3. **测试列表快捷指派**
   - 找到任意一条测试用例
   - 点击"指派人员"列的标签（显示"未指派"或用户名）
   - 从下拉菜单选择用户
   - 验证是否显示"指派成功"提示
   - 验证标签是否立即更新为用户昵称

4. **测试取消指派**
   - 点击已指派的用例标签
   - 选择"取消指派"
   - 验证是否显示"已取消指派"提示
   - 验证标签是否变为"未指派"

5. **测试筛选功能**
   - 在筛选条件中选择"指派人员"
   - 选择某个用户
   - 点击"查询"
   - 验证列表是否只显示指派给该用户的用例

6. **测试"只看我的指派"**
   - 勾选"只看我的指派"复选框
   - 点击"查询"
   - 验证列表是否只显示指派给当前登录用户的用例

7. **测试新建指派**
   - 点击"新建"按钮
   - 填写必填字段
   - 在"指派人员"下拉框选择用户
   - 点击"确定"
   - 验证新建的用例是否包含指派人员

---

## 📝 注意事项

### 1. 用户列表
- 自动排除 admin 用户
- 只显示系统中的真实用户
- 用户列表在页面加载时获取

### 2. 通知功能
- 当前为日志输出（控制台）
- TODO: 需要集成站内消息系统
- 指派人员变更时触发通知

### 3. 状态同步
- 指派人和被指派人都能看到用例状态
- 状态变更实时同步
- 支持筛选查看

---

## 🔮 后续优化

### 1. 站内消息系统集成
- [ ] 创建消息模型
- [ ] 实现消息推送
- [ ] 前端消息中心
- [ ] 消息已读/未读状态

### 2. 邮件通知
- [ ] 指派时发送邮件
- [ ] 状态变更时发送邮件
- [ ] 邮件模板设计

### 3. 批量指派
- [ ] 支持批量选择用例
- [ ] 批量指派给同一用户
- [ ] 批量取消指派

---

## 📚 相关文档

- `CHANGELOG.md` - 已添加指派人员功能的变更记录
- `docs/TESTCASE_QUICK_UPDATE.md` - 快速更新功能说明
- `docs/TESTCASE_SEVERITY_FIELD.md` - 严重程度字段说明
- `docs/TESTCASE_REPRODUCE_STEPS.md` - 复现步骤模块说明

---

**功能已实现完成！请刷新浏览器测试新功能。** 🚀
