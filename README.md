# PCF Config

[![PyPI version](https://badge.fury.io/py/pcf-config.svg)](https://badge.fury.io/py/pcf-config)
[![Python versions](https://img.shields.io/pypi/pyversions/pcf-config.svg)](https://pypi.org/project/pcf-config/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple and flexible YAML configuration management library for Python applications. PCF Config provides an easy way to manage configuration files with support for nested keys, default values, and singleton pattern.

## Features

- 🔧 **Simple API**: Easy-to-use methods for getting configuration values
- 🏗️ **Nested Keys**: Support for dot-notation nested key access (e.g., `database.host`)
- 🛡️ **Default Values**: Graceful handling of missing keys with default values
- 🔄 **Hot Reload**: Reload configuration files at runtime
- 📦 **Singleton Pattern**: Global configuration instance for consistent access
- 🪶 **Lightweight**: Minimal dependencies (only PyYAML required)
- 🎯 **Type Hints**: Full type hint support for better IDE experience
- 📝 **Optional Logging**: Supports both loguru and standard logging

## Installation

Install from PyPI:

```bash
pip install pcf-config
```

Install with optional loguru support for better logging:

```bash
pip install pcf-config[loguru]
```

## Quick Start

1. **Create a configuration file** (`config.yaml`):

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

2. **Use in your Python code**:

```python
from pcf_config import get_config, get_config_with_default

# Get configuration values
db_host = get_config("database.host")  # Returns: "localhost"
db_port = get_config("database.port")  # Returns: 5432

# Get with default values
redis_host = get_config_with_default("redis.host", "localhost")
timeout = get_config_with_default("api.timeout", 30)

print(f"Database: {db_host}:{db_port}")
print(f"Redis: {redis_host}")
```

## API Reference

### Functions

#### `get_config(key: str) -> Any`

Get a configuration value by key. Supports nested keys using dot notation.

```python
from pcf_config import get_config

# Simple key
app_name = get_config("app_name")

# Nested key
db_host = get_config("database.host")
```

**Parameters:**
- `key` (str): Configuration key, supports dot notation for nested keys

**Returns:**
- `Any`: The configuration value

**Raises:**
- `KeyError`: If the key doesn't exist

#### `get_config_with_default(key: str, default: Any = None) -> Any`

Get a configuration value with a default fallback.

```python
from pcf_config import get_config_with_default

# With default value
debug = get_config_with_default("debug", False)
max_connections = get_config_with_default("database.max_connections", 100)
```

**Parameters:**
- `key` (str): Configuration key
- `default` (Any): Default value if key doesn't exist

**Returns:**
- `Any`: The configuration value or default

### Config Class

For advanced usage, you can use the `Config` class directly:

```python
from pcf_config import Config

config = Config()

# Check if key exists
if config.has_key("database.host"):
    host = config.get("database.host")

# Reload configuration
config.reload()
```

#### Methods

##### `get(key: str) -> Any`
Get configuration value by key.

##### `get_with_default(key: str, default: Any = None) -> Any`
Get configuration value with default fallback.

##### `has_key(key: str) -> bool`
Check if a configuration key exists.

##### `reload() -> None`
Reload the configuration file from disk.

## Configuration File Location

PCF Config looks for configuration files in the following order:

1. `config.yaml` in the current working directory
2. `config.yaml` in the package directory

## Examples

### Basic Usage

```python
from pcf_config import get_config, get_config_with_default

# config.yaml:
# app:
#   name: "My App"
#   version: "1.0.0"
#   debug: true
# database:
#   host: "localhost"
#   port: 5432

app_name = get_config("app.name")           # "My App"
app_version = get_config("app.version")     # "1.0.0"
db_host = get_config("database.host")       # "localhost"

# Using defaults for missing keys
cache_ttl = get_config_with_default("cache.ttl", 3600)  # 3600 (default)
debug_mode = get_config_with_default("app.debug", False)  # True (from config)
```

### Error Handling

```python
from pcf_config import get_config, get_config_with_default

try:
    api_key = get_config("api.secret_key")
except KeyError:
    print("API key not configured!")
    api_key = None

# Or use default values to avoid exceptions
api_key = get_config_with_default("api.secret_key", None)
if not api_key:
    print("Warning: API key not configured!")
```

### Hot Reload

```python
from pcf_config import Config

config = Config()

# Initial load
print(config.get("app.name"))

# Modify config.yaml file externally...

# Reload configuration
config.reload()
print(config.get("app.name"))  # Updated value
```

### Complex Configuration

```yaml
# config.yaml
app:
  name: "My Application"
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
from pcf_config import get_config

# Access nested configurations
primary_db = get_config("database.primary.host")
username = get_config("database.primary.credentials.username")

# Access array elements
services = get_config("services")
auth_service = services[0]["url"]  # "https://auth.example.com"
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/yourusername/pcf-config.git
cd pcf-config

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Run linting
black .
flake8
mypy pcf_config
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pcf_config --cov-report=html

# Run specific test file
pytest tests/test_config.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release
- Basic configuration loading from YAML files
- Support for nested keys with dot notation
- Default value support
- Hot reload functionality
- Singleton pattern implementation
- Optional loguru integration

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/pcf-config/issues) on GitHub.
