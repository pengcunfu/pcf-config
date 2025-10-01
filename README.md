# PCF Config

[![PyPI version](https://badge.fury.io/py/pcf-config.svg)](https://badge.fury.io/py/pcf-config)
[![Python versions](https://img.shields.io/pypi/pyversions/pcf-config.svg)](https://pypi.org/project/pcf-config/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple and flexible YAML configuration management library for Python applications. PCF Config provides an easy way to manage configuration files with support for nested keys, default values, and read/write operations.

## Features

- 🔧 **Simple API**: Easy-to-use methods for getting and setting configuration values
- 🏗️ **Nested Keys**: Support for dot-notation nested key access (e.g., `database.host`)
- 🛡️ **Default Values**: Graceful handling of missing keys with default values
- 🔄 **Hot Reload**: Reload configuration files at runtime
- ✏️ **Read/Write**: Set configuration values and save to files
- 🪶 **Lightweight**: Minimal dependencies (only PyYAML required)
- 🎯 **Type Hints**: Full type hint support for better IDE experience
- 🚀 **No Singleton**: Multiple instances supported for flexibility

## Installation

Install from PyPI:

```bash
pip install pcf-config
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
from pcf_config import Config

# Create config instance with file path
config = Config("config.yaml")

# Get configuration values
db_host = config.get("database.host")  # Returns: "localhost"
db_port = config.get("database.port")  # Returns: 5432

# Get with default values
redis_host = config.get("redis.host", "localhost")
timeout = config.get("api.timeout", 30)

# Set new values
config.set("database.timeout", 30)
config.set("api.debug", True)

# Save changes to file
config.save()

print(f"Database: {db_host}:{db_port}")
print(f"Redis: {redis_host}")
```

## API Reference

### Config Class

The main class for configuration management:

```python
from pcf_config import Config

# Create config instance with file path
config = Config("config.yaml")

# Get configuration values
value = config.get("key")
value_with_default = config.get("key", "default")

# Set configuration values
config.set("new.key", "value")

# Save changes to file
config.save()

# Reload from file
config.reload()

# Check if key exists
if config.has_key("key"):
    print("Key exists")
```

#### Methods

##### `__init__(config_file: str)`
Initialize Config instance with configuration file path.

**Parameters:**
- `config_file` (str): Path to the YAML configuration file

##### `get(key: str, default: Any = ...) -> Any`
Get configuration value by key. Supports nested keys using dot notation.

**Parameters:**
- `key` (str): Configuration key, supports dot notation for nested keys
- `default` (Any): Default value if key doesn't exist

**Returns:**
- `Any`: The configuration value or default

**Raises:**
- `KeyError`: If the key doesn't exist and no default is provided

##### `set(key: str, value: Any) -> None`
Set configuration value. Creates nested structure if needed.

**Parameters:**
- `key` (str): Configuration key, supports dot notation for nested keys
- `value` (Any): Value to set

##### `save() -> None`
Save current configuration to the file.

##### `reload() -> None`
Reload the configuration file from disk.

##### `has_key(key: str) -> bool`
Check if a configuration key exists.

**Parameters:**
- `key` (str): Configuration key to check

**Returns:**
- `bool`: True if key exists, False otherwise

## Configuration File Location

PCF Config requires you to specify the configuration file path when creating a Config instance:

```python
config = Config("path/to/your/config.yaml")
```

## Examples

### Basic Usage

```python
from pcf_config import Config

# Create config instance
config = Config("config.yaml")

# config.yaml:
# app:
#   name: "My App"
#   version: "1.0.0"
#   debug: true
# database:
#   host: "localhost"
#   port: 5432

app_name = config.get("app.name")           # "My App"
app_version = config.get("app.version")     # "1.0.0"
db_host = config.get("database.host")       # "localhost"

# Using defaults for missing keys
cache_ttl = config.get("cache.ttl", 3600)  # 3600 (default)
debug_mode = config.get("app.debug", False)  # True (from config)
```

### Error Handling

```python
from pcf_config import Config

config = Config("config.yaml")

try:
    api_key = config.get("api.secret_key")
except KeyError:
    print("API key not configured!")
    api_key = None

# Or use default values to avoid exceptions
api_key = config.get("api.secret_key", None)
if not api_key:
    print("Warning: API key not configured!")
```

### Hot Reload

```python
from pcf_config import Config

config = Config("config.yaml")

# Initial load
print(config.get("app.name"))

# Modify config.yaml file externally...

# Reload configuration
config.reload()
print(config.get("app.name"))  # Updated value
```

### Read/Write Operations

```python
from pcf_config import Config

config = Config("config.yaml")

# Read existing values
db_host = config.get("database.host")

# Set new values
config.set("database.timeout", 30)
config.set("api.rate_limit", 1000)

# Save changes to file
config.save()

# Verify changes
print(config.get("database.timeout"))  # 30
print(config.get("api.rate_limit"))    # 1000
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
from pcf_config import Config

config = Config("config.yaml")

# Access nested configurations
primary_db = config.get("database.primary.host")
username = config.get("database.primary.credentials.username")

# Access array elements
services = config.get("services")
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

### v1.1.0
- **BREAKING**: Removed singleton pattern - Config now requires explicit file path
- **BREAKING**: Removed convenience functions `get_config` and `get_config_with_default`
- **NEW**: Added `set()` method for modifying configuration values
- **NEW**: Added `save()` method for persisting changes to file
- **IMPROVED**: `get()` method now supports default values with `...` sentinel
- **IMPROVED**: `reload()` method no longer requires file path parameter
- **REMOVED**: loguru dependency - now uses standard logging only
- **REMOVED**: All Chinese characters from source code
- **IMPROVED**: Better error handling and type hints

### v1.0.0
- Initial release
- Basic configuration loading from YAML files
- Support for nested keys with dot notation
- Default value support
- Hot reload functionality
- Singleton pattern implementation
- Optional loguru integration

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/pengcunfu/pcf-config/issues) on GitHub.
