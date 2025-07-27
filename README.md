# LADA - Local AI-Driven Development Assistant

A local AI assistant workflow that mimics agent-style development setups using Ollama and open-source LLMs, allowing for structured, iterative, agent-guided software development.

## Architecture Summary

LADA is designed with a modular architecture to ensure scalability and maintainability:

- **CLI Interface** (`lada.py`): Main entry point, built using Typer and Rich for a user-friendly command-line experience.
- **Core Modules**:
  - **Models**: Interfaces with local LLMs (using Ollama) and optional cloud models for AI processing.
  - **Session Management**: Handles state persistence to maintain context across interactions.
  - **Prompts**: Stores and manages prompt templates for various modes (chat, plan, code).
  - **Utilities**: Suppports ancillary functions and helpers.

## Overview

LADA provides a terminal-based interface for AI-assisted development with three main modes:
- **Chat**: Interactive conversation with the AI
- **Plan**: Generate structured implementation plans
- **Code**: AI-driven code generation and refactoring

## Features

- 🏠 **Fully Local**: Runs entirely on your machine using Ollama
- 🔧 **Multiple Modes**: Chat, planning, and coding assistance
- 📁 **Project Aware**: Understands your project structure and respects .gitignore
- 💾 **Session Persistence**: Maintains context across sessions
- 🔌 **Extensible**: Plugin architecture for custom functionality
- ☁️ **Optional Cloud**: Can fall back to cloud models when needed

## Requirements

- Python 3.12+
- Ollama
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
```

### Code Mode
Generate new code or refactor existing code:

```bash
# Generate new code
python lada.py code new_module.py

# Refactor existing code
python lada.py code existing_module.py --refactor
```

### Initialize Project
Set up LADA configuration in your project:

```bash
python lada.py init
```

## Configuration

Create a `.lada_config.yml` file in your project root to customize settings:

```yaml
model:
  default_model: "codellama:7b"
  temperature: 0.7
  ollama_host: "http://localhost:11434"

session:
  auto_save: true
  auto_save_interval: 300  # seconds
```

## Project Status

🚧 **Under Active Development** - This project is in early stages of development.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read the development guidelines in LADA_Guidelines.txt before contributing.
