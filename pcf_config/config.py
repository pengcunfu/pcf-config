#!/usr/bin/env python3
"""
Configuration file reading module
Supports reading configuration from YAML files with simple get methods
"""

import yaml
import os
from typing import Any


class Config:
    """Configuration management class"""

    def __init__(self, config_file: str):
        self._config_data = None
        self._config_file = config_file
        self._load_config(config_file)

    def _load_config(self, config_file: str):
        """Load configuration file"""
        # Check if configuration file exists
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found")

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                self._config_data = yaml.safe_load(f)
        except Exception as e:
            raise

    def get(self, key: str, default: Any = ...) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key, supports dot-separated nested keys like "llm.douyin.api_key"
            default: Default value if key does not exist

        Returns:
            Any: Configuration value or default value

        Raises:
            KeyError: When configuration key does not exist and no default is provided
        """
        if self._config_data is None:
            raise RuntimeError("Configuration not initialized")

        # Split key by dots
        keys = key.split(".")
        value = self._config_data

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError) as e:
            if default is not ...:
                return default
            raise KeyError(f"Configuration key '{key}' does not exist") from e

    def has_key(self, key: str) -> bool:
        """
        Check if configuration key exists

        Args:
            key: Configuration key

        Returns:
            bool: Whether the key exists
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def set(self, key: str, value: Any):
        """
        Set configuration value

        Args:
            key: Configuration key, supports dot-separated nested keys
            value: Configuration value
        """
        if self._config_data is None:
            raise RuntimeError("Configuration not initialized")

        # Split key by dots
        keys = key.split(".")
        data = self._config_data

        # Navigate to parent of last key
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]

        # Set value of last key
        data[keys[-1]] = value

    def save(self):
        """
        Save configuration to file
        """
        if self._config_data is None:
            raise RuntimeError("Configuration not initialized")

        if self._config_file is None:
            raise RuntimeError("Configuration file path not set")

        try:
            with open(self._config_file, "w", encoding="utf-8") as f:
                yaml.safe_dump(
                    self._config_data, f, default_flow_style=False, allow_unicode=True
                )
        except Exception as e:
            raise RuntimeError(f"Failed to save configuration file: {e}") from e

    def reload(self):
        """Reload configuration file"""
        if self._config_file is None:
            raise RuntimeError("Configuration file path not set")
        self._config_data = None
        self._load_config(self._config_file)
