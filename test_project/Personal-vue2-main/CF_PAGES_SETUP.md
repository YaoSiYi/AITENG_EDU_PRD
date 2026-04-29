# Cloudflare Pages 部署指南

您的项目是一个Vue.js前端应用，应该部署到Cloudflare Pages而不是Workers。

## 当前问题

您当前的配置试图将一个Vue.js前端项目作为Worker部署，但Vue.js项目生成的是静态文件，不是Worker代码。

## 正确的部署方式

### 1. 更正Cloudflare Pages设置

在Cloudflare控制台中，将您的部署配置更改为：

- **构建命令**: `npm run build`
- **构建输出目录**: `dist`
- **根目录**: `/` (而不是 /dist)
- **部署类型**: 选择 "Pages" 而不是 "Workers"

### 2. 部署配置详情

- **构建命令**: `npm install && npm run build`
- **构建输出**: `dist` 目录
- **环境变量**: 
  - NODE_ENV = production

### 3. 为什么不能使用Worker部署

- Cloudflare Worker用于运行JavaScript代码
- 您的Vue.js项目构建后产生的是静态HTML、CSS和JavaScript文件
- 静态文件应该使用Cloudflare Pages部署

### 4. 推荐的构建命令

在Cloudflare Pages设置中使用以下命令：

```bash
npm install && npm run build
```

构建后，您的文件将位于`dist`目录中，Cloudflare Pages将自动托管这些静态文件。

### 5. 重置部署配置

1. 进入Cloudflare Dashboard
2. 选择"Pages"服务
3. 删除当前的Worker部署
4. 创建新的Pages项目
5. 连接到您的仓库
6. 使用上述配置进行设置