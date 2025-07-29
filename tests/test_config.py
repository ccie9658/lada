"""Tests for Configuration System - Multi-engine support and migration."""

import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, mock_open

from lada.config import ConfigManager, LADAConfig, ModelConfig, EngineConfig

class TestConfigStructure:
    """Test new configuration structure and features."""
    
    def test_per_mode_models(self):
        """Test configuration with different models for each mode."""
        config = LADAConfig(
            version=2,
            model=ModelConfig(
                chat_model="codellama:7b",
                plan_model="mlx:GLM-4.5-Air",
                code_model="deepseek-coder:6.7b",
                engines={
                    "ollama": EngineConfig(
                        host="http://localhost:11434",
                        timeout=120
                    ),
                    "mlx": EngineConfig(
                        host="http://localhost:8000",
                        timeout=180,
                        extra_params={"gpu_layers": 32}
                    )
                }
            )
        )
        
        # Test per-mode model retrieval
        assert config.model.get_model_for_mode("chat") == "codellama:7b"
        assert config.model.get_model_for_mode("plan") == "mlx:GLM-4.5-Air"
        assert config.model.get_model_for_mode("code") == "deepseek-coder:6.7b"
        
        # Test engine config retrieval
        ollama_config = config.model.get_engine_config("ollama")
        mlx_config = config.model.get_engine_config("mlx")
        
        assert ollama_config.host == "http://localhost:11434"
        assert ollama_config.timeout == 120
        assert mlx_config.host == "http://localhost:8000"
        assert mlx_config.timeout == 180
        assert mlx_config.extra_params["gpu_layers"] == 32
    
    def test_default_model_fallback(self):
        """Test fallback to default_model when per-mode models not set."""
        config = ModelConfig(
            default_model="llama2:7b",
            ollama_host="http://localhost:11434"
        )
        
        # Should fall back to default_model for all modes
        assert config.get_model_for_mode('chat') == "llama2:7b"
        assert config.get_model_for_mode('plan') == "llama2:7b"
        assert config.get_model_for_mode('code') == "llama2:7b"
    
    def test_engine_config_creation(self):
        """Test creating engine configurations."""
        config = ModelConfig(
            engines={
                "ollama": EngineConfig(host="http://localhost:11434"),
                "mlx": EngineConfig(host="http://localhost:8000", timeout=180)
            }
        )
        
        assert "ollama" in config.engines
        assert "mlx" in config.engines
        
        # Check values
        ollama_engine = config.engines["ollama"]
        assert ollama_engine.host == "http://localhost:11434"
        assert ollama_engine.timeout == 120  # Default
        
        mlx_engine = config.engines["mlx"]
        assert mlx_engine.host == "http://localhost:8000"
        assert mlx_engine.timeout == 180  # Custom
    

def test_config_migration():
    """Test configuration migration from v1 to v2 format."""
    v1_config = {
        "model": {
            "default_model": "codellama:13b",
            "ollama_host": "http://localhost:11434",
            "timeout": 150,
            "temperature": 0.8
        },
        "session_dir": ".lada/sessions",
        "auto_save": True
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.safe_dump(v1_config, f)
        temp_path = Path(f.name)

    try:
        # Load with ConfigManager, triggering migration
        manager = ConfigManager(config_path=temp_path)
        config = manager.config

        assert config.version == 2
        assert config.model.chat_model == "codellama:13b"
        assert config.model.plan_model == "codellama:13b"
        assert config.model.code_model == "codellama:13b"

        # Check engine configuration
        ollama_engine = config.model.engines.get("ollama")
        mlx_engine = config.model.engines.get("mlx")

        assert ollama_engine.host == "http://localhost:11434"
        assert ollama_engine.timeout == 150
        # Check backup was created
        backup_path = temp_path.with_suffix('.yml.backup')
        assert backup_path.exists()
        backup_path.unlink()  # Clean up backup

    finally:
        temp_path.unlink()

def test_config_backward_compatibility():
    """Test backward compatibility with old configuration versions."""
    config = ModelConfig(
        default_model="llama2:7b",
        ollama_host="http://localhost:11434"
    )

    assert config.get_model_for_mode('chat') == "llama2:7b"
    assert config.get_model_for_mode('plan') == "llama2:7b"
    assert config.get_model_for_mode('code') == "llama2:7b"


def test_config_saving():
    """Test creating, saving, and loading a configuration file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir) / "test_config.yml"
        
        # Create manager and default config
        manager = ConfigManager(config_path=temp_path)
        
        # Modify configuration
        manager.config.model.chat_model = "ollama:mistral"
        manager.config.model.plan_model = "mlx:GLM-4.5-Air"
        manager.config.model.engines["mlx"] = EngineConfig(
            host="http://localhost:8001",
            timeout=200
        )
        
        # Save
        manager.save_config()
        
        # Reload and verify
        with open(temp_path, 'r') as f:
            saved_data = yaml.safe_load(f)
        
        assert saved_data.get('version') == 2
        assert saved_data['model']['chat_model'] == "ollama:mistral"
        assert saved_data['model']['plan_model'] == "mlx:GLM-4.5-Air"
        assert saved_data['model']['engines']['mlx']['host'] == "http://localhost:8001"


class TestConfigManager:
    """Test ConfigManager functionality."""
    
    def test_default_config_creation(self):
        """Test that ConfigManager creates default config when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test_config.yml"
            
            # Create manager with non-existent config file
            manager = ConfigManager(config_path=config_path)
            
            # Should have default config values
            assert manager.config.version == 2
            assert manager.config.model.default_model == "codellama:7b"
            
            # Save config and verify file is created
            manager.save_config()
            assert config_path.exists()
    
    def test_invalid_config_fallback(self):
        """Test that invalid config falls back to defaults."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as temp_file:
            # Write invalid YAML data
            temp_file.write("invalid: yaml: --:")
            temp_file.flush()
            temp_path = Path(temp_file.name)
        
        try:
            # Should log warning and return default config
            manager = ConfigManager(config_path=temp_path)
            assert manager.config.version == 2  # Falls back to default
            assert manager.config.model.default_model == "codellama:7b"
        finally:
            temp_path.unlink()


# For standalone testing
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
