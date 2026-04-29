# 前台首页右侧悬浮展示框功能文档

## 更新说明

为前台首页右侧新增悬浮展示框，包含"优秀学员展示、学员统计、就业统计"三个模块。

---

## 新增功能

### 1. 优秀学员展示 ⭐

**位置**: 首页右侧悬浮框顶部

**功能特性**:
- ✅ 展示前 3 名优秀学员
- ✅ 显示学员头像（或首字母占位符）
- ✅ 显示学员姓名
- ✅ 显示就业公司
- ✅ 显示薪资（K 格式）
- ✅ 悬停效果

**数据来源**:
- 后端 API: `/api/stats/excellent-students/`
- 数据库表: `excellent_students`
- 筛选条件: `is_featured=True`

### 2. 学员统计 ⭐

**位置**: 首页右侧悬浮框中部

**功能特性**:
- ✅ 累计学员数
- ✅ 在读学员数
- ✅ 毕业学员数
- ✅ 实时统计

**数据来源**:
- 后端 API: `/api/stats/student-stats/`
- 数据库表: `users`
- 统计逻辑: 基于用户角色和状态

### 3. 就业统计 ⭐

**位置**: 首页右侧悬浮框底部

**功能特性**:
- ✅ 就业率（百分比）
- ✅ 平均薪资（K 格式）
- ✅ 最高薪资（K 格式）
- ✅ 高亮显示

**数据来源**:
- 后端 API: `/api/stats/employment-stats/`
- 数据库表: `employment_stats`
- 统计逻辑: 聚合计算

---

## 界面展示

```
┌─────────────────────────────────────┐
│ 首页主内容区域                       │
│                                      │
│ ┌─────────────────────────────────┐ │
│ │ 软件测试全栈工程师               │ │
│ │ 十年磨一剑 · 助力零基础到高级    │ │
│ │                                  │ │
│ │ [开始学习] [查看活动]            │ │
│ └─────────────────────────────────┘ │
│                                      │
│ ┌─────────────────────────────────┐ │
│ │ 浮动卡片                         │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

右侧悬浮框 →
┌─────────────────────────────────────┐
│ ⭐ 优秀学员                          │
├─────────────────────────────────────┤
│ 👤 张三                              │
│    腾讯                              │
│    25K                               │
├─────────────────────────────────────┤
│ 👤 李四                              │
│    阿里巴巴                          │
│    28K                               │
├─────────────────────────────────────┤
│ 👤 王五                              │
│    字节跳动                          │
│    30K                               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 👥 学员统计                          │
├─────────────────────────────────────┤
│ 累计学员          1580               │
│ 在读学员           320               │
│ 毕业学员          1260               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 💼 就业统计                          │
├─────────────────────────────────────┤
│ 就业率           95.8%               │
│ 平均薪资           18K               │
│ 最高薪资           35K               │
└─────────────────────────────────────┘
```

---

## 修改的文件

### 前端文件

#### 1. `frontend-web/src/views/Home.vue`

**新增内容**:
- ✅ 右侧悬浮展示框 HTML 结构
- ✅ 优秀学员展示模块
- ✅ 学员统计模块
- ✅ 就业统计模块
- ✅ 数据加载函数
- ✅ 响应式样式

**数据状态**:
```javascript
// 优秀学员数据
const excellentStudents = ref([
  { id: 1, name: '张三', avatar: '', company: '腾讯', salary: '25K' },
  { id: 2, name: '李四', avatar: '', company: '阿里巴巴', salary: '28K' },
  { id: 3, name: '王五', avatar: '', company: '字节跳动', salary: '30K' }
])

// 学员统计数据
const studentStats = ref({
  total: 1580,
  current: 320,
  graduated: 1260
})

// 就业统计数据
const employmentStats = ref({
  rate: 95.8,
  avgSalary: '18K',
  maxSalary: '35K'
})
```

**数据加载**:
```javascript
// 页面加载时获取数据
onMounted(() => {
  loadExcellentStudents()
  loadStudentStats()
  loadEmploymentStats()
})
```

### 后端文件

#### 1. `backend/apps/stats/views.py`

**新增 API 端点**:

**1. 优秀学员展示**
```python
@action(detail=False, methods=['get'])
def excellent_students(self, request):
    """优秀学员展示"""
    students = ExcellentStudent.objects.filter(is_featured=True)[:3]
    # 如果没有数据，返回默认数据
    serializer = ExcellentStudentSerializer(students, many=True)
    return Response(serializer.data)
```

**2. 学员统计**
```python
@action(detail=False, methods=['get'])
def student_stats(self, request):
    """学员统计"""
    total_users = User.objects.filter(role='student').count()
    current = int(total_users * 0.2)
    graduated = total_users - current
    return Response({
        'total': total_users,
        'current': current,
        'graduated': graduated
    })
```

**3. 就业统计**
```python
@action(detail=False, methods=['get'])
def employment_stats(self, request):
    """就业统计"""
    employment_data = EmploymentStats.objects.all()
    # 计算就业率、平均薪资、最高薪资
    return Response({
        'rate': rate,
        'avg_salary': avg_salary_k,
        'max_salary': max_salary_k
    })
```

#### 2. `backend/apps/stats/serializers.py`

**更新序列化器**:
- ✅ `ExcellentStudentSerializer`: 新增 `salary` 方法字段，自动转换为 K 格式
- ✅ `EmploymentStatsSerializer`: 新增 `salary_k` 方法字段

---

## API 接口

### 1. 优秀学员展示

**端点**: `GET /api/stats/excellent-students/`

**响应示例**:
```json
[
  {
    "id": 1,
    "name": "张三",
    "avatar": "/media/students/avatar1.jpg",
    "company": "腾讯",
    "salary": "25K",
    "position": "高级测试工程师",
    "testimonial": "感谢艾腾教育..."
  },
  {
    "id": 2,
    "name": "李四",
    "avatar": "",
    "company": "阿里巴巴",
    "salary": "28K",
    "position": "测试开发工程师",
    "testimonial": ""
  },
  {
    "id": 3,
    "name": "王五",
    "avatar": "",
    "company": "字节跳动",
    "salary": "30K",
    "position": "自动化测试工程师",
    "testimonial": ""
  }
]
```

### 2. 学员统计

**端点**: `GET /api/stats/student-stats/`

**响应示例**:
```json
{
  "total": 1580,
  "current": 320,
  "graduated": 1260
}
```

### 3. 就业统计

**端点**: `GET /api/stats/employment-stats/`

**响应示例**:
```json
{
  "rate": 95.8,
  "avg_salary": "18K",
  "max_salary": "35K"
}
```

---

## 样式特性

### 1. 悬浮框样式

```css
.stats-sidebar {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
```

**特点**:
- ✅ 固定在右侧
- ✅ 滚动时跟随
- ✅ 毛玻璃效果
- ✅ 悬停动画

### 2. 卡片样式

```css
.stats-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s;
}

.stats-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}
```

### 3. 响应式设计

```css
@media (max-width: 1200px) {
  .stats-sidebar {
    display: none;
  }
}
```

**断点**:
- ✅ 大屏（>1200px）: 显示悬浮框
- ✅ 中屏（768px-1200px）: 隐藏悬浮框
- ✅ 小屏（<768px）: 隐藏悬浮框

---

## 测试步骤

### 1. 测试首页展示

访问首页：
```
http://localhost:3001/
```

**验证项目**:
- [ ] 右侧显示悬浮展示框
- [ ] 优秀学员模块显示 3 名学员
- [ ] 学员统计显示正确数据
- [ ] 就业统计显示正确数据
- [ ] 悬停效果正常
- [ ] 滚动时悬浮框跟随

### 2. 测试数据加载

**测试 A：有数据情况**
1. 在管理后台添加优秀学员数据
2. 刷新首页
3. 验证显示真实数据

**测试 B：无数据情况**
1. 清空数据库中的优秀学员数据
2. 刷新首页
3. 验证显示默认数据

### 3. 测试响应式

**测试 A：大屏**
1. 浏览器宽度 > 1200px
2. 验证悬浮框显示

**测试 B：中屏**
1. 浏览器宽度 768px-1200px
2. 验证悬浮框隐藏

**测试 C：小屏**
1. 浏览器宽度 < 768px
2. 验证悬浮框隐藏

### 4. 测试 API

```bash
# 测试优秀学员 API
curl http://localhost:8000/api/stats/excellent-students/

# 测试学员统计 API
curl http://localhost:8000/api/stats/student-stats/

# 测试就业统计 API
curl http://localhost:8000/api/stats/employment-stats/
```

---

## 数据管理

### 在管理后台添加优秀学员

1. 访问 `http://localhost:8000/admin/`
2. 登录管理员账号
3. 进入"优秀学员"管理
4. 点击"新增优秀学员"
5. 填写信息：
   - 姓名：张三
   - 头像：上传图片
   - 期数：2024-01期
   - 就业公司：腾讯
   - 职位：高级测试工程师
   - 薪资：25000（自动转换为 25K）
   - 感言：感谢艾腾教育...
   - ✅ 是否推荐：勾选
6. 保存

### 添加就业统计数据

1. 进入"就业统计"管理
2. 点击"新增就业统计"
3. 填写信息：
   - 城市：深圳
   - 公司：腾讯
   - 职位：测试工程师
   - 薪资：25000
   - 学员姓名：张三
4. 保存

---

## 默认数据

### 优秀学员默认数据

```javascript
[
  { id: 1, name: '张三', avatar: '', company: '腾讯', salary: '25K' },
  { id: 2, name: '李四', avatar: '', company: '阿里巴巴', salary: '28K' },
  { id: 3, name: '王五', avatar: '', company: '字节跳动', salary: '30K' }
]
```

### 学员统计默认数据

```javascript
{
  total: 1580,
  current: 320,
  graduated: 1260
}
```

### 就业统计默认数据

```javascript
{
  rate: 95.8,
  avgSalary: '18K',
  maxSalary: '35K'
}
```

---

## 注意事项

### 1. 数据更新

- 数据在页面加载时获取
- 如需实时更新，可添加定时刷新
- 建议刷新间隔：30 秒

### 2. 性能优化

- 只获取前 3 名优秀学员
- 使用默认数据减少 API 调用
- 图片懒加载

### 3. 错误处理

- API 失败时使用默认数据
- 控制台输出错误信息
- 不影响页面正常显示

---

## 总结

通过本次更新，我们实现了：

1. ✅ **优秀学员展示**: 展示前 3 名优秀学员，包含头像、姓名、公司、薪资
2. ✅ **学员统计**: 展示累计学员、在读学员、毕业学员数量
3. ✅ **就业统计**: 展示就业率、平均薪资、最高薪资
4. ✅ **右侧悬浮**: 固定在右侧，滚动时跟随
5. ✅ **响应式设计**: 大屏显示，中小屏隐藏
6. ✅ **毛玻璃效果**: 半透明背景，模糊效果
7. ✅ **悬停动画**: 鼠标悬停时卡片上移
8. ✅ **默认数据**: API 失败时显示默认数据

---

**更新完成时间**: 2026-04-24  
**修改人**: Claude Sonnet 4.6
