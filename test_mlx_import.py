#!/usr/bin/env python3
"""Quick test of MLX server components without running the server."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("🧪 Testing MLX Server Components...\n")

# Test imports
print("1️⃣ Testing imports...")
try:
    from lada.servers.mlx_wrapper import MLXModelWrapper, GenerationConfig
    from lada.servers.mlx_server import app, GenerateRequest, GenerateResponse
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test MLX wrapper
print("\n2️⃣ Testing MLX wrapper...")
wrapper = MLXModelWrapper()

# List models
models = wrapper.list_models()
print(f"✅ Found {len(models)} models:")
for model in models:
    info = wrapper.get_model_info(model)
    print(f"   - {model}: {info['size']} (downloaded: {info['is_downloaded']})")

# Test model info
print("\n3️⃣ Testing model info for Qwen2.5-0.5B-Instruct...")
info = wrapper.get_model_info("Qwen2.5-0.5B-Instruct")
if info:
    print(f"✅ Model info retrieved:")
    print(f"   - Model ID: {info['model_id']}")
    print(f"   - Size: {info['size']}")
    print(f"   - Downloaded: {info['is_downloaded']}")
    print(f"   - Loaded: {info['is_loaded']}")
else:
    print("❌ Failed to get model info")

# Test API structure
print("\n4️⃣ Testing API request/response models...")
try:
    # Create a sample request
    request = GenerateRequest(
        model="Qwen2.5-0.5B-Instruct",
        prompt="Hello",
        options={"temperature": 0.7}
    )
    print(f"✅ GenerateRequest created: model={request.model}")
    
    # Create a sample response
    response = GenerateResponse(
        model="test",
        created_at="2024-01-01T00:00:00",
        response="Test response",
        done=True,
        total_duration=1000000,
        prompt_eval_count=10,
        eval_count=20,
        eval_duration=500000
    )
    print(f"✅ GenerateResponse created: {response.response}")
    
except Exception as e:
    print(f"❌ API model test failed: {e}")

print("\n✨ Component tests completed!")
print("\nTo test the full server:")
print("1. Start the server: python scripts/start_mlx_server.py")
print("2. Run the test: python test_mlx_server.py")
