# MLX Setup Guide for LADA

This guide covers setting up and using MLX models with LADA on Apple Silicon Macs.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Starting the MLX Server](#starting-the-mlx-server)
- [Available Models](#available-models)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Performance Tuning](#performance-tuning)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Apple Silicon Mac** (M1, M2, M3, etc.)
- **macOS 12.0+** (Monterey or later)
- **Python 3.12+**
- **LADA installed** with MLX dependencies

## Installation

### 1. Install MLX Dependencies

If you haven't already installed MLX dependencies with LADA:

```bash
cd /path/to/lada
source venv/bin/activate
pip install mlx mlx-lm transformers fastapi uvicorn
```

### 2. Verify Installation

```bash
python -c "import mlx; print(f'MLX version: {mlx.__version__}')"
```

## Starting the MLX Server

LADA includes a FastAPI server that provides Ollama-compatible endpoints for MLX models.

### Basic Start

```bash
# Activate LADA environment
source venv/bin/activate

# Start with defaults (localhost:8000)
python scripts/start_mlx_server.py
```

### Advanced Options

```bash
# Custom host and port
python scripts/start_mlx_server.py --host 0.0.0.0 --port 8080

# Enable debug logging
python scripts/start_mlx_server.py --log-level DEBUG

# Preload a model on startup
python scripts/start_mlx_server.py --preload-model Qwen2.5-0.5B-Instruct

# Enable auto-reload for development
python scripts/start_mlx_server.py --reload
```

### Running as a Background Service

```bash
# Start in background
nohup python scripts/start_mlx_server.py > mlx_server.log 2>&1 &

# Save the PID
echo $! > mlx_server.pid

# Stop the server
kill $(cat mlx_server.pid)
```

## Available Models

LADA's MLX server includes these pre-configured models:

| Model Name | Size | Best For | Memory Required |
|------------|------|----------|-----------------|
| `Qwen2.5-0.5B-Instruct` | ~400MB | Quick responses, testing | 2GB |
| `Qwen2.5-1.5B-Instruct` | ~1.2GB | Balanced performance | 4GB |
| `Qwen2.5-3B-Instruct` | ~2.4GB | High quality output | 6GB |
| `Llama-3.2-1B-Instruct` | ~800MB | General purpose | 3GB |
| `Llama-3.2-3B-Instruct` | ~2.4GB | Complex tasks | 6GB |
| `GLM-4.5-Air` | Coming soon | Advanced reasoning | TBD |

### Model Download

Models are automatically downloaded from Hugging Face on first use:
- Download location: `~/.cache/huggingface/hub/`
- First-time download requires internet connection
- Subsequent uses work offline

## Configuration

### Basic MLX Configuration

In your `.lada_config.yml`:

```yaml
version: 2
model:
  # Use MLX for specific modes
  chat_model: "mlx:Qwen2.5-1.5B-Instruct"
  plan_model: "mlx:Qwen2.5-3B-Instruct"
  code_model: "mlx:Llama-3.2-3B-Instruct"
  
  engines:
    mlx:
      host: "http://localhost:8000"
      timeout: 180
```

### Per-Command Model Override

```bash
# Use MLX model for a specific command
python lada.py chat --model mlx:Llama-3.2-1B-Instruct
python lada.py plan file.py --model mlx:Qwen2.5-3B-Instruct
python lada.py code "data parser" --model mlx:Llama-3.2-3B-Instruct
```

## Usage Examples

### Example 1: Interactive Chat with MLX

```bash
# Start MLX server (in separate terminal)
python scripts/start_mlx_server.py

# Use MLX for chat
python lada.py chat --model mlx:Qwen2.5-1.5B-Instruct
```

### Example 2: Code Generation with MLX

```bash
# Generate code using MLX
python lada.py code "FastAPI endpoint for user authentication" \
  --model mlx:Llama-3.2-3B-Instruct \
  --output auth_endpoint.py
```

### Example 3: Mixed Engine Setup

Configure different engines for different tasks:

```yaml
model:
  chat_model: "codellama:7b"              # Ollama for chat
  plan_model: "mlx:Qwen2.5-3B-Instruct"   # MLX for planning
  code_model: "deepseek-coder:6.7b"       # Ollama for coding
```

## Performance Tuning

### 1. Model Selection

- **Small models** (0.5B-1B): Fast responses, good for chat and simple tasks
- **Medium models** (1.5B-3B): Balanced performance and quality
- **Large models** (3B+): Best quality but slower

### 2. Server Optimization

```bash
# Preload frequently used model
python scripts/start_mlx_server.py --preload-model Qwen2.5-1.5B-Instruct

# Adjust timeout for large models
# In .lada_config.yml:
engines:
  mlx:
    timeout: 300  # 5 minutes for large models
```

### 3. Memory Management

- Close unused applications to free RAM
- Use smaller models if experiencing memory issues
- Monitor Activity Monitor for memory usage

### 4. Generation Parameters

Note: MLX currently only supports `max_tokens` parameter:

```yaml
model:
  max_tokens: 2048  # Adjust based on needs
  # temperature, top_p not yet supported by MLX
```

## Troubleshooting

### Server Won't Start

```bash
# Check if port is already in use
lsof -i :8000

# Use different port
python scripts/start_mlx_server.py --port 8001
```

### Model Download Issues

```bash
# Clear cache and retry
rm -rf ~/.cache/huggingface/hub/models--mlx-community--*

# Manual download test
python -c "from mlx_lm import load; load('mlx-community/Qwen2.5-0.5B-Instruct-4bit')"
```

### Memory Errors

- Use smaller models
- Close other applications
- Restart Mac to clear memory
- Check available memory: `vm_stat | grep free`

### Slow Performance

1. Ensure you're on Apple Silicon (not Intel Mac)
2. Check CPU usage: `top -o cpu`
3. Try smaller model
4. Disable other GPU-intensive apps

### Connection Refused

```bash
# Verify server is running
curl http://localhost:8000/health

# Check server logs
python scripts/start_mlx_server.py --log-level DEBUG
```

### Model Not Found

```bash
# List available models
curl http://localhost:8000/v1/models

# Check exact model name in server response
python lada.py chat --model mlx:ModelNameFromList
```

## Advanced Topics

### Custom Model Addition

To add new MLX models, edit `lada/servers/mlx_wrapper.py`:

```python
self._available_models = {
    # ... existing models ...
    "YourModel": "mlx-community/your-model-id",
}
```

### API Endpoints

The MLX server provides these endpoints:

- `GET /health` - Server health check
- `GET /v1/models` - List available models
- `POST /v1/completions` - Generate text (Ollama-compatible)
- `POST /models/{model_name}/load` - Load specific model
- `POST /models/unload` - Unload current model

### Direct API Usage

```bash
# Generate text via API
curl -X POST http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen2.5-0.5B-Instruct",
    "prompt": "Hello, how are you?",
    "max_tokens": 100
  }'
```

## Next Steps

1. Start with small models to test your setup
2. Experiment with different models for different tasks
3. Monitor performance and adjust configuration
4. Share your experience and optimizations with the community

For more help, see the [main README](../README.md) or open an issue on GitHub.
