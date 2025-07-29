"""Tests for Model Registry - Core multi-engine support."""

import pytest
from unittest.mock import Mock, patch

from lada.models.registry import ModelRegistry
from lada.models.ollama import OllamaLLM
from lada.models.mlx import MLXLLM
from lada.models.exceptions import LLMException
from lada.config import EngineConfig


class TestModelRegistry:
    """Test cases for the ModelRegistry class."""
    
    def test_model_name_parsing(self):
        """Test parsing of model names with engine prefixes."""
        registry = ModelRegistry()
        
        # Test cases: (input, expected_output)
        test_cases = [
            # Default to ollama (no prefix)
            ("codellama:7b", ("ollama", "codellama:7b")),
            ("llama2:13b", ("ollama", "llama2:13b")),
            ("deepseek-coder:6.7b", ("ollama", "deepseek-coder:6.7b")),
            
            # Explicit ollama prefix
            ("ollama:codellama:7b", ("ollama", "codellama:7b")),
            ("ollama:llama2:latest", ("ollama", "llama2:latest")),
            
            # MLX models
            ("mlx:GLM-4.5-Air", ("mlx", "GLM-4.5-Air")),
            ("mlx:Qwen2.5-0.5B-Instruct", ("mlx", "Qwen2.5-0.5B-Instruct")),
            
            # Edge cases
            ("mlx:", ("mlx", "")),  # Empty model name
            (":", ("ollama", ":")),  # Just colon defaults to ollama
        ]
        
        for model_name, expected in test_cases:
            engine, model = registry._parse_model_name(model_name)
            assert (engine, model) == expected, f"Failed for {model_name}"
    
    def test_get_llm_ollama(self):
        """Test creating Ollama LLM instances."""
        registry = ModelRegistry()
        
        # Test default ollama model
        llm = registry.get_llm("codellama:7b", host="http://localhost:11434")
        assert isinstance(llm, OllamaLLM)
        assert llm.model == "codellama:7b"
        assert llm.host == "http://localhost:11434"
        
        # Test explicit ollama prefix
        llm2 = registry.get_llm("ollama:llama2:13b")
        assert isinstance(llm2, OllamaLLM)
        assert llm2.model == "llama2:13b"
    
    def test_get_llm_mlx(self):
        """Test creating MLX LLM instances."""
        registry = ModelRegistry()
        
        # Test MLX model creation
        llm = registry.get_llm("mlx:GLM-4.5-Air", host="http://localhost:8000")
        assert isinstance(llm, MLXLLM)
        assert llm.model == "GLM-4.5-Air"
        assert llm.host == "http://localhost:8000"
    
    def test_get_llm_custom_params(self):
        """Test creating LLM with custom parameters."""
        registry = ModelRegistry()
        
        # Test with custom host and timeout
        llm = registry.get_llm(
            "codellama:7b", 
            host="http://custom-host:9999",
            timeout=300
        )
        assert isinstance(llm, OllamaLLM)
        assert llm.host == "http://custom-host:9999"
        assert llm.timeout == 300
    
    def test_get_llm_unknown_engine_defaults_to_ollama(self):
        """Test that unknown engine prefixes default to ollama."""
        registry = ModelRegistry()
        
        # Unknown engine prefix should be treated as part of the model name
        llm = registry.get_llm("invalid:model")
        assert isinstance(llm, OllamaLLM)
        assert llm.model == "invalid:model"  # Whole string becomes the model name
    
    def test_list_engines(self):
        """Test listing available engines."""
        registry = ModelRegistry()
        
        engines = registry.list_engines()
        assert "ollama" in engines
        assert "mlx" in engines
    
    def test_registry_singleton_behavior(self):
        """Test that multiple registry instances share the same state."""
        registry1 = ModelRegistry()
        registry2 = ModelRegistry()
        
        # Both should have the same engine mappings
        assert registry1._engines == registry2._engines
        assert "ollama" in registry1._engines
        assert "mlx" in registry1._engines


# For standalone testing
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

