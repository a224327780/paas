# CheckinHub 开发指南

## 项目架构

### 核心模块

```
checkinhub/
├── sites/          # 站点签到模块
├── notifiers/      # 通知模块
├── utils/          # 工具模块
└── main.py         # 主程序
```

### 设计模式

1. **基类模式** - 所有站点继承 `BaseSite`
2. **注册模式** - 站点通过 `SITE_REGISTRY` 注册
3. **异步模式** - 使用 `asyncio` + `aiohttp`
4. **配置驱动** - TOML 配置文件

## 添加新站点

### 步骤 1: 创建站点类

在 `sites/` 目录创建新文件，例如 `mysite.py`：

```python
import aiohttp
from typing import Dict, Any
from .base import BaseSite, CheckinResult


class MySite(BaseSite):
    """我的站点签到器"""
    
    site_name = "mysite"  # 站点ID，必须唯一
    
    async def checkin(self, account: Dict[str, Any]) -> CheckinResult:
        """
        执行签到
        
        Args:
            account: 账户信息字典，包含 username, password, cookie 等
        
        Returns:
            CheckinResult: 签到结果
        """
        username = account.get('username', '')
        password = account.get('password', '')
        cookie = account.get('cookie', '')
        
        # 自定义字段
        extra_field = account.get('extra', {}).get('custom_field', '')
        
        try:
            async with aiohttp.ClientSession() as session:
                # 示例：登录
                async with session.post(
                    'https://mysite.com/api/login',
                    json={
                        'username': username,
                        'password': password
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status != 200:
                        return CheckinResult(
                            success=False,
                            message=f"登录失败: HTTP {resp.status}"
                        )
                    
                    login_data = await resp.json()
                    token = login_data.get('token', '')
                
                # 示例：签到
                headers = {'Authorization': f'Bearer {token}'}
                async with session.post(
                    'https://mysite.com/api/checkin',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return CheckinResult(
                            success=True,
                            message=f"签到成功: {data.get('message', '')}",
                            data=data
                        )
                    else:
                        return CheckinResult(
                            success=False,
                            message=f"签到失败: HTTP {resp.status}"
                        )
        
        except aiohttp.ClientError as e:
            return CheckinResult(
                success=False,
                message=f"网络错误: {str(e)}"
            )
        except Exception as e:
            return CheckinResult(
                success=False,
                message=f"未知错误: {str(e)}"
            )
```

### 步骤 2: 注册站点

在 `sites/__init__.py` 中添加：

```python
from .mysite import MySite

SITE_REGISTRY = {
    'example': ExampleSite,
    'glados': GladosSite,
    'hostloc': HostLocSite,
    'mysite': MySite,  # 添加新站点
}
```

### 步骤 3: 配置站点

在 `config/sites.toml` 中添加：

```toml
[mysite]
name = "我的站点"
enabled = true
notify = true

[[mysite.accounts]]
username = "user@example.com"
password = "password123"
cookie = ""
extra = { custom_field = "value" }
enabled = true
```

### 步骤 4: 测试

```bash
# 测试新站点
python main.py mysite

# 查看日志
cat logs/mysite_$(date +%Y-%m-%d).log
```

## 常用代码片段

### HTTP 请求

```python
# GET 请求
async with aiohttp.ClientSession() as session:
    async with session.get(
        url,
        headers=headers,
        timeout=aiohttp.ClientTimeout(total=30)
    ) as resp:
        data = await resp.json()

# POST 请求
async with session.post(
    url,
    json=payload,
    headers=headers,
    timeout=aiohttp.ClientTimeout(total=30)
) as resp:
    data = await resp.json()

# 带 Cookie
async with session.get(
    url,
    headers={'Cookie': cookie},
    timeout=aiohttp.ClientTimeout(total=30)
) as resp:
    data = await resp.text()
```

### 错误处理

```python
try:
    # 请求代码
    pass
except asyncio.TimeoutError:
    return CheckinResult(False, "请求超时")
except aiohttp.ClientError as e:
    return CheckinResult(False, f"网络错误: {e}")
except Exception as e:
    return CheckinResult(False, f"未知错误: {e}")
```

### 日志记录

```python
# 在站点类中
self.logger.info("开始签到", extra={'account': username})
self.logger.error("签到失败", extra={'account': username})
self.logger.debug("调试信息", extra={'account': username})
```

## 添加新通知器

### 步骤 1: 创建通知器类

在 `notifiers/` 目录创建文件，例如 `slack.py`：

```python
import aiohttp
from .base import BaseNotifier


class SlackNotifier(BaseNotifier):
    def __init__(self, config: dict, logger=None):
        super().__init__(config, logger)
        self.webhook_url = config.get('webhook_url', '')
    
    async def send(self, title: str, message: str) -> bool:
        if not self.webhook_url:
            return False
        
        payload = {
            "text": f"*{title}*\n{message}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            if self.logger:
                self.logger.error(f"Slack 发送失败: {e}")
            return False
```

### 步骤 2: 注册通知器

在 `notifiers/__init__.py` 中添加：

```python
from .slack import SlackNotifier

__all__ = [..., 'SlackNotifier']
```

### 步骤 3: 使用通知器

在 `main.py` 的 `run_site_checkin` 函数中添加：

```python
slack_config = main_config.get('notifications', {}).get('slack', {})
slack = SlackNotifier(slack_config, logger)
await slack.send_if_enabled(f"CheckinHub - {site_name}", message)
```

## 测试

### 单元测试

创建 `tests/test_sites.py`：

```python
import asyncio
import pytest
from sites import ExampleSite
from utils import get_site_logger


@pytest.mark.asyncio
async def test_example_site():
    logger = get_site_logger('example')
    site = ExampleSite(logger, {
        'example': {
            'name': 'Test Site'
        }
    })
    
    account = {
        'username': 'test@example.com',
        'password': 'password',
        'enabled': True
    }
    
    result = await site.checkin(account)
    assert result.success == True
```

运行测试：

```bash
pytest tests/
```

### 手动测试

```bash
# 测试单个站点
python main.py example

# 测试多个站点
python main.py example glados

# 查看详细日志
python main.py example --config config/config.toml
```

## 调试技巧

### 1. 增加日志级别

在 `config/config.toml` 中：

```toml
[logging]
level = "DEBUG"
```

### 2. 使用 Python 调试器

```python
import pdb; pdb.set_trace()
```

### 3. 查看请求详情

```python
async with session.get(url) as resp:
    print(f"Status: {resp.status}")
    print(f"Headers: {resp.headers}")
    print(f"Body: {await resp.text()}")
```

## 代码规范

### 命名规范

- 类名：大驼峰 `ExampleSite`
- 函数名：小写+下划线 `checkin_user`
- 变量名：小写+下划线 `user_name`
- 常量：大写+下划线 `MAX_RETRY`

### 文档字符串

```python
def function(param1: str, param2: int) -> bool:
    """
    函数描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
    
    Returns:
        返回值描述
    """
    pass
```

### 类型提示

```python
from typing import Dict, List, Optional, Any

async def checkin(self, account: Dict[str, Any]) -> CheckinResult:
    pass
```

## 性能优化

### 1. 并发签到

```python
tasks = [site.checkin(acc) for acc in accounts]
results = await asyncio.gather(*tasks)
```

### 2. 连接池复用

```python
connector = aiohttp.TCPConnector(limit=100)
async with aiohttp.ClientSession(connector=connector) as session:
    # 复用连接
    pass
```

### 3. 超时控制

```python
timeout = aiohttp.ClientTimeout(
    total=30,      # 总超时
    connect=10,    # 连接超时
    sock_read=20   # 读取超时
)
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 `git checkout -b feature/new-site`
3. 提交更改 `git commit -am 'Add new site'`
4. 推送分支 `git push origin feature/new-site`
5. 创建 Pull Request

## 参考资源

- [aiohttp 文档](https://docs.aiohttp.org/)
- [asyncio 文档](https://docs.python.org/3/library/asyncio.html)
- [TOML 规范](https://toml.io/)
