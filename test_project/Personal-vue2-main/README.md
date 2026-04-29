# Courseware Web Project

这是一个基于Vue.js的课件Web项目。

## 功能特性

- 基于Vue.js框架开发
- 使用Element UI组件库
- 支持权限控制
- 数据可视化功能（ECharts）

## 快速开始

### 开发环境

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 生产构建

```bash
# 构建生产版本
npm run build:prod
```

## Docker 部署

本项目支持通过 Docker 进行容器化部署。

### 使用 Docker 直接部署

```bash
# 构建 Docker 镜像
docker build -t courseware-web .

# 运行容器
docker run -d -p 8080:80 --name courseware-web courseware-web
```

访问 `http://localhost:8080` 即可查看应用。

### 使用 Docker Compose 部署

```bash
# 构建并启动服务
docker-compose up -d
```

访问 `http://localhost:8080` 即可查看应用。

### 停止服务

```bash
# 停止并移除容器
docker-compose down
```

## 项目结构

```
.
├── public                   # 静态资源
│   └── index.html           # HTML模板
├── src                      # 源代码
│   ├── api                  # API接口
│   ├── components           # 全局组件
│   ├── layout               # 布局组件
│   ├── router               # 路由配置
│   ├── store                # 状态管理
│   ├── styles               # 全局样式
│   ├── utils                # 工具函数
│   ├── views                # 页面视图
│   ├── App.vue              # 根组件
│   ├── main.js              # 入口文件
│   ├── permission.js        # 权限控制
│   └── settings.js          # 配置文件
├── .env.xxx                 # 环境变量配置
├── vue.config.js            # Vue CLI 配置
└── package.json             # 包依赖管理
```

## 许可证

MIT