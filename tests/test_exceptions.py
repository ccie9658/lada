# Test exception handling for multi-engine support

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lada.models.exceptions import (
    LLMException,
    LLMConnectionError,
    LLMEngineError,
    LLMConfigurationError
)

def test_exceptions():
    """Test that exceptions work correctly with engine information."""
    
    print("Testing LLMConnectionError with engine info:")
    
    # Test Ollama connection error
    try:
        raise LLMConnectionError("localhost:11434", engine="ollama")
    except LLMConnectionError as e:
        print(f"  ✓ Ollama error: {e}")
        print(f"    Details: {e.details}")
    
    # Test MLX connection error
    try:
        raise LLMConnectionError("localhost:8000", engine="mlx")
    except LLMConnectionError as e:
        print(f"  ✓ MLX error: {e}")
        print(f"    Details: {e.details}")
    
    # Test generic connection error
    try:
        raise LLMConnectionError("localhost:9999")
    except LLMConnectionError as e:
        print(f"  ✓ Generic error: {e}")
        print(f"    Details: {e.details}")
    
    print("\nTesting LLMEngineError:")
    
    # Test engine-specific error
    try:
        raise LLMEngineError("mlx", "Model loading failed", {"model": "GLM-4.5-Air"})
    except LLMEngineError as e:
        print(f"  ✓ Engine error: {e}")
        print(f"    Details: {e.details}")
    
    print("\nTesting LLMConfigurationError:")
    
    # Test configuration error
    try:
        raise LLMConfigurationError("Invalid MLX host configuration", config_key="engines.mlx.host")
    except LLMConfigurationError as e:
        print(f"  ✓ Config error: {e}")
        print(f"    Details: {e.details}")
    
    print("\n✅ All exception tests passed!")

if __name__ == "__main__":
    test_exceptions()
