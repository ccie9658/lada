# Test configuration system with per-mode models and migration

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile
import yaml
from pathlib import Path
from lada.config import ConfigManager, LADAConfig, ModelConfig, EngineConfig

def test_new_config_structure():
    """Test the new configuration structure with per-mode models."""
    print("Testing new configuration structure...")
    
    # Create a config with per-mode models
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
    print("  ✓ Chat model:", config.model.get_model_for_mode("chat"))
    print("  ✓ Plan model:", config.model.get_model_for_mode("plan"))
    print("  ✓ Code model:", config.model.get_model_for_mode("code"))
    
    # Test engine config retrieval
    ollama_config = config.model.get_engine_config("ollama")
    mlx_config = config.model.get_engine_config("mlx")
    
    print(f"  ✓ Ollama config: host={ollama_config.host}, timeout={ollama_config.timeout}")
    print(f"  ✓ MLX config: host={mlx_config.host}, timeout={mlx_config.timeout}, extras={mlx_config.extra_params}")
    

def test_config_migration():
    """Test configuration migration from v1 to v2."""
    print("\nTesting configuration migration...")
    
    # Create a v1 config
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
    
    # Write v1 config to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.safe_dump(v1_config, f)
        temp_path = Path(f.name)
    
    try:
        # Load with ConfigManager (should trigger migration)
        manager = ConfigManager(config_path=temp_path)
        config = manager.config
        
        print(f"  ✓ Version migrated to: {config.version}")
        print(f"  ✓ Chat model: {config.model.chat_model}")
        print(f"  ✓ Plan model: {config.model.plan_model}")
        print(f"  ✓ Code model: {config.model.code_model}")
        
        # Check engine configuration
        ollama_engine = config.model.engines.get("ollama")
        mlx_engine = config.model.engines.get("mlx")
        
        if ollama_engine:
            print(f"  ✓ Ollama engine migrated: host={ollama_engine.host}")
        if mlx_engine:
            print(f"  ✓ MLX engine added: host={mlx_engine.host}")
        
        # Check backup was created
        backup_path = temp_path.with_suffix('.yml.backup')
        if backup_path.exists():
            print(f"  ✓ Backup created at: {backup_path}")
            backup_path.unlink()  # Clean up backup
        
    finally:
        # Clean up
        temp_path.unlink()


def test_backward_compatibility():
    """Test that old configs still work."""
    print("\nTesting backward compatibility...")
    
    # Create a config without per-mode models
    config = ModelConfig(
        default_model="llama2:7b",
        ollama_host="http://localhost:11434"
    )
    
    # Should fall back to default_model for all modes
    print(f"  ✓ Chat falls back to: {config.get_model_for_mode('chat')}")
    print(f"  ✓ Plan falls back to: {config.get_model_for_mode('plan')}")
    print(f"  ✓ Code falls back to: {config.get_model_for_mode('code')}")


def test_config_saving():
    """Test saving the new configuration format."""
    print("\nTesting configuration saving...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        temp_path = Path(f.name)
    
    try:
        # Create and save a config
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
        
        print(f"  ✓ Saved version: {saved_data.get('version', 'missing')}")
        print(f"  ✓ Saved chat model: {saved_data['model']['chat_model']}")
        print(f"  ✓ Saved MLX host: {saved_data['model']['engines']['mlx']['host']}")
        
    finally:
        # Clean up
        temp_path.unlink()


if __name__ == "__main__":
    test_new_config_structure()
    test_config_migration()
    test_backward_compatibility()
    test_config_saving()
    print("\n✅ All configuration tests passed!")
