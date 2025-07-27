"""
Configuration management for LADA.

Handles loading and saving configuration from .lada_config.yml
"""

from typing import Dict, Any, Optional
from pathlib import Path
import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for LLM models."""
    default_model: str = Field(default="codellama:7b", description="Default model to use")
    ollama_host: str = Field(default="http://localhost:11434", description="Ollama API host")
    timeout: int = Field(default=120, description="Request timeout in seconds")
    temperature: float = Field(default=0.7, description="Model temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")


class LADAConfig(BaseModel):
    """Main configuration for LADA."""
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
                return LADAConfig(**data)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                return LADAConfig()
        return LADAConfig()
    
    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(
                self.config.model_dump(exclude_none=True),
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
