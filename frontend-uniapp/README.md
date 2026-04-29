# 艾腾教育 - Uni-app 多端应用

> 软件测试全栈工程师培训系统 - 小程序/App/H5 多端应用

## 项目简介

本项目是基于 Uni-app 框架开发的跨平台应用，支持编译到微信小程序、App、H5 等多个平台。

## 技术栈

- **框架**: Uni-app 3.x
- **UI**: Vue 3 Composition API
- **状态管理**: Pinia
- **HTTP请求**: uni.request 封装
- **样式**: CSS + rpx 响应式单位

## 目录结构

```
frontend-uniapp/
├── pages/                    # 页面目录
│   ├── index/               # 首页
│   ├── login/               # 登录页
│   ├── questions/           # 题库页
│   ├── wrong-book/          # 错题本
│   ├── activities/          # 活动中心
│   └── profile/             # 个人中心
├── components/              # 公共组件
├── store/                   # Pinia状态管理
│   ├── index.js            # Pinia配置
│   ├── user.js             # 用户状态
│   ├── question.js         # 题库状态
│   └── activity.js         # 活动状态
├── api/                     # API接口
│   ├── index.js            # 统一导出
│   ├── user.js             # 用户接口
│   ├── question.js         # 题库接口
│   ├── activity.js         # 活动接口
│   └── stats.js            # 统计接口
├── utils/                   # 工具函数
│   ├── index.js            # 通用工具
│   ├── request.js          # HTTP请求封装
│   ├── auth.js             # 认证工具
│   └── storage.js          # 存储工具
├── common/                  # 公共资源
│   └── styles/             # 全局样式
│       └── common.css      # 通用样式
├── static/                  # 静态资源
│   ├── images/             # 图片
│   └── tabbar/             # TabBar图标
├── App.vue                  # 应用入口
├── main.js                  # 主入口文件
├── pages.json               # 页面配置
├── package.json             # 依赖配置
└── README.md                # 项目文档
```

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置API地址

修改 `utils/request.js` 中的 `BASE_URL`：

```javascript
const BASE_URL = 'http://localhost:8000/api'  // 开发环境
// const BASE_URL = 'https://api.example.com/api'  // 生产环境
```

### 3. 运行项目

#### 微信小程序

```bash
npm run dev:mp-weixin
```

然后使用微信开发者工具打开 `dist/dev/mp-weixin` 目录。

#### H5

```bash
npm run dev:h5
```

访问 http://localhost:8080

#### App

```bash
npm run dev:app
```

使用 HBuilderX 打开项目进行真机调试。

### 4. 构建发布

#### 微信小程序

```bash
npm run build:mp-weixin
```

#### H5

```bash
npm run build:h5
```

#### App

```bash
npm run build:app
```

## 核心功能

### 1. 用户认证

- 用户名/密码登录
- 微信一键登录（小程序）
- 游客模式
- Token自动刷新
- 登录状态持久化

### 2. 题库练习

- 题目列表（分页加载）
- 阶段筛选
- 难度筛选
- 随机练习
- 答题详情
- 错题本管理

### 3. 活动中心

- 活动列表
- 活动详情
- 活动报名
- 活动签到
- 我的活动

### 4. 个人中心

- 用户信息展示
- 学习统计
- 错题本入口
- 我的活动
- 设置
- 退出登录

## 状态管理

使用 Pinia 进行状态管理，主要包括：

### User Store (用户状态)

```javascript
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

// 登录
await userStore.login({ username, password })

// 获取用户信息
await userStore.fetchUserInfo()

// 登出
userStore.logout()
```

### Question Store (题库状态)

```javascript
import { useQuestionStore } from '@/store/question'

const questionStore = useQuestionStore()

// 获取题目列表
await questionStore.fetchQuestionList({ stage: 1 })

// 获取错题本
await questionStore.fetchWrongQuestions()

// 添加到错题本
await questionStore.addToWrong(questionId)
```

### Activity Store (活动状态)

```javascript
import { useActivityStore } from '@/store/activity'

const activityStore = useActivityStore()

// 获取活动列表
await activityStore.fetchActivityList()

// 参与活动
await activityStore.join(activityId)
```

## API 接口

所有 API 接口统一通过 `utils/request.js` 进行请求，自动处理：

- Token 认证
- 请求/响应拦截
- 错误处理
- 加载提示
- Token 过期自动跳转登录

### 使用示例

```javascript
import request from '@/utils/request'

// GET 请求
const res = await request.get('/questions/', { stage: 1 })

// POST 请求
const res = await request.post('/users/login/', { username, password })

// PUT 请求
const res = await request.put('/users/profile/', data)

// DELETE 请求
const res = await request.delete('/questions/wrong-book/1/')
```

## 工具函数

### 日期格式化

```javascript
import { formatDate } from '@/utils/index'

formatDate(new Date())  // 2026-04-29 12:00:00
formatDate(new Date(), 'YYYY-MM-DD')  // 2026-04-29
```

### Toast 提示

```javascript
import { showToast } from '@/utils/index'

showToast('操作成功', 'success')
showToast('操作失败', 'error')
```

### 确认对话框

```javascript
import { showConfirm } from '@/utils/index'

const confirmed = await showConfirm('确定要删除吗？')
if (confirmed) {
  // 执行删除操作
}
```

## 样式规范

### rpx 响应式单位

使用 rpx 作为响应式单位，1rpx = 屏幕宽度 / 750

```css
.container {
  padding: 32rpx;  /* 相当于 16px (在 375px 宽度的屏幕上) */
}
```

### 通用样式类

```html
<!-- Flex布局 -->
<view class="flex flex-between">
  <text>左侧</text>
  <text>右侧</text>
</view>

<!-- 文字省略 -->
<text class="ellipsis">这是一段很长的文字...</text>

<!-- 卡片样式 -->
<view class="card">卡片内容</view>

<!-- 按钮样式 -->
<button class="btn btn-primary">主要按钮</button>

<!-- 标签样式 -->
<text class="tag tag-success">成功</text>
```

## 平台差异处理

使用条件编译处理不同平台的差异：

```vue
<!-- 微信小程序特有代码 -->
<!-- #ifdef MP-WEIXIN -->
<button open-type="getUserProfile" @click="handleWechatLogin">
  微信登录
</button>
<!-- #endif -->

<!-- App特有代码 -->
<!-- #ifdef APP-PLUS -->
<view>App专属功能</view>
<!-- #endif -->

<!-- H5特有代码 -->
<!-- #ifdef H5 -->
<view>H5专属功能</view>
<!-- #endif -->
```

## 注意事项

1. **API地址配置**: 开发前请先配置正确的API地址
2. **微信小程序**: 需要在微信公众平台配置服务器域名白名单
3. **图片资源**: 建议使用网络图片或本地相对路径
4. **权限申请**: App端需要在 manifest.json 中配置相应权限
5. **真机调试**: 建议使用真机调试，模拟器可能存在兼容性问题

## 开发建议

1. **组件化开发**: 将可复用的UI封装成组件
2. **状态管理**: 复杂状态使用 Pinia 管理
3. **错误处理**: 所有异步操作都要有 try-catch
4. **加载状态**: 长时间操作要显示加载提示
5. **用户体验**: 操作成功/失败要有明确的反馈

## 常见问题

### 1. 如何调试？

- 微信小程序：使用微信开发者工具的调试功能
- H5：使用浏览器开发者工具
- App：使用 HBuilderX 的真机调试功能

### 2. 如何处理跨域？

开发环境可以在后端配置 CORS，生产环境建议使用 Nginx 反向代理。

### 3. 如何上传图片？

```javascript
uni.chooseImage({
  count: 1,
  success: (res) => {
    const tempFilePath = res.tempFilePaths[0]
    // 上传到服务器
    uni.uploadFile({
      url: BASE_URL + '/upload/',
      filePath: tempFilePath,
      name: 'file',
      success: (uploadRes) => {
        console.log('Upload success:', uploadRes)
      }
    })
  }
})
```

## 更新日志

### v1.0.0 (2026-04-29)

- ✅ 完整的代码框架搭建
- ✅ 6个核心页面开发
- ✅ Pinia状态管理集成
- ✅ API接口封装
- ✅ 工具函数库
- ✅ 通用样式库

## 技术支持

如有问题，请参考：

- Uni-app 官方文档: https://uniapp.dcloud.net.cn/
- Vue 3 文档: https://vuejs.org/
- Pinia 文档: https://pinia.vuejs.org/

---

**项目状态**: ✅ 代码框架已完成，可开始开发

**下一步**: 
1. 安装依赖并运行项目
2. 配置API地址
3. 测试核心功能
4. 根据需求调整和完善
