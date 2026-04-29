# 个人中心密码修改功能文档

## 功能概述

在个人中心的设置页面新增密码修改模块，支持用户修改登录密码，包含完整的验证流程和安全机制。

---

## 功能详情

### 1. 密码修改表单

**位置**：个人中心 → 设置 → 修改密码

**表单字段**：
1. **原始密码**：验证用户身份
2. **新密码**：设置新的登录密码（6-20位）
3. **确认新密码**：确保新密码输入正确

### 2. 验证规则

#### 原始密码验证
- ✅ 必填项
- ✅ 与数据库中的密码匹配
- ❌ 不匹配时提示"原始密码不正确"

#### 新密码验证
- ✅ 必填项
- ✅ 长度为 6-20 位字符
- ✅ 不能与原始密码相同
- ❌ 长度不符时提示"密码长度为 6-20 位字符"
- ❌ 与原密码相同时提示"新密码不能与原始密码相同"

#### 确认密码验证
- ✅ 必填项
- ✅ 必须与新密码一致
- ❌ 不一致时提示"两次输入的密码不一致"

### 3. 安全机制

#### 实时验证
- 输入框失去焦点时自动验证
- 验证失败时输入框下方显示错误提示
- 验证通过时清除错误提示

#### 二次确认
- 点击"修改密码"按钮后弹出确认对话框
- 提示"修改密码后需要重新登录，确定要继续吗？"
- 用户可以取消操作

#### 自动退出
- 密码修改成功后显示提示"密码修改成功，请重新登录"
- 1.5秒后自动退出登录
- 跳转到登录页面

---

## 技术实现

### 前端实现

#### 1. 表单状态管理

```javascript
// 密码修改表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 表单引用
const passwordFormRef = ref(null)
```

#### 2. 验证规则

```javascript
const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原始密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为 6-20 位字符', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value === passwordForm.value.oldPassword) {
          callback(new Error('新密码不能与原始密码相同'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}
```

#### 3. 修改密码函数

```javascript
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    // 1. 验证表单
    await passwordFormRef.value.validate()

    // 2. 二次确认
    await ElMessageBox.confirm(
      '修改密码后需要重新登录，确定要继续吗？',
      '确认修改密码',
      {
        confirmButtonText: '确定修改',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 3. 调用 API
    const response = await fetch('/api/users/change-password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        old_password: passwordForm.value.oldPassword,
        new_password: passwordForm.value.newPassword
      })
    })

    const data = await response.json()

    if (response.ok) {
      ElMessage.success('密码修改成功，请重新登录')
      resetPasswordForm()
      setTimeout(() => {
        userStore.logout()
        router.push('/login')
      }, 1500)
    } else {
      // 处理错误
      if (data.old_password) {
        ElMessage.error('原始密码不正确')
      } else if (data.error) {
        ElMessage.error(data.error)
      } else {
        ElMessage.error('密码修改失败，请重试')
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('修改密码失败:', error)
    }
  }
}
```

### 后端实现

#### API 端点

```python
@action(detail=False, methods=['post'])
def change_password(self, request):
    """修改密码"""
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    # 验证参数
    if not old_password or not new_password:
        return Response(
            {'error': '原始密码和新密码不能为空'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 验证原始密码
    if not user.check_password(old_password):
        return Response(
            {'old_password': '原始密码不正确'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 验证新密码长度
    if len(new_password) < 6 or len(new_password) > 20:
        return Response(
            {'new_password': '密码长度必须为 6-20 位字符'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 验证新密码不能与原密码相同
    if old_password == new_password:
        return Response(
            {'new_password': '新密码不能与原始密码相同'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 修改密码
    user.set_password(new_password)
    # 同时更新明文密码字段
    user.plain_password = new_password
    user.save()

    return Response({
        'message': '密码修改成功'
    }, status=status.HTTP_200_OK)
```

---

## 使用流程

### 步骤 1：进入设置页面

1. 登录系统
2. 访问个人中心 `http://localhost:3001/profile`
3. 点击左侧菜单的"设置"

### 步骤 2：填写密码表单

1. 在"修改密码"模块中填写：
   - 原始密码：输入当前登录密码
   - 新密码：输入新的密码（6-20位）
   - 确认新密码：再次输入新密码

2. 实时验证：
   - 输入框失去焦点时自动验证
   - 验证失败时显示错误提示

### 步骤 3：提交修改

1. 点击"修改密码"按钮
2. 在弹出的确认对话框中点击"确定修改"
3. 等待处理结果

### 步骤 4：重新登录

1. 密码修改成功后显示提示
2. 1.5秒后自动退出登录
3. 跳转到登录页面
4. 使用新密码登录

---

## 验证场景

### 场景 1：原始密码错误

**操作**：
1. 输入错误的原始密码
2. 输入新密码和确认密码
3. 点击"修改密码"

**预期结果**：
- ❌ 提示"原始密码不正确"
- ❌ 密码未修改

### 场景 2：新密码与原密码相同

**操作**：
1. 输入正确的原始密码
2. 新密码输入与原密码相同的值
3. 输入框失去焦点

**预期结果**：
- ❌ 输入框下方提示"新密码不能与原始密码相同"
- ❌ 无法提交表单

### 场景 3：确认密码不一致

**操作**：
1. 输入正确的原始密码
2. 输入新密码
3. 确认密码输入不同的值
4. 输入框失去焦点

**预期结果**：
- ❌ 输入框下方提示"两次输入的密码不一致"
- ❌ 无法提交表单

### 场景 4：密码长度不符

**操作**：
1. 输入正确的原始密码
2. 新密码输入少于6位或多于20位
3. 输入框失去焦点

**预期结果**：
- ❌ 输入框下方提示"密码长度为 6-20 位字符"
- ❌ 无法提交表单

### 场景 5：取消修改

**操作**：
1. 填写完整的表单
2. 点击"修改密码"
3. 在确认对话框中点击"取消"

**预期结果**：
- ✅ 对话框关闭
- ✅ 密码未修改
- ✅ 表单数据保留

### 场景 6：成功修改密码

**操作**：
1. 输入正确的原始密码
2. 输入符合要求的新密码
3. 确认密码输入一致
4. 点击"修改密码"
5. 在确认对话框中点击"确定修改"

**预期结果**：
- ✅ 提示"密码修改成功，请重新登录"
- ✅ 1.5秒后自动退出登录
- ✅ 跳转到登录页面
- ✅ 使用新密码可以成功登录
- ✅ 使用旧密码无法登录

---

## 安全特性

### 1. 密码验证

- ✅ 原始密码必须正确
- ✅ 新密码长度限制（6-20位）
- ✅ 新密码不能与原密码相同
- ✅ 确认密码必须一致

### 2. 二次确认

- ✅ 修改前弹出确认对话框
- ✅ 提示修改后需要重新登录
- ✅ 用户可以取消操作

### 3. 自动退出

- ✅ 修改成功后自动退出登录
- ✅ 清除所有登录状态
- ✅ 强制用户使用新密码登录

### 4. 密码存储

- ✅ 哈希密码存储（Django 内置）
- ✅ 明文密码存储（管理后台使用）
- ✅ 修改时同步更新两个字段

---

## 界面设计

### 表单布局

```
┌─────────────────────────────────────┐
│ 修改密码                             │
├─────────────────────────────────────┤
│ 原始密码    [**********]  👁         │
│ 新密码      [**********]  👁         │
│ 确认新密码  [**********]  👁         │
│                                      │
│ [修改密码]  [重置]                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ℹ️ 密码修改提示                      │
├─────────────────────────────────────┤
│ • 密码长度为 6-20 位字符             │
│ • 新密码不能与原始密码相同           │
│ • 修改密码后需要重新登录             │
│ • 请妥善保管您的密码                 │
└─────────────────────────────────────┘
```

### 确认对话框

```
┌─────────────────────────────────────┐
│ ⚠️  确认修改密码                     │
├─────────────────────────────────────┤
│ 修改密码后需要重新登录，             │
│ 确定要继续吗？                       │
│                                      │
│              [取消]  [确定修改]      │
└─────────────────────────────────────┘
```

---

## 已修改的文件

### 前端

1. ✅ `frontend-web/src/views/Profile.vue`
   - 添加密码修改表单
   - 添加验证规则
   - 添加 `handleChangePassword` 函数
   - 添加 `resetPasswordForm` 函数
   - 添加密码提示信息

### 后端

2. ✅ `backend/apps/users/views.py`
   - 添加 `change_password` API 端点
   - 实现密码验证逻辑
   - 同步更新哈希密码和明文密码

### 文档

3. ✅ `README.md` - 添加密码修改功能说明
4. ✅ `CHANGELOG.md` - 记录新增功能
5. ✅ `docs/PASSWORD_CHANGE_FEATURE.md` - 本文档

---

## 测试清单

### 功能测试

- [ ] 原始密码验证
  - [ ] 输入正确的原始密码
  - [ ] 输入错误的原始密码
  - [ ] 不输入原始密码

- [ ] 新密码验证
  - [ ] 输入符合要求的新密码（6-20位）
  - [ ] 输入少于6位的新密码
  - [ ] 输入多于20位的新密码
  - [ ] 新密码与原密码相同
  - [ ] 不输入新密码

- [ ] 确认密码验证
  - [ ] 确认密码与新密码一致
  - [ ] 确认密码与新密码不一致
  - [ ] 不输入确认密码

- [ ] 修改流程
  - [ ] 点击"修改密码"按钮
  - [ ] 确认对话框显示
  - [ ] 点击"取消"按钮
  - [ ] 点击"确定修改"按钮
  - [ ] 修改成功提示
  - [ ] 自动退出登录
  - [ ] 跳转到登录页

- [ ] 重新登录
  - [ ] 使用新密码登录成功
  - [ ] 使用旧密码登录失败

### 界面测试

- [ ] 表单布局正常
- [ ] 输入框显示正常
- [ ] 密码显示/隐藏功能正常
- [ ] 错误提示显示正常
- [ ] 按钮状态正常
- [ ] 提示信息显示正常

### 安全测试

- [ ] 原始密码验证有效
- [ ] 新密码长度限制有效
- [ ] 新旧密码不能相同
- [ ] 确认密码验证有效
- [ ] 二次确认机制有效
- [ ] 自动退出机制有效

---

## 常见问题

### Q1: 忘记原始密码怎么办？

**A**: 目前系统不支持密码找回功能，请联系管理员重置密码。

### Q2: 修改密码后其他设备会自动退出吗？

**A**: 目前只会退出当前设备，其他设备的 token 仍然有效。建议后续添加"退出所有设备"功能。

### Q3: 密码可以使用特殊字符吗？

**A**: 可以，密码支持所有字符，只要长度在 6-20 位之间即可。

### Q4: 修改密码后可以立即使用新密码登录吗？

**A**: 可以，密码修改后立即生效。

---

## 后续优化建议

### 1. 密码强度检测

- 添加密码强度指示器
- 提示用户使用强密码
- 建议包含大小写字母、数字、特殊字符

### 2. 密码找回功能

- 通过邮箱找回密码
- 通过手机号找回密码
- 安全问题验证

### 3. 多设备管理

- 显示所有登录设备
- 支持退出指定设备
- 支持退出所有设备

### 4. 密码历史

- 记录密码修改历史
- 防止使用最近使用过的密码
- 显示上次修改时间

### 5. 安全提醒

- 定期提醒用户修改密码
- 检测异常登录行为
- 发送密码修改通知

---

**功能已完成！** 🎉
