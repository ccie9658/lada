# LADA - Local AI-Driven Development Assistant

A local AI assistant workflow that mimics agent-style development setups using Ollama and open-source LLMs, allowing for structured, iterative, agent-guided software development.

## Architecture Summary

LADA is designed with a modular architecture to ensure scalability and maintainability:

- **CLI Interface** (`lada.py`): Main entry point, built using Typer and Rich for a user-friendly command-line experience.
- **Core Modules**:
  - **Models**: Multi-engine LLM support with a flexible registry system for Ollama, MLX, and future integrations.
  - **Session Management**: Handles state persistence to maintain context across interactions.
  - **Prompts**: Stores and manages prompt templates for various modes (chat, plan, code).
  - **Configuration**: Advanced per-mode model selection with automatic migration from older versions.
  - **Utilities**: Supports ancillary functions and helpers.

## Overview

LADA provides a terminal-based interface for AI-assisted development with three main modes:
- **Chat**: Interactive conversation with the AI
- **Plan**: Generate structured implementation plans
- **Code**: AI-driven code generation and refactoring

## Features

- 🏠 **Fully Local**: Runs entirely on your machine using Ollama or MLX
- 🤖 **Multi-Engine Support**: Use different LLM engines (Ollama, MLX) for different tasks
- 🎯 **Per-Mode Models**: Configure different models for chat, planning, and coding
- 🔧 **Multiple Modes**: Chat, planning, and coding assistance
- 📁 **Project Aware**: Understands your project structure and respects .gitignore
- 💾 **Session Persistence**: Maintains context across sessions
- 🔌 **Extensible**: Plugin architecture for custom functionality
- ⚡ **Flexible Configuration**: Mix and match models based on your needs
- 🔄 **Automatic Migration**: Seamlessly upgrades from older configurations

## Requirements

- Python 3.12+
- Ollama (for Ollama models)
- Apple Silicon Mac (for MLX models)
- 8GB+ RAM recommended

## Installation

### Prerequisites
1. **Python 3.12+**: Ensure you have Python 3.12 or higher installed
2. **Ollama**: Install from [ollama.ai](https://ollama.ai)

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/ccie9658/lada.git
cd lada

# 2. Set Python version (if using pyenv)
pyenv local 3.12.6  # or your preferred 3.12+ version

# 3. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install development dependencies (optional)
pip install -r requirements-dev.txt

# 6. Pull a local model
ollama pull codellama:7b

# 7. Verify installation
python lada.py --version
```

### Quick Start with Helper Script

For convenience, use the activation script:

```bash
source activate.sh  # Sets up environment and installs dependencies if needed
```

## Usage

### Available Commands

```bash
# Show help and available commands
python lada.py --help

# Show version
python lada.py --version

# Show help for specific command
python lada.py chat --help
python lada.py plan --help
python lada.py code --help
```

### Chat Mode
Interactive conversation with the AI assistant:

```bash
python lada.py chat

# With custom model
python lada.py chat --model llama2:13b
```

### Planning Mode
Generate implementation plans for files or modules:

```bash
# Generate plan for a specific file
python lada.py plan path/to/file.py

# Save plan to custom location
python lada.py plan file.py --output my-plan.md

# Use specific model for planning
python lada.py plan main.py --model mlx:GLM-4.5-Air
```

### Code Mode
Generate new code or refactor existing code:

```bash
# Generate new code from description
python lada.py code "FastAPI server with user authentication"

# Generate code for a new file
python lada.py code new_module.py

# Refactor existing code
python lada.py code existing_module.py --refactor

# With specific requirements
python lada.py code calculator.py --requirements "Add scientific functions"

# Save to specific location
python lada.py code "data parser" --output src/parser.py

# Use a specific model
python lada.py code app.py --model mlx:GLM-4.5-Air
```

### Initialize Project
Set up LADA configuration in your project:

```bash
python lada.py init
```

## Configuration

LADA supports flexible configuration with per-mode model selection. Create a `.lada_config.yml` file in your project root:

### Basic Configuration
```yaml
version: 2

model:
  default_model: "codellama:7b"
  temperature: 0.7
  ollama_host: "http://localhost:11434"

session_dir: ".lada/sessions"
auto_save: true
auto_save_interval: 300  # seconds
```

### Advanced Multi-Engine Configuration
```yaml
version: 2

model:
  # Use different models for each mode
  chat_model: "codellama:7b"           # Ollama for chat
  plan_model: "mlx:GLM-4.5-Air"        # MLX for planning
  code_model: "deepseek-coder:6.7b"    # Specialized model for coding
  
  # Engine configurations
  engines:
    ollama:
      host: "http://localhost:11434"
      timeout: 120
    mlx:
      host: "http://localhost:8000"
      timeout: 180
      extra_params:
        gpu_layers: 32
  
  # Global parameters
  temperature: 0.7
  max_tokens: 4096

session_dir: ".lada/sessions"
plan_dir: ".lada/plans"
auto_save: true
```

### Model Selection Examples

You can override the configured model for any command:

```bash
# Use MLX for chat
python lada.py chat --model mlx:GLM-4.5-Air

# Use a specific Ollama model for planning
python lada.py plan file.py --model llama2:13b
```

## MLX Server

LADA includes a FastAPI server wrapper for MLX models that provides Ollama-compatible endpoints. This allows seamless integration of MLX models with Apple Silicon acceleration.

### Starting the MLX Server

```bash
# Activate the virtual environment
source venv/bin/activate

# Start the server with default settings
python scripts/start_mlx_server.py

# Start with custom options
python scripts/start_mlx_server.py --host 0.0.0.0 --port 8080 --log-level DEBUG

# Preload a model on startup
python scripts/start_mlx_server.py --preload-model Qwen2.5-0.5B-Instruct
```

### MLX Server Endpoints

- `GET /health` - Health check and server status
- `GET /v1/models` - List available MLX models
- `POST /v1/completions` - Generate text (Ollama-compatible)
- `POST /models/{model_name}/load` - Load a specific model
- `POST /models/unload` - Unload current model

### Available MLX Models

- `Qwen2.5-0.5B-Instruct` (~400MB)
- `Qwen2.5-1.5B-Instruct` (~1.2GB)
- `Qwen2.5-3B-Instruct` (~2.4GB)
- `Llama-3.2-1B-Instruct` (~800MB)
- `Llama-3.2-3B-Instruct` (~2.4GB)
- `GLM-4.5-Air` (Coming soon)

### MLX Configuration

In your `.lada_config.yml`:

```yaml
model:
  engines:
    mlx:
      host: "http://localhost:8000"
      timeout: 180
```

## Project Status

🚧 **Under Active Development** - This project is in early stages of development.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read the development guidelines in LADA_Guidelines.txt before contributing.
