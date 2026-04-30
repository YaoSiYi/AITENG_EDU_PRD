# Changelog

所有版本的重要变更记录在此文件中。

---

## [Unreleased]

### Added

- **测试用例列表快速更新功能**：支持在列表中直接点击修改「优先级」「状态」「冒烟」三个字段并实时保存（PATCH 部分更新），无需进入编辑弹窗。
  - 优先级：下拉选择（紧急/高/中/低）
  - 状态：下拉选择（草稿/有效/已废弃）
  - 冒烟：点击标签即时切换（是/否）
- **测试用例状态新增**：状态字段新增 `closed`（已关闭），并同步到筛选、编辑弹窗、列表快捷修改、标签显示样式。
- **测试用例严重程度字段**：新增 `severity`（严重程度）字段，包含高/中/低三个级别，带图标标识（高=警告、中=信息、低=勾选），支持筛选、编辑、列表快捷修改。
- **测试用例复现步骤模块**：新增 `reproduce_steps`（复现步骤）字段，支持文字和图片混合添加，图片最大分辨率 2048x1280，支持 JPG/PNG/GIF/WEBP/BMP 格式，缩略图预览，鼠标悬停放大，点击关闭，**支持主页面实时编辑**。
- **测试用例指派人员功能**：新增 `assignee`（指派人员）字段，支持指派给除admin外的所有用户，列表快捷指派，筛选条件支持按指派人员和"只看我的指派"，被指派人收到站内通知，状态同步给指派人和被指派人。
- **注册模块期数字段**：新增 `period`（期数）字段，格式为YYYYMMDD（8位数字），必填项，支持日期有效性验证（年份2000-2100，月份01-12，日期01-31），Web和Uni-app端同步更新。

### Changed

- **时间格式统一**：所有模块的时间显示统一为标准格式 `YYYY-MM-DD HH:mm:ss`，创建全局时间格式化工具 `utils/datetime.js`，更新测试用例管理、个人中心、活动中心等页面的时间显示。
- **生产环境阶段颜色调整**：将"生产环境"阶段的标签颜色从绿色（success）改为红色（danger），以突出显示生产环境的重要性和风险性。
- **已关闭状态颜色调整**：将"已关闭"状态的标签颜色从红色（danger）改为蓝色（primary），使其更加友好和易于区分。
- **状态联动编辑控制**：当测试用例状态为"已关闭"时，整行显示蓝色高亮背景，除状态外其他字段不可编辑；当状态为"已废弃"时，整行显示灰色背景，除状态外其他字段不可编辑；只有"有效"和"草稿"状态可以正常编辑所有字段。
- **管理后台密码管理优化**：将用户密码从哈希加密显示改为明文密码显示，支持在 Django Admin 后台直接查看和修改用户密码，新增 `plain_password` 字段用于存储明文密码，修改密码时自动同步更新哈希密码。

### Fixed

- **前端登录 404**：`frontend-web/src/stores/user.js` 用户接口路径补全 `/api` 前缀，恢复登录与鉴权流程（详见 `docs/bugs/BUG-002-frontend-login-404.md`）
- **题库等模块 API 路径错误**：`frontend-web/src/api/index.js` 所有接口路径补全 `/api` 前缀，修复题库、活动、统计、评价模块的 API 调用
- **数据看板静态数据**：`frontend-web/src/views/Dashboard.vue` 改为实时获取测试用例统计数据，图表显示真实的优先级和状态分布（详见 `docs/bugs/BUG-003-dashboard-static-data.md`）
- **缺少返回首页入口**：为 `/testcases` 与 `/dashboard` 页面新增面包屑导航（`首页 / 页面名`），支持一键返回首页（详见 `docs/bugs/BUG-004-missing-home-navigation.md`）
- **个人中心编辑资料按钮无效**：`frontend-web/src/views/Profile.vue` 新增编辑弹窗组件和保存逻辑，修复编辑资料功能（详见 `docs/bugs/BUG-005-profile-edit-button-not-working.md`）
- **注册页面性别选项框遮挡文字**：将 `el-radio-button` 改为 `el-radio`，使用 flex 水平布局，修复选项框遮挡"性别"文字的问题（BUG-008）
- **注册页面性别选项颜色与座次不一致**：添加 `male-radio` 和 `female-radio` 类名，自定义选中颜色（男=湖蓝色、女=粉色），与座次页面保持一致，性别设为必选项（BUG-009）
- **后台用户管理缺少性别字段**：在 `UserAdmin` 中添加 `gender` 到 `list_display`、`list_filter`、`fieldsets` 和 `add_fieldsets`，支持列表显示、筛选和编辑（BUG-010）
- **个人中心设置缺少性别字段**：在设置表单添加性别 `el-radio-group`，添加 `watch` 监听从 store 加载数据，更新 `saveSettings` 调用 API（BUG-011）
- **部分用户无法登录系统**：修改 `User.save()` 方法，检查密码哈希是否与明文密码匹配，不匹配则重新生成；批量修复所有用户密码哈希（BUG-012）
- **数据看板 Vue 组件响应式警告**：使用 `markRaw()` 包装图标组件，防止 Vue 将其转换为响应式对象（BUG-013）
- **数据看板测试用例状态统计与管理页面不一致**：在 `statusCount` 添加 `closed` 统计，更新柱状图数据和 X 轴类别（BUG-014）
- **数据看板测试用例状态统计数据为空**：调整 `onMounted` 执行顺序，先初始化图表再加载数据；完善 `updateTestcaseCharts` 的 `setOption` 调用（BUG-015）
- **登录失败无提示且清空表单**：修改 `request.js` 响应拦截器，在登录页面收到 401 错误时不自动重定向，显示错误信息；修改 `Login.vue` 登录失败时不清空表单（BUG-016）
- **端口占用导致服务无法启动**：清理重复的前端进程（3个），统一API配置使用局域网IP（192.168.0.156），修复CORS配置支持手机访问（BUG-017）
- **Django ALLOWED_HOSTS配置错误**：添加局域网IP（192.168.0.156）到ALLOWED_HOSTS，修复手机端访问返回400 DisallowedHost错误（BUG-018）
- **Web前端API请求400错误**：修复Django ALLOWED_HOSTS配置，添加通配符支持所有主机访问（开发环境）（BUG-019）
- **Uni-app注册页面checkbox无法勾选**：使用checkbox-group包裹checkbox组件，修复H5环境下change事件不触发的问题（BUG-020）
- **Uni-app注册API缺少confirm_password字段**：在注册请求中添加confirm_password字段，修复后端验证失败问题（BUG-021）
- **Uni-app注册错误信息显示不友好**：改进request.js错误信息解析，支持显示字段验证错误的详细信息（BUG-022）
- **Uni-app注册模块userStore.register方法缺失**：在userStore中添加register方法，支持注册后自动登录（BUG-023）
- **注册模块字段不一致**：统一Web和Uni-app注册字段（用户名、昵称、手机号、籍贯、密码、确认密码、密码提示、性别），添加密码显示/隐藏功能（BUG-024）
- **用户名格式验证缺失**：添加用户名格式验证（只支持字母或字母+数字，必须以字母开头），添加输入提示和错误提示（BUG-025）
- **测试用例CSV导入中文值解析失败**：添加中文到英文的映射字典（priority/status/stage），支持导入包含中文值的CSV文件，兼容中英文两种格式（BUG-027）

---

## [0.0.7] - 2024-04-22

### Added

- **测试用例管理模块** (`apps.testcases`)
  - 完整的 CRUD API（9个端点）
  - TestCase 数据模型（19个字段）
  - 雪花算法 ID 生成器（`common/snowflake.py`）
  - CSV 批量导入导出功能
  - 高级筛选（8个筛选条件）
  - 关键字搜索
  - 安全防护（公式注入、XSS检测）
  - 审计追踪（创建人、修改人）
  - Django Admin 配置

- **测试用例管理前端页面** (`/testcases`)
  - 完整的 CRUD 操作界面
  - 数据表格（支持展开行）
  - 高级筛选和搜索
  - 批量操作（批量删除）
  - CSV 导入导出
  - 分页组件
  - 响应式设计

- **数据看板页面** (`/dashboard`)
  - 4个统计卡片（题目/用户/活动/测试用例）
  - 4个 ECharts 图表
    - 测试用例优先级分布（饼图）
    - 测试用例状态统计（柱状图）
    - 用户角色分布（饼图）
    - 题库难度分布（柱状图）
  - 实时数据加载
  - 响应式图表

- **导航集成**
  - 桌面端导航新增「测试用例」和「数据看板」菜单项
  - 移动端导航新增对应菜单项
  - 权限控制（登录后可见）

- **示例数据**
  - 20条真实测试用例（覆盖功能/接口/安全/兼容性/边界/性能测试）
  - 数据生成脚本（`create_sample_testcases.py`）

- **文档**
  - 详细集成文档（`TESTCASE_MODULE_INTEGRATION.md`）
  - 完整报告（`INTEGRATION_COMPLETE_REPORT.md`）
  - 导航集成说明（`NAVIGATION_INTEGRATION.md`）
  - 最终验证报告（`FINAL_VERIFICATION_REPORT.md`）
  - 快速参考（`QUICK_REFERENCE.md`）

### Changed

- 更新 README.md，添加 v0.0.7 版本记录
- 更新项目结构说明，包含 testcases 模块
- 更新核心功能列表，包含测试用例管理和数据看板

### Technical Details

**新增文件**: 15个（9个后端 + 3个前端 + 3个文档）  
**修改文件**: 4个（settings.py, urls.py, Home.vue, MobileNav.vue）  
**新增数据表**: 1个（testcases，19个字段）  
**API接口**: 9个  
**前端页面**: 2个  
**代码行数**: 2500+

---

## [1.0.1] - 2026-04-22

### Bug Fixes

- **Python 3.14 + Django 5.x 兼容性问题**（详见 `docs/bugs/BUG-001-python314-django-compatibility.md`）
  - 升级 Django 5.0.3 → 6.0.4，获得 Python 3.14 原生支持
  - 升级 mysqlclient 1.4.6 → 2.2.8，满足 Django 6.0 最低版本要求
  - 升级 django-celery-beat 2.6.0 → 2.9.0，兼容 Django 6.x
  - 移除 PyMySQL，改用 mysqlclient 作为唯一 MySQL 驱动
  - 修复 `config/__init__.py` 中残留的 `pymysql.install_as_MySQLdb()` 调用
  - 修复 Django REST Framework 在 Django 6.0 下重复注册 URL 转换器的问题

### Dependency Changes

| 包 | 旧版本 | 新版本 |
|---|---|---|
| Django | 5.0.3 | 6.0.4 |
| mysqlclient | 1.4.6 | 2.2.8 |
| django-celery-beat | 2.6.0 | 2.9.0 |
| PyMySQL | 1.1.0 | 已移除 |

---

## [1.0.0] - 2026-04-01

### Initial Release

- 用户管理模块（注册、登录、JWT 鉴权）
- 题库管理模块（题目、分类、错题本、作业）
- 活动管理模块
- 数据统计模块
- 评价模块
- Django Admin 后台
- Vue 3 前端管理界面
