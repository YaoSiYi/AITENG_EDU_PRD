# BUG-002: 前端登录接口 404（缺少 /api 前缀）

**日期**: 2026-04-22  
**严重程度**: 🔴 High  
**状态**: ✅ 已解决  
**影响范围**: 前端登录流程、依赖用户鉴权的页面访问

---

## 问题现象

前端登录时报错：

```
:8000/users/login/:1 Failed to load resource: the server responded with a status of 404 (Not Found)
```

用户无法正常登录，导致测试用例管理页等需鉴权页面显示为空或被重定向。

---

## 根因分析

`frontend-web/src/stores/user.js` 中用户相关 API 路径未带 `/api` 前缀：

- `/users/login/`
- `/users/register/`
- `/users/profile/`
- `/users/update_profile/`

而后端真实接口前缀为 `/api`，应为：

- `/api/users/login/`
- `/api/users/register/`
- `/api/users/profile/`
- `/api/users/update_profile/`

请求发错地址，返回 404。

---

## 修复内容

### 1) 修复前端用户 Store API 路径

**文件**: `frontend-web/src/stores/user.js`

将所有用户接口路径统一改为带 `/api` 前缀。

### 2) 校正前端环境变量 API 基础地址

**文件**: `frontend-web/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 验证结果

- 后端登录接口可用：`POST /api/users/login/` ✅
- 前端服务可正常访问：`http://localhost:3000` ✅
- 登录流程恢复正常 ✅

---

## 预防措施

1. 前端 API 路径规范统一（必须以 `/api/...` 开头）。
2. 增加接口冒烟检查（登录、鉴权、个人信息接口）。
3. 改动 `request` 封装或用户 Store 时，加入回归检查清单。

---

**修复人**: Claude Sonnet 4.6  
**最后更新**: 2026-04-22
