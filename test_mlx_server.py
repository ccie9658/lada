#!/usr/bin/env python3
"""Test the MLX server functionality."""

import requests
import time
import subprocess
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_server():
    """Test the MLX server endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing MLX Server...\n")
    
    # 1. Test health endpoint
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to server: {e}")
        print("💡 Start the server with: python scripts/start_mlx_server.py")
        return False
    
    # 2. Test model listing
    print("\n2️⃣ Testing model listing...")
    try:
        response = requests.get(f"{base_url}/api/tags")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['models'])} models:")
            for model in data['models']:
                print(f"   - {model['name']} ({model['size']})")
        else:
            print(f"❌ Model listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False
    
    # 3. Test generation with the already downloaded model
    print("\n3️⃣ Testing text generation...")
    model_name = "Qwen2.5-0.5B-Instruct"  # We downloaded this earlier
    
    try:
        payload = {
            "model": model_name,
            "prompt": "What is Python?",
            "options": {
                "num_predict": 50,
                "temperature": 0.7
            }
        }
        
        print(f"📤 Sending request to generate with {model_name}...")
        start_time = time.time()
        
        response = requests.post(f"{base_url}/api/generate", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            elapsed = time.time() - start_time
            print(f"✅ Generation successful in {elapsed:.1f}s")
            print(f"📝 Response: {data['response'][:100]}...")
            print(f"📊 Tokens: {data['eval_count']} generated, {data['prompt_eval_count']} prompt")
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return False
    
    print("\n✨ All tests passed!")
    return True


if __name__ == "__main__":
    # First, let's check if we can import the server modules
    try:
        from lada.servers.mlx_wrapper import MLXModelWrapper
        from lada.servers.mlx_server import app
        print("✅ Server modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import server modules: {e}")
        sys.exit(1)
    
    # Run the tests
    if test_server():
        print("\n🎉 MLX server is working correctly!")
    else:
        print("\n❌ Some tests failed. Please check the server.")
