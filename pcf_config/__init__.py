#!/usr/bin/env python3
"""
PCF Config - A simple YAML configuration management library

This package provides a simple and flexible way to manage YAML configuration files
with support for nested keys, default values, and read/write operations.
"""

from .config import Config

__version__ = "1.1.8"
__author__ = "pengcunfu"
__email__ = "3173484026@qq.com"
__description__ = "A simple YAML configuration management library"

__all__ = [
    "Config",
    "__version__",
]
