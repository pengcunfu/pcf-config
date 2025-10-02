#!/usr/bin/env python3
"""
Tests for pcf_config module
"""

import os
import tempfile
import pytest
import yaml
from pathlib import Path

from pcf_config import Config


class TestConfig:
    """Test cases for Config class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        
        # Use config.example.yaml content
        self.test_config = {
            'test': {
                'data': 'test_data',
                'user': {
                    'name': 'test_user',
                    'age': 18
                }
            }
        }
        
        # Create temporary directory and config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'config.yaml')
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self.test_config, f)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        # Clean up temp files
        if os.path.exists(self.config_file):
            os.unlink(self.config_file)
        os.rmdir(self.temp_dir)
    
    def test_multiple_instances(self):
        """Test that Config can create multiple instances"""
        config1 = Config(self.config_file)
        config2 = Config(self.config_file)
        assert config1 is not config2
        # Both should have the same data
        assert config1.get('test.data') == config2.get('test.data')
    
    def test_get_simple_key(self):
        """Test getting simple configuration keys"""
        config = Config(self.config_file)
        assert config.get('test.data') == 'test_data'
        assert config.get('test.user.name') == 'test_user'
        assert config.get('test.user.age') == 18
    
    def test_get_nested_key(self):
        """Test getting nested configuration keys"""
        config = Config(self.config_file)
        assert config.get('test.user.name') == 'test_user'
        assert config.get('test.user.age') == 18
        assert config.get('test.data') == 'test_data'
    
    def test_get_nonexistent_key(self):
        """Test getting non-existent keys raises KeyError"""
        config = Config(self.config_file)
        with pytest.raises(KeyError):
            config.get('nonexistent.key')
    
    def test_get_with_default(self):
        """Test getting keys with default values"""
        config = Config(self.config_file)
        # Existing key should return actual value
        assert config.get('test.data', 'default') == 'test_data'
        # Non-existent key should return default
        assert config.get('nonexistent.key', 'default') == 'default'
        # No default specified should raise KeyError
        with pytest.raises(KeyError):
            config.get('nonexistent.key')
    
    def test_has_key(self):
        """Test checking if keys exist"""
        config = Config(self.config_file)
        assert config.has_key('test.data') is True
        assert config.has_key('test.user.name') is True
        assert config.has_key('nonexistent.key') is False
    
    def test_convenience_functions(self):
        """Test convenience functions"""
        config = Config(self.config_file)
        assert config.get('test.data') == 'test_data'
        assert config.get('test.user.name', 'default') == 'test_user'
        assert config.get('nonexistent.key', 'default') == 'default'
    
    def test_reload(self):
        """Test configuration reload"""
        config = Config(self.config_file)
        original_data = config.get('test.data')
        
        # Modify config file
        modified_config = self.test_config.copy()
        modified_config['test']['data'] = 'modified_data'
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(modified_config, f)
        
        # Reload and check
        config.reload()
        assert config.get('test.data') == 'modified_data'
        assert config.get('test.data') != original_data
    
    def test_missing_config_file(self):
        """Test behavior when config file is missing"""
        # Remove config file
        os.unlink(self.config_file)
        
        with pytest.raises(FileNotFoundError):
            Config('nonexistent.yaml')
    
    def test_invalid_yaml(self):
        """Test behavior with invalid YAML"""
        # Write invalid YAML
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write('invalid: yaml: content: [')
        
        with pytest.raises(yaml.YAMLError):
            Config(self.config_file)

    def test_set_and_save(self):
        """Test setting configuration values and saving"""
        config = Config(self.config_file)
        
        # Test setting simple key
        config.set('test.new_key', 'new_value')
        assert config.get('test.new_key') == 'new_value'
        
        # Test setting nested key
        config.set('test.user.email', 'test@example.com')
        assert config.get('test.user.email') == 'test@example.com'
        
        # Test setting new nested structure
        config.set('database.host', 'localhost')
        config.set('database.port', 3306)
        assert config.get('database.host') == 'localhost'
        assert config.get('database.port') == 3306
        
        # Test saving to file
        config.save()
        
        # Verify file was saved by reloading
        config.reload()
        assert config.get('test.new_key') == 'new_value'
        assert config.get('test.user.email') == 'test@example.com'
        assert config.get('database.host') == 'localhost'
        assert config.get('database.port') == 3306

    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        config = Config(self.config_file)
        
        # Test configuration not initialized scenarios
        # Force _config_data to None to test error handling
        original_data = config._config_data
        config._config_data = None
        
        with pytest.raises(RuntimeError, match="Configuration not initialized"):
            config.get('test.key')
            
        with pytest.raises(RuntimeError, match="Configuration not initialized"):
            config.set('test.key', 'value')
            
        with pytest.raises(RuntimeError, match="Configuration not initialized"):
            config.save()
            
        # Restore data
        config._config_data = original_data
        
        # Test configuration file path not set
        original_file = config._config_file
        config._config_file = None
        
        with pytest.raises(RuntimeError, match="Configuration file path not set"):
            config.save()
            
        with pytest.raises(RuntimeError, match="Configuration file path not set"):
            config.reload()
            
        # Restore file path
        config._config_file = original_file
        
        # Test save exception handling
        config._config_file = "/invalid/path/that/does/not/exist/config.yaml"
        with pytest.raises(RuntimeError, match="Failed to save configuration file"):
            config.save()


if __name__ == '__main__':
    pytest.main([__file__])
