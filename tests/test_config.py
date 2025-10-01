#!/usr/bin/env python3
"""
Tests for pcf_config module
"""

import os
import tempfile
import pytest
import yaml
from pathlib import Path

from pcf_config import Config, get_config, get_config_with_default


class TestConfig:
    """Test cases for Config class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Reset singleton instance for each test
        Config._instance = None
        Config._config_data = None
        
        # Use config.example.yaml content
        self.test_config = {
            'test': {
                'data': '测试数据',
                'user': {
                    'name': '张三',
                    'age': 18
                }
            }
        }
        
        # Create temporary directory and config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'config.yaml')
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self.test_config, f)
        
        # Change to temp directory so config.yaml is found
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        # Clean up temp files
        if os.path.exists(self.config_file):
            os.unlink(self.config_file)
        os.rmdir(self.temp_dir)
    
    def test_singleton_pattern(self):
        """Test that Config follows singleton pattern"""
        config1 = Config()
        config2 = Config()
        assert config1 is config2
    
    def test_get_simple_key(self):
        """Test getting simple configuration keys"""
        config = Config()
        assert config.get('test.data') == '测试数据'
        assert config.get('test.user.name') == '张三'
        assert config.get('test.user.age') == 18
    
    def test_get_nested_key(self):
        """Test getting nested configuration keys"""
        config = Config()
        assert config.get('test.user.name') == '张三'
        assert config.get('test.user.age') == 18
        assert config.get('test.data') == '测试数据'
    
    def test_get_nonexistent_key(self):
        """Test getting non-existent keys raises KeyError"""
        config = Config()
        with pytest.raises(KeyError):
            config.get('nonexistent.key')
    
    def test_get_with_default(self):
        """Test getting keys with default values"""
        config = Config()
        # Existing key should return actual value
        assert config.get_with_default('test.data', 'default') == '测试数据'
        # Non-existent key should return default
        assert config.get_with_default('nonexistent.key', 'default') == 'default'
        # No default specified should return None
        assert config.get_with_default('nonexistent.key') is None
    
    def test_has_key(self):
        """Test checking if keys exist"""
        config = Config()
        assert config.has_key('test.data') is True
        assert config.has_key('test.user.name') is True
        assert config.has_key('nonexistent.key') is False
    
    def test_convenience_functions(self):
        """Test convenience functions"""
        assert get_config('test.data') == '测试数据'
        assert get_config_with_default('test.user.name', 'default') == '张三'
        assert get_config_with_default('nonexistent.key', 'default') == 'default'
    
    def test_reload(self):
        """Test configuration reload"""
        config = Config()
        original_data = config.get('test.data')
        
        # Modify config file
        modified_config = self.test_config.copy()
        modified_config['test']['data'] = '修改后的数据'
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(modified_config, f)
        
        # Reload and check
        config.reload()
        assert config.get('test.data') == '修改后的数据'
        assert config.get('test.data') != original_data
    
    def test_missing_config_file(self):
        """Test behavior when config file is missing"""
        # Remove config file
        os.unlink(self.config_file)
        
        # Reset singleton
        Config._instance = None
        Config._config_data = None
        
        with pytest.raises(FileNotFoundError):
            Config()
    
    def test_invalid_yaml(self):
        """Test behavior with invalid YAML"""
        # Write invalid YAML
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write('invalid: yaml: content: [')
        
        # Reset singleton
        Config._instance = None
        Config._config_data = None
        
        with pytest.raises(yaml.YAMLError):
            Config()


if __name__ == '__main__':
    pytest.main([__file__])
