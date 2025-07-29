# Test for Model Registry

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from lada.models.registry import ModelRegistry
from lada.models.ollama import OllamaLLM

def test_model_parsing():
    """Test model name parsing logic."""
    registry = ModelRegistry()
    
    # Test parsing
    test_cases = [
        ("codellama:7b", ("ollama", "codellama:7b")),  # Default to ollama
        ("ollama:codellama:7b", ("ollama", "codellama:7b")),  # Explicit ollama
        ("mlx:GLM-4.5-Air", ("mlx", "GLM-4.5-Air")),  # MLX model
        ("deepseek-coder:6.7b", ("ollama", "deepseek-coder:6.7b")),  # Another ollama
    ]
    
    print("Testing model name parsing:")
    for model_name, expected in test_cases:
        result = registry._parse_model_name(model_name)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {model_name} -> {result} (expected: {expected})")

async def test_model_creation():
    """Test model instantiation."""
    registry = ModelRegistry()
    
    print("\nTesting model creation:")
    
    # Test default ollama model
    try:
        llm1 = registry.get_llm("codellama:7b")
        print(f"  ✓ Created {type(llm1).__name__} with model={llm1.model}")
    except Exception as e:
        print(f"  ✗ Failed to create codellama:7b: {e}")
    
    # Test explicit ollama
    try:
        llm2 = registry.get_llm("ollama:codellama:7b") 
        print(f"  ✓ Created {type(llm2).__name__} with model={llm2.model}")
    except Exception as e:
        print(f"  ✗ Failed to create ollama:codellama:7b: {e}")
    
    # Test MLX
    try:
        llm3 = registry.get_llm("mlx:GLM-4.5-Air")
        print(f"  ✓ Created {type(llm3).__name__} with model={llm3.model}")
    except Exception as e:
        print(f"  ✗ Failed to create mlx:GLM-4.5-Air: {e}")
    
    # Test invalid engine
    try:
        llm4 = registry.get_llm("invalid:model")
        print(f"  ✗ Should have failed for invalid engine, but got {type(llm4).__name__}")
    except Exception as e:
        print(f"  ✓ Correctly rejected invalid engine: {e}")

# Run tests
test_model_parsing()
asyncio.run(test_model_creation())

