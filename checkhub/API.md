# CheckHub API 文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **认证方式**: Session Cookie
- **Content-Type**: `application/json`

## 认证接口

### 1. 登录页面

```
GET /auth/login
```

**响应**: HTML 登录页面

---

### 2. 登录

```
POST /auth/login
```

**请求参数** (Form Data):

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应**: 重定向到首页，设置 Session Cookie

**示例**:

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=admin123"
```

---

### 3. 退出登录

```
GET /auth/logout
```

**响应**: 清除 Session，重定向到登录页

---

## 仪表板接口

### 1. 仪表板页面

```
GET /
```

**权限**: 需要登录

**响应**: HTML 仪表板页面

**显示内容**:
- 站点统计
- 账户统计
- 日志列表
- 站点列表

---

### 2. 查看日志

```
GET /logs/{log_name}
```

**权限**: 需要登录

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| log_name | string | 日志文件名 |

**响应**: 文本格式的日志内容

**示例**:

```bash
curl http://localhost:8000/logs/example_2024-01-01.log \
  --cookie "session_id=xxx"
```

---

## 站点管理接口

### 1. 站点管理页面

```
GET /sites/
```

**权限**: 需要登录

**响应**: HTML 站点管理页面

---

### 2. 获取站点列表

```
GET /sites/api/list
```

**权限**: 需要登录

**响应**:

```json
{
  "success": true,
  "sites": [
    {
      "id": "example",
      "name": "示例站点",
      "enabled": true,
      "checker_class": "ExampleChecker",
      "account_count": 2
    }
  ]
}
```

**示例**:

```bash
curl http://localhost:8000/sites/api/list \
  --cookie "session_id=xxx"
```

---

### 3. 添加站点

```
POST /sites/api/add
```

**权限**: 需要登录

**请求体** (JSON):

```json
{
  "id": "mysite",
  "name": "我的站点",
  "checker_class": "ExampleChecker"
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 站点唯一标识（英文） |
| name | string | 是 | 站点显示名称 |
| checker_class | string | 否 | 签到器类名，默认 BaseChecker |

**成功响应**:

```json
{
  "success": true,
  "message": "站点添加成功"
}
```

**失败响应**:

```json
{
  "success": false,
  "error": "站点ID已存在"
}
```

**示例**:

```bash
curl -X POST http://localhost:8000/sites/api/add \
  --cookie "session_id=xxx" \
  -H "Content-Type: application/json" \
  -d '{"id":"test","name":"测试站点","checker_class":"ExampleChecker"}'
```

---

### 4. 删除站点

```
DELETE /sites/api/delete/{site_id}
```

**权限**: 需要登录

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| site_id | string | 站点ID |

**成功响应**:

```json
{
  "success": true,
  "message": "站点删除成功"
}
```

**失败响应**:

```json
{
  "success": false,
  "error": "站点不存在"
}
```

**示例**:

```bash
curl -X DELETE http://localhost:8000/sites/api/delete/test \
  --cookie "session_id=xxx"
```

---

### 5. 切换站点状态

```
POST /sites/api/toggle/{site_id}
```

**权限**: 需要登录

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| site_id | string | 站点ID |

**响应**:

```json
{
  "success": true,
  "enabled": true,
  "message": "状态更新成功"
}
```

**示例**:

```bash
curl -X POST http://localhost:8000/sites/api/toggle/example \
  --cookie "session_id=xxx"
```

---

### 6. 添加账户

```
POST /sites/api/add_account/{site_id}
```

**权限**: 需要登录

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| site_id | string | 站点ID |

**请求体** (JSON):

```json
{
  "username": "user1",
  "password": "pass1"
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 账户用户名 |
| password | string | 是 | 账户密码 |

**成功响应**:

```json
{
  "success": true,
  "message": "账户添加成功"
}
```

**示例**:

```bash
curl -X POST http://localhost:8000/sites/api/add_account/example \
  --cookie "session_id=xxx" \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"newpass"}'
```

---

### 7. 立即签到

```
POST /sites/api/check/{site_id}
```

**权限**: 需要登录

**路径参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| site_id | string | 站点ID |

**响应**:

```json
{
  "success": true,
  "results": [
    {
      "success": true,
      "message": "用户 user1 签到成功!",
      "timestamp": "2024-01-01T08:00:00"
    },
    {
      "success": false,
      "message": "用户 user2 签到失败: 密码错误",
      "timestamp": "2024-01-01T08:00:01"
    }
  ]
}
```

**示例**:

```bash
curl -X POST http://localhost:8000/sites/api/check/example \
  --cookie "session_id=xxx"
```

---

## 错误码

| HTTP 状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 302 | 重定向（未登录跳转到登录页） |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 认证流程

### 1. 获取 Session

首先需要登录获取 Session Cookie：

```bash
# 登录并保存 Cookie
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=admin123" \
  -c cookies.txt \
  -L

# 使用 Cookie 访问 API
curl http://localhost:8000/sites/api/list \
  -b cookies.txt
```

### 2. 使用 Session

所有需要认证的接口都需要带上 `session_id` Cookie：

```bash
curl http://localhost:8000/sites/api/list \
  --cookie "session_id=your-session-id-here"
```

---

## 使用示例

### Python 示例

```python
import requests

# 创建会话
session = requests.Session()

# 登录
login_data = {
    "username": "admin",
    "password": "admin123"
}
session.post("http://localhost:8000/auth/login", data=login_data)

# 获取站点列表
response = session.get("http://localhost:8000/sites/api/list")
print(response.json())

# 添加站点
new_site = {
    "id": "test",
    "name": "测试站点",
    "checker_class": "ExampleChecker"
}
response = session.post("http://localhost:8000/sites/api/add", json=new_site)
print(response.json())

# 立即签到
response = session.post("http://localhost:8000/sites/api/check/test")
print(response.json())
```

### JavaScript 示例

```javascript
// 登录
async function login() {
  const response = await fetch('/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'username=admin&password=admin123'
  });
  return response.ok;
}

// 获取站点列表
async function getSites() {
  const response = await fetch('/sites/api/list');
  const data = await response.json();
  return data.sites;
}

// 添加站点
async function addSite(id, name, checkerClass) {
  const response = await fetch('/sites/api/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: id,
      name: name,
      checker_class: checkerClass
    })
  });
  return await response.json();
}

// 立即签到
async function checkSite(siteId) {
  const response = await fetch(`/sites/api/check/${siteId}`, {
    method: 'POST'
  });
  return await response.json();
}
```

---

## 最佳实践

### 1. 错误处理

始终检查 `success` 字段：

```python
response = session.post("/sites/api/add", json=data)
result = response.json()

if result.get("success"):
    print("操作成功:", result.get("message"))
else:
    print("操作失败:", result.get("error"))
```

### 2. 并发请求

签到操作可能耗时较长，建议使用异步请求：

```python
import asyncio
import aiohttp

async def check_multiple_sites(site_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [
            session.post(f"http://localhost:8000/sites/api/check/{site_id}")
            for site_id in site_ids
        ]
        results = await asyncio.gather(*tasks)
        return results

# 使用
asyncio.run(check_multiple_sites(['site1', 'site2', 'site3']))
```

### 3. 超时设置

设置合理的请求超时：

```python
response = session.post(
    "/sites/api/check/example",
    timeout=60  # 60秒超时
)
```

---

## 更新日志

### v1.0.0 (2024-01-01)

- 初始版本
- 支持站点管理
- 支持账户管理
- 支持立即签到
- 支持认证系统

---

## 反馈与支持

如有问题，请提交 Issue。
