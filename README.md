# PCF Config

[![PyPI version](https://badge.fury.io/py/pcf-config.svg)](https://badge.fury.io/py/pcf-config)
[![Python versions](https://img.shields.io/pypi/pyversions/pcf-config.svg)](https://pypi.org/project/pcf-config/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[English](README_EN.md) | 简体中文

一个简单灵活的 Python 应用程序 YAML 配置文件管理库。PCF Config 提供了简单易用的方式来管理配置文件，支持嵌套键、默认值和读写操作。

## 特性

- 🔧 **简单 API**：易于使用的获取和设置配置值的方法
- 🏗️ **嵌套键**：支持点号分隔的嵌套键访问（如 `database.host`）
- 🛡️ **默认值**：优雅处理缺失键并提供默认值
- 🔄 **热重载**：运行时重新加载配置文件
- ✏️ **读写操作**：设置配置值并保存到文件
- 🪶 **轻量级**：最小依赖（仅需 PyYAML）
- 🎯 **类型提示**：完整的类型提示支持，提供更好的 IDE 体验
- 🚀 **非单例**：支持多个实例，提供更大的灵活性

## 安装

从 PyPI 安装：

```bash
pip install pcf-config
```

## 快速开始

1. **创建配置文件** (`config.yaml`)：

```yaml
database:
  host: localhost
  port: 5432
  name: myapp

api:
  host: 0.0.0.0
  port: 8000
  debug: true
```

2. **在 Python 代码中使用**：

```python
from pcf_config import Config

# 使用文件路径创建配置实例
config = Config("config.yaml")

# 获取配置值
db_host = config.get("database.host")  # 返回: "localhost"
db_port = config.get("database.port")  # 返回: 5432

# 使用默认值获取
redis_host = config.get("redis.host", "localhost")
timeout = config.get("api.timeout", 30)

# 设置新值
config.set("database.timeout", 30)
config.set("api.debug", True)

# 保存更改到文件
config.save()

print(f"数据库: {db_host}:{db_port}")
print(f"Redis: {redis_host}")
```

## API 参考

### Config 类

配置管理的主要类：

```python
from pcf_config import Config

# 使用文件路径创建配置实例
config = Config("config.yaml")

# 获取配置值
value = config.get("key")
value_with_default = config.get("key", "default")

# 设置配置值
config.set("new.key", "value")

# 保存更改到文件
config.save()

# 从文件重新加载
config.reload()

# 检查键是否存在
if config.has_key("key"):
    print("键存在")
```

#### 方法

##### `__init__(config_file: str)`
使用配置文件路径初始化 Config 实例。

**参数：**
- `config_file` (str)：YAML 配置文件的路径

##### `get(key: str, default: Any = ...) -> Any`
通过键获取配置值。支持使用点号分隔的嵌套键。

**参数：**
- `key` (str)：配置键，支持点号分隔的嵌套键
- `default` (Any)：如果键不存在时的默认值

**返回：**
- `Any`：配置值或默认值

**抛出：**
- `KeyError`：如果键不存在且未提供默认值

##### `set(key: str, value: Any) -> None`
设置配置值。如果需要会创建嵌套结构。

**参数：**
- `key` (str)：配置键，支持点号分隔的嵌套键
- `value` (Any)：要设置的值

##### `save() -> None`
将当前配置保存到文件。

##### `reload() -> None`
从磁盘重新加载配置文件。

##### `has_key(key: str) -> bool`
检查配置键是否存在。

**参数：**
- `key` (str)：要检查的配置键

**返回：**
- `bool`：如果键存在返回 True，否则返回 False

## 配置文件位置

PCF Config 要求您在创建 Config 实例时指定配置文件路径：

```python
config = Config("path/to/your/config.yaml")
```

## 示例

### 基本用法

```python
from pcf_config import Config

# 创建配置实例
config = Config("config.yaml")

# config.yaml:
# app:
#   name: "我的应用"
#   version: "1.0.0"
#   debug: true
# database:
#   host: "localhost"
#   port: 5432

app_name = config.get("app.name")           # "我的应用"
app_version = config.get("app.version")     # "1.0.0"
db_host = config.get("database.host")       # "localhost"

# 对缺失的键使用默认值
cache_ttl = config.get("cache.ttl", 3600)  # 3600 (默认值)
debug_mode = config.get("app.debug", False)  # True (来自配置)
```

### 错误处理

```python
from pcf_config import Config

config = Config("config.yaml")

try:
    api_key = config.get("api.secret_key")
except KeyError:
    print("API 密钥未配置！")
    api_key = None

# 或使用默认值避免异常
api_key = config.get("api.secret_key", None)
if not api_key:
    print("警告: API 密钥未配置！")
```

### 热重载

```python
from pcf_config import Config

config = Config("config.yaml")

# 初始加载
print(config.get("app.name"))

# 外部修改 config.yaml 文件...

# 重新加载配置
config.reload()
print(config.get("app.name"))  # 更新后的值
```

### 读写操作

```python
from pcf_config import Config

config = Config("config.yaml")

# 读取现有值
db_host = config.get("database.host")

# 设置新值
config.set("database.timeout", 30)
config.set("api.rate_limit", 1000)

# 保存更改到文件
config.save()

# 验证更改
print(config.get("database.timeout"))  # 30
print(config.get("api.rate_limit"))    # 1000
```

### 复杂配置

```yaml
# config.yaml
app:
  name: "我的应用程序"
  version: "2.1.0"
  
database:
  primary:
    host: "db1.example.com"
    port: 5432
    credentials:
      username: "admin"
      password: "secret"
  
  replica:
    host: "db2.example.com"
    port: 5432
    
services:
  - name: "auth"
    url: "https://auth.example.com"
  - name: "payment"
    url: "https://payment.example.com"
```

```python
from pcf_config import Config

config = Config("config.yaml")

# 访问嵌套配置
primary_db = config.get("database.primary.host")
username = config.get("database.primary.credentials.username")

# 访问数组元素
services = config.get("services")
auth_service = services[0]["url"]  # "https://auth.example.com"
```

## 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/pengcunfu/pcf-config.git
cd pcf-config

# 以开发模式安装
pip install -e .[dev]

# 运行测试
pytest

# 运行代码检查
black .
flake8
mypy pcf_config
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行覆盖率测试
pytest --cov=pcf_config --cov-report=html

# 运行特定测试文件
pytest tests/test_config.py
```

## 贡献

欢迎贡献！请随时提交 Pull Request。对于重大更改，请先打开 issue 讨论您想要更改的内容。

1. Fork 仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 许可证

本项目采用 Apache 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 更新日志

### v1.1.0
- **重大变更**：移除单例模式 - Config 现在需要明确的文件路径
- **重大变更**：移除便利函数 `get_config` 和 `get_config_with_default`
- **新增**：添加 `set()` 方法用于修改配置值
- **新增**：添加 `save()` 方法用于将更改持久化到文件
- **改进**：`get()` 方法现在支持使用 `...` 哨兵值的默认值
- **改进**：`reload()` 方法不再需要文件路径参数
- **移除**：loguru 依赖 - 现在仅使用标准日志
- **移除**：源码中的所有中文字符
- **改进**：更好的错误处理和类型提示

### v1.0.0
- 初始发布
- 从 YAML 文件加载基本配置
- 支持点号分隔的嵌套键
- 默认值支持
- 热重载功能
- 单例模式实现
- 可选的 loguru 集成

## 支持

如果您遇到任何问题或有疑问，请在 GitHub 上[打开 issue](https://github.com/pengcunfu/pcf-config/issues)。
