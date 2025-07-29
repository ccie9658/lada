# Test chat command with multi-engine support

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from lada.models import ModelRegistry
from lada.config import ConfigManager

def test_model_parsing_for_chat():
    """Test that chat command properly handles different model formats."""
    
    print("Testing model parsing for chat command...")
    
    registry = ModelRegistry()
    
    test_cases = [
        ("codellama:7b", "ollama", "codellama:7b"),
        ("ollama:llama2:13b", "ollama", "llama2:13b"),
        ("mlx:GLM-4.5-Air", "mlx", "GLM-4.5-Air"),
        ("mistral:latest", "ollama", "mistral:latest"),
    ]
    
    for model_string, expected_engine, expected_model in test_cases:
        engine, model = registry._parse_model_name(model_string)
        if engine == expected_engine and model == expected_model:
            print(f"  ✓ {model_string} -> engine: {engine}, model: {model}")
        else:
            print(f"  ✗ {model_string} -> got ({engine}, {model}), expected ({expected_engine}, {expected_model})")

def test_config_defaults():
    """Test that configuration defaults work for chat mode."""
    
    print("\nTesting configuration defaults for chat...")
    
    config_manager = ConfigManager()
    config = config_manager.config
    
    chat_model = config.model.get_model_for_mode('chat')
    print(f"  ✓ Default chat model: {chat_model}")
    
    # Test with different mode configurations
    if config.model.chat_model:
        print(f"  ✓ Configured chat model: {config.model.chat_model}")
    else:
        print(f"  ✓ Using default_model for chat: {config.model.default_model}")

async def test_llm_instantiation():
    """Test that we can instantiate LLMs for different engines."""
    
    print("\nTesting LLM instantiation...")
    
    registry = ModelRegistry()
    
    # Test Ollama instantiation
    try:
        ollama_llm = registry.get_llm("codellama:7b")
        print(f"  ✓ Created Ollama LLM: {type(ollama_llm).__name__}")
    except Exception as e:
        print(f"  ✗ Failed to create Ollama LLM: {e}")
    
    # Test MLX instantiation
    try:
        mlx_llm = registry.get_llm("mlx:GLM-4.5-Air")
        print(f"  ✓ Created MLX LLM: {type(mlx_llm).__name__}")
    except Exception as e:
        print(f"  ✗ Failed to create MLX LLM: {e}")

if __name__ == "__main__":
    test_model_parsing_for_chat()
    test_config_defaults()
    asyncio.run(test_llm_instantiation())
    print("\n✅ Chat command tests completed!")
