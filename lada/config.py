"""
Configuration management for LADA.

Handles loading and saving configuration from .lada_config.yml
"""

from typing import Dict, Any, Optional, Union
from pathlib import Path
import yaml
from pydantic import BaseModel, Field, validator
import logging

logger = logging.getLogger(__name__)


class EngineConfig(BaseModel):
    """Configuration for a specific LLM engine."""
    host: str = Field(description="Engine API host URL")
    timeout: int = Field(default=120, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    extra_params: Dict[str, Any] = Field(default_factory=dict, description="Engine-specific parameters")


class ModelConfig(BaseModel):
    """Configuration for LLM models with per-mode selection."""
    # Per-mode model selection
    chat_model: Optional[str] = Field(default=None, description="Model for chat mode")
    plan_model: Optional[str] = Field(default=None, description="Model for plan mode")
    code_model: Optional[str] = Field(default=None, description="Model for code mode")
    
    # Legacy fields for backward compatibility
    default_model: str = Field(default="codellama:7b", description="Default model (legacy)")
    ollama_host: str = Field(default="http://localhost:11434", description="Ollama API host (legacy)")
    
    # Engine configurations
    engines: Dict[str, EngineConfig] = Field(default_factory=dict, description="Engine-specific configurations")
    
    # Global model parameters
    timeout: int = Field(default=120, description="Default request timeout in seconds")
    temperature: float = Field(default=0.7, description="Model temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")
    
    @validator('engines', pre=True)
    def ensure_engines_dict(cls, v):
        """Ensure engines is a dictionary and convert configurations."""
        if not isinstance(v, dict):
            return {}
        
        # Convert dict configurations to EngineConfig objects
        result = {}
        for engine_name, config in v.items():
            if isinstance(config, dict):
                result[engine_name] = EngineConfig(**config)
            elif isinstance(config, EngineConfig):
                result[engine_name] = config
        return result
    
    def get_model_for_mode(self, mode: str) -> str:
        """Get the configured model for a specific mode.
        
        Args:
            mode: One of 'chat', 'plan', or 'code'
            
        Returns:
            Model name for the mode, falling back to default_model
        """
        mode_field = f"{mode}_model"
        mode_model = getattr(self, mode_field, None)
        return mode_model or self.default_model
    
    def get_engine_config(self, engine: str) -> Optional[EngineConfig]:
        """Get configuration for a specific engine.
        
        Args:
            engine: Engine name (e.g., 'ollama', 'mlx')
            
        Returns:
            EngineConfig if found, None otherwise
        """
        return self.engines.get(engine)


class LADAConfig(BaseModel):
    """Main configuration for LADA."""
    version: int = Field(default=2, description="Configuration schema version")
    model: ModelConfig = Field(default_factory=ModelConfig)
    session_dir: Path = Field(default=Path(".lada/sessions"), description="Session storage directory")
    plan_dir: Path = Field(default=Path(".lada/plans"), description="Plan storage directory")
    backup_dir: Path = Field(default=Path(".lada/backups"), description="Backup storage directory")
    auto_save: bool = Field(default=True, description="Auto-save sessions")
    auto_save_interval: int = Field(default=300, description="Auto-save interval in seconds")


class ConfigManager:
    """Manages LADA configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path(".lada_config.yml")
        self.config = self._load_config()
    
    def _load_config(self) -> LADAConfig:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = yaml.safe_load(f) or {}
                
                # Migrate old configuration if needed
                data = self._migrate_config(data)
                
                return LADAConfig(**data)
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
                return LADAConfig()
        return LADAConfig()
    
    def _migrate_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate configuration from older versions.
        
        Args:
            data: Raw configuration data
            
        Returns:
            Migrated configuration data
        """
        version = data.get('version', 1)
        
        if version < 2:
            logger.info("Migrating configuration from version 1 to 2")
            
            # Migrate model configuration
            if 'model' in data:
                model_data = data['model']
                
                # If only default_model exists, set it for all modes
                if 'default_model' in model_data and not any(
                    k in model_data for k in ['chat_model', 'plan_model', 'code_model']
                ):
                    default = model_data['default_model']
                    logger.info(f"Setting all modes to use default model: {default}")
                    model_data['chat_model'] = default
                    model_data['plan_model'] = default
                    model_data['code_model'] = default
                
                # Migrate ollama_host to engines configuration
                if 'ollama_host' in model_data and 'engines' not in model_data:
                    logger.info("Migrating ollama_host to engines configuration")
                    model_data['engines'] = {
                        'ollama': {
                            'host': model_data['ollama_host'],
                            'timeout': model_data.get('timeout', 120)
                        }
                    }
                
                # Add default MLX engine config if not present
                if 'engines' in model_data and 'mlx' not in model_data.get('engines', {}):
                    model_data['engines']['mlx'] = {
                        'host': 'http://localhost:8000',
                        'timeout': 120
                    }
            
            # Update version
            data['version'] = 2
            
            # Save migrated configuration
            logger.info("Configuration migration complete")
            self._save_migration_backup(data)
        
        return data
    
    def _save_migration_backup(self, data: Dict[str, Any]):
        """Save a backup of the migrated configuration."""
        backup_path = self.config_path.with_suffix('.yml.backup')
        try:
            with open(backup_path, 'w') as f:
                yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
            logger.info(f"Migration backup saved to {backup_path}")
        except Exception as e:
            logger.warning(f"Failed to save migration backup: {e}")
    
    def save_config(self):
        """Save current configuration to file."""
        # Convert config to dict, handling Path objects
        config_dict = self.config.model_dump(exclude_none=True)
        
        # Convert Path objects to strings for YAML serialization
        def convert_paths(obj):
            if isinstance(obj, dict):
                return {k: convert_paths(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_paths(v) for v in obj]
            elif isinstance(obj, Path):
                return str(obj)
            return obj
        
        config_dict = convert_paths(config_dict)
        
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(
                config_dict,
                f,
                default_flow_style=False,
                sort_keys=False
            )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by dot-notation key."""
        parts = key.split('.')
        value = self.config
        
        for part in parts:
            if hasattr(value, part):
                value = getattr(value, part)
            else:
                return default
        
        return value
