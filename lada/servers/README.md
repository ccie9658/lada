# MLX Server for LADA

This server provides an Ollama-compatible API for MLX models, allowing LADA to use MLX models through the same interface as Ollama models.

## Quick Start

1. Start the server:
   ```bash
   python scripts/start_mlx_server.py
   ```

2. The server will start on `http://localhost:8000`

3. Use MLX models in LADA:
   ```bash
   lada chat --model mlx:Qwen2.5-0.5B-Instruct
   lada plan file.py --model mlx:Llama-3.2-1B-Instruct
   lada code app.py --model mlx:Qwen2.5-3B-Instruct
   ```

## Available Models

The server currently supports these models:
- `Qwen2.5-0.5B-Instruct` (~400MB)
- `Qwen2.5-1.5B-Instruct` (~1.2GB)
- `Qwen2.5-3B-Instruct` (~2.4GB)
- `Llama-3.2-1B-Instruct` (~800MB)
- `Llama-3.2-3B-Instruct` (~2.4GB)

## Server Options

```bash
# Start on a different port
python scripts/start_mlx_server.py --port 8080

# Pre-load a model
python scripts/start_mlx_server.py --load-model "Qwen2.5-0.5B-Instruct"

# Enable debug logging
python scripts/start_mlx_server.py --log-level DEBUG

# Enable auto-reload for development
python scripts/start_mlx_server.py --reload
```

## API Endpoints

- `GET /api/tags` - List available models
- `POST /api/generate` - Generate text completion
- `GET /health` - Check server health
- `POST /api/load` - Load a specific model
- `POST /api/unload` - Unload current model

## How It Works

1. The server loads MLX models from Hugging Face on demand
2. Models are cached in `~/.cache/huggingface/`
3. Only one model can be loaded at a time (to save memory)
4. The server automatically loads models when requested

## Troubleshooting

- **Server won't start**: Make sure port 8000 is free
- **Model won't load**: Check internet connection for first download
- **Out of memory**: Try smaller models or unload current model first
