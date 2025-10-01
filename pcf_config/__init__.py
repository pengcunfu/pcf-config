#!/usr/bin/env python3
"""
PCF Config - A simple YAML configuration management library

This package provides a simple and flexible way to manage YAML configuration files
with support for nested keys, default values, and singleton pattern.
"""

from .config import Config, get_config, get_config_with_default

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "A simple YAML configuration management library"

__all__ = [
    "Config",
    "get_config", 
    "get_config_with_default",
    "__version__",
]
