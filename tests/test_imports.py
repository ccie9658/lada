# Test all model package imports

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all model package exports are importable."""
    
    print("Testing model package imports...")
    
    try:
        # Import everything from __all__
        from lada.models import (
            # Base classes
            BaseLLM,
            LLMResponse,
            # Implementations
            OllamaLLM,
            MLXLLM,
            # Registry
            ModelRegistry,
            # Exceptions
            LLMException,
            LLMConnectionError,
            LLMTimeoutError,
            LLMModelNotFoundError,
            LLMContextLengthExceeded,
            LLMResponseError,
            LLMEngineError,
            LLMConfigurationError,
        )
        print("  ✓ All imports successful")
        
        # Test instantiation
        print("\nTesting instantiation:")
        
        # Test registry
        registry = ModelRegistry()
        print(f"  ✓ ModelRegistry created with engines: {registry.list_engines()}")
        
        # Test Ollama
        ollama = OllamaLLM(model="test:model")
        print(f"  ✓ OllamaLLM created with model: {ollama.model}")
        
        # Test MLX
        mlx = MLXLLM(model="test:mlx")
        print(f"  ✓ MLXLLM created with model: {mlx.model}")
        
        print("\n✅ All import tests passed!")
        
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_imports()
