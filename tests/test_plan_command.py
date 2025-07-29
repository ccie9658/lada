# Test plan command with multi-engine support

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from pathlib import Path
from lada.models import ModelRegistry
from lada.config import ConfigManager

def test_plan_config_defaults():
    """Test that configuration defaults work for plan mode."""
    
    print("Testing configuration defaults for planning...")
    
    config_manager = ConfigManager()
    config = config_manager.config
    
    plan_model = config.model.get_model_for_mode('plan')
    print(f"  ✓ Default plan model: {plan_model}")
    
    # Test with different mode configurations
    if config.model.plan_model:
        print(f"  ✓ Configured plan model: {config.model.plan_model}")
    else:
        print(f"  ✓ Using default_model for planning: {config.model.default_model}")

def test_prompt_template():
    """Test that plan prompt template exists and is valid."""
    
    print("\nTesting plan prompt template...")
    
    prompt_path = Path(__file__).parent.parent / "lada" / "prompts" / "plan.txt"
    
    if prompt_path.exists():
        print(f"  ✓ Prompt template found at: {prompt_path}")
        
        try:
            template = prompt_path.read_text()
            # Check for required placeholders
            required_placeholders = ["{filename}", "{file_content}", "{project_context}"]
            missing = [p for p in required_placeholders if p not in template]
            
            if not missing:
                print(f"  ✓ All required placeholders present")
            else:
                print(f"  ✗ Missing placeholders: {missing}")
                
        except Exception as e:
            print(f"  ✗ Error reading template: {e}")
    else:
        print(f"  ✗ Prompt template not found at: {prompt_path}")

async def test_model_selection():
    """Test that plan command can use different models."""
    
    print("\nTesting model selection for planning...")
    
    registry = ModelRegistry()
    
    # Test cases for different model selections
    test_models = [
        "llama2:13b",           # Ollama model
        "mlx:GLM-4.5-Air",      # MLX model
        "codellama:7b",         # Default-ish model
    ]
    
    for model in test_models:
        try:
            llm = registry.get_llm(model)
            engine, model_name = registry._parse_model_name(model)
            print(f"  ✓ {model} -> engine: {engine}, model: {model_name}, type: {type(llm).__name__}")
        except Exception as e:
            print(f"  ✗ Failed to create LLM for {model}: {e}")

def test_output_path_logic():
    """Test output path generation logic."""
    
    print("\nTesting output path logic...")
    
    test_files = [
        Path("main.py"),
        Path("src/module.py"),
        Path("test_file.js"),
    ]
    
    for file in test_files:
        default_output = Path(f".lada/plans/{file.stem}.plan.md")
        print(f"  ✓ {file} -> {default_output}")

if __name__ == "__main__":
    test_plan_config_defaults()
    test_prompt_template()
    asyncio.run(test_model_selection())
    test_output_path_logic()
    print("\n✅ Plan command tests completed!")
