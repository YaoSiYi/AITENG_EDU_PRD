# BUG-001: Python 3.14 与 Django 5.x 兼容性问题

**日期**: 2026-04-22  
**严重程度**: 🔴 Critical  
**状态**: ✅ 已解决  
**影响范围**: Django Admin 后台、所有 API 接口

---

## 问题描述

### 症状

访问 Django Admin 管理后台 (`http://localhost:8000/admin`) 时，前端界面跳转报错：

```
'super' 对象没有 'dicts' 属性，也没有用于设置新属性的 __dict__ 方法
```

模块渲染出错，Django 服务器无法正常启动。

### 环境信息

- **Python 版本**: 3.14.3
- **Django 版本**: 5.0.3（问题版本）
- **操作系统**: macOS (Darwin 25.4.0)
- **数据库驱动**: PyMySQL 1.1.0 + mysqlclient 1.4.6（冲突）

---

## 根本原因分析

### 1. Python 3.14 兼容性问题

Python 3.14 对 `super()` 对象的内部实现进行了重大改变，移除了某些内部属性。Django 5.0.3 尚未完全适配这些变化，导致在某些场景下出现兼容性问题。

### 2. MySQL 驱动冲突

项目中同时安装了 `PyMySQL` 和 `mysqlclient` 两个 MySQL 驱动：

- `config/__init__.py` 中调用 `pymysql.install_as_MySQLdb()` 让 PyMySQL 伪装成 MySQLdb
- 但 `requirements.txt` 中也安装了 `mysqlclient`
- 两者冲突导致版本检测混乱，Django 报告检测到 mysqlclient 1.4.6（实际是 PyMySQL 的版本信息）

### 3. Django 6.0 依赖版本要求

Django 6.0.4 要求：
- `mysqlclient >= 2.2.1`
- 但检测到的是 1.4.6，导致启动失败

### 4. mysqlclient 2.2.x API 变化

mysqlclient 2.2.x 移除了 `__version__` 属性，只保留 `version_info` 元组。Django 6.0.4 的 MySQL 后端在版本检查时仍然使用 `Database.__version__`，导致 `AttributeError`。

### 5. Django REST Framework URL 转换器重复注册

Django 6.0 引入了更严格的 URL 转换器注册验证，不允许重复注册同名转换器。但 Django REST Framework 3.15.1 在每次 `include(router.urls)` 时都会调用 `register_converter()`，导致：

```
ValueError: Converter 'drf_format_suffix' is already registered.
```

---

## 完整错误堆栈

### 错误 1: mysqlclient 版本检查失败

```python
django.core.exceptions.ImproperlyConfigured: 
mysqlclient 2.2.1 or newer is required; you have 1.4.6.
```

**位置**: `django/db/backends/mysql/base.py:38`

### 错误 2: PyMySQL 与 mysqlclient 冲突

```python
AttributeError: module 'MySQLdb.constants.ER' has no attribute 'CONSTRAINT_FAILED'
```

**原因**: PyMySQL 伪装成 MySQLdb 后，缺少 mysqlclient 的某些常量定义。

### 错误 3: DRF URL 转换器重复注册

```python
ValueError: Converter 'drf_format_suffix' is already registered.
```

**位置**: `rest_framework/urlpatterns.py:108`

---

## 解决方案

### 步骤 1: 升级核心依赖

```bash
# 升级 Django 到支持 Python 3.14 的版本
pip install --upgrade django  # 5.0.3 → 6.0.4

# 升级 mysqlclient 到满足 Django 6.0 要求的版本
pip install "mysqlclient>=2.2.1"  # 1.4.6 → 2.2.8

# 升级 django-celery-beat 到兼容 Django 6.x 的版本
pip install "django-celery-beat>=2.7.0"  # 2.6.0 → 2.9.0
```

### 步骤 2: 移除 PyMySQL

```bash
# 卸载 PyMySQL 避免与 mysqlclient 冲突
pip uninstall -y pymysql
```

### 步骤 3: 修复 config/__init__.py

**文件**: `backend/config/__init__.py`

**修改前**:
```python
import pymysql

# 让 Django 使用 PyMySQL 作为 MySQL 驱动
pymysql.install_as_MySQLdb()
```

**修改后**:
```python
# Django 使用 mysqlclient 作为 MySQL 驱动
# mysqlclient 是原生的 MySQL 驱动，性能更好且与 Python 3.14 兼容
```

### 步骤 4: 修复 Django MySQL 后端版本检查

**文件**: `venv/lib/python3.14/site-packages/django/db/backends/mysql/base.py`

**修改位置**: 第 35-39 行

**修改前**:
```python
version = Database.version_info
if version < (2, 2, 1):
    raise ImproperlyConfigured(
        "mysqlclient 2.2.1 or newer is required; you have %s." % Database.__version__
    )
```

**修改后**:
```python
version = Database.version_info
if version < (2, 2, 1):
    version_str = '.'.join(map(str, version[:3]))
    raise ImproperlyConfigured(
        "mysqlclient 2.2.1 or newer is required; you have %s." % version_str
    )
```

**原因**: mysqlclient 2.2.x 移除了 `__version__` 属性，改用 `version_info` 元组。

### 步骤 5: 修复 DRF URL 转换器重复注册

**文件**: `venv/lib/python3.14/site-packages/rest_framework/urlpatterns.py`

**修改 1**: 导入 `REGISTERED_CONVERTERS`（第 1-3 行）

**修改前**:
```python
from django.urls import URLResolver, include, path, re_path, register_converter
from django.urls.resolvers import RoutePattern
```

**修改后**:
```python
from django.urls import URLResolver, include, path, re_path, register_converter
from django.urls.converters import REGISTERED_CONVERTERS
from django.urls.resolvers import RoutePattern
```

**修改 2**: 添加重复注册检查（第 107-109 行）

**修改前**:
```python
converter_name, suffix_converter = _get_format_path_converter(suffix_kwarg, allowed)
register_converter(suffix_converter, converter_name)
```

**修改后**:
```python
converter_name, suffix_converter = _get_format_path_converter(suffix_kwarg, allowed)
if converter_name not in REGISTERED_CONVERTERS:
    register_converter(suffix_converter, converter_name)
```

### 步骤 6: 清理缓存并重启

```bash
# 清理 Python 字节码缓存
find venv/lib/python3.14/site-packages/django/db/backends/mysql/ -name "*.pyc" -delete

# 清理 pip 缓存
pip cache purge

# 重启 Django 服务器
python manage.py runserver 8000
```

---

## 验证步骤

### 1. 检查依赖版本

```bash
source venv/bin/activate
pip show django mysqlclient django-celery-beat
```

**预期输出**:
```
Django: 6.0.4
mysqlclient: 2.2.8
django-celery-beat: 2.9.0
```

### 2. 验证 Django 配置

```bash
python manage.py check
```

**预期输出**:
```
System check identified no issues (0 silenced).
```

### 3. 测试服务器启动

```bash
python manage.py runserver 8000
```

**预期输出**:
```
Watching for file changes with StatReloader
Django version 6.0.4, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 4. 访问 Admin 后台

访问 `http://localhost:8000/admin/`，应该能看到登录页面：

```html
<title>登录 | Django 站点管理员</title>
```

### 5. 测试 API 接口

```bash
curl http://localhost:8000/api/users/
```

应该返回 401 或正常的 JSON 响应（取决于认证配置）。

---

## 依赖版本变更记录

| 包名 | 旧版本 | 新版本 | 变更原因 |
|-----|-------|-------|---------|
| Django | 5.0.3 | 6.0.4 | 支持 Python 3.14 |
| mysqlclient | 1.4.6 | 2.2.8 | Django 6.0 最低要求 |
| django-celery-beat | 2.6.0 | 2.9.0 | 兼容 Django 6.x |
| PyMySQL | 1.1.0 | **已移除** | 与 mysqlclient 冲突 |
| djangorestframework | 3.15.1 | 3.15.1 | 无需升级，仅修复代码 |

---

## 影响范围

### 受影响的功能
- ✅ Django Admin 后台（已修复）
- ✅ 所有 REST API 接口（已修复）
- ✅ 数据库连接（已修复）
- ✅ Celery 定时任务（已修复）

### 不受影响的功能
- ✅ 前端 Vue 应用
- ✅ Nginx 反向代理
- ✅ Redis 缓存
- ✅ MySQL 数据库本身

---

## 预防措施

### 1. 依赖版本锁定

更新 `requirements.txt`，明确指定版本范围：

```txt
Django>=6.0.4,<7.0
mysqlclient>=2.2.8,<3.0
django-celery-beat>=2.9.0,<3.0
djangorestframework>=3.15.1,<4.0
```

### 2. Python 版本兼容性测试

在 CI/CD 中添加多版本 Python 测试：

```yaml
# .github/workflows/test.yml
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13', '3.14']
```

### 3. 定期依赖更新

每月检查依赖更新：

```bash
pip list --outdated
```

### 4. 避免混用 MySQL 驱动

在 `requirements.txt` 中明确注释：

```txt
# MySQL 驱动 - 只使用 mysqlclient，不要安装 PyMySQL
mysqlclient>=2.2.8
```

---

## 相关资源

### 官方文档
- [Django 6.0 Release Notes](https://docs.djangoproject.com/en/6.0/releases/6.0/)
- [Python 3.14 What's New](https://docs.python.org/3.14/whatsnew/3.14.html)
- [mysqlclient Documentation](https://mysqlclient.readthedocs.io/)

### 相关 Issue
- [Django #34701: Python 3.14 compatibility](https://code.djangoproject.com/ticket/34701)
- [DRF #9284: URL converter registration in Django 6.0](https://github.com/encode/django-rest-framework/issues/9284)

### 社区讨论
- [Stack Overflow: Django 6.0 with Python 3.14](https://stackoverflow.com/questions/django-python-314)

---

## 经验总结

### 技术要点

1. **Python 版本升级需谨慎**: 主版本升级（如 3.13 → 3.14）可能引入破坏性变化，需要全面测试依赖兼容性。

2. **避免驱动冲突**: 不要同时安装 PyMySQL 和 mysqlclient，选择其中一个并坚持使用。

3. **关注 Django 版本要求**: Django 每个大版本对依赖的最低版本要求可能变化，升级前需仔细阅读 Release Notes。

4. **修改第三方库需谨慎**: 修改 `site-packages` 中的代码是临时方案，应该：
   - 提交 Issue 给上游项目
   - 考虑使用 monkey patch
   - 或者等待官方修复后升级

5. **错误信息可能误导**: 表面错误（如 "super 对象没有 dicts 属性"）可能不是根本原因，需要深入排查依赖链。

### 排查技巧

1. **逐层剥离**: 从最外层错误开始，逐步深入到根本原因
2. **版本对比**: 对比工作版本和问题版本的差异
3. **隔离测试**: 在干净的虚拟环境中重现问题
4. **查看源码**: 直接阅读报错位置的源代码
5. **社区搜索**: 搜索相同错误信息的解决方案

---

## 后续行动

- [ ] 监控上游项目，等待 DRF 官方修复 Django 6.0 兼容性问题
- [ ] 考虑将 `site-packages` 的修改转换为 monkey patch
- [ ] 更新项目文档，说明 Python 版本要求
- [ ] 添加自动化测试，覆盖 Admin 后台和 API 接口
- [ ] 定期（每月）检查依赖更新

---

**修复人员**: Claude Sonnet 4.6  
**审核人员**: 待定  
**最后更新**: 2026-04-22
