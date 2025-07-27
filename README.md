# LADA - Local AI-Driven Development Assistant

A local AI assistant workflow that mimics agent-style development setups using Ollama and open-source LLMs, allowing for structured, iterative, agent-guided software development.

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

```bash
# Clone the repository
git clone https://github.com/yourusername/lada.git
cd lada

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull a local model
ollama pull codellama:7b
```

## Usage

```bash
# Start chat mode
python lada.py chat

# Generate an implementation plan
python lada.py plan module.py

# Generate or refactor code
python lada.py code module.py
```

## Project Status

🚧 **Under Active Development** - This project is in early stages of development.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read the development guidelines in LADA_Guidelines.txt before contributing.
