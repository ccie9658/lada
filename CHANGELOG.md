# Changelog

All notable changes to LADA (Local AI-Driven Development Assistant) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with modular architecture
- CLI interface using Typer and Rich for beautiful terminal output
- Four main commands: `chat`, `plan`, `code`, and `init`
- Configuration management system using Pydantic
- Prompt templates for different modes (chat, planning, code generation)
- Basic test suite with pytest
- Project documentation (README.md, LADA_Guidelines.txt)
- Development environment setup with virtual environment support
- Helper activation script for quick development setup
- GitHub repository initialization
- **Multi-Engine LLM Support**: Flexible model registry supporting Ollama and MLX
- **Per-Mode Model Configuration**: Use different models for chat, planning, and coding
- **Model Registry Pattern**: Factory-based LLM instantiation with smart model name parsing
- **Advanced Configuration System**: Version 2 configuration with automatic migration
- **MLX Integration**: Support for MLX models via FastAPI server
- **Enhanced Error Handling**: Engine-specific exceptions and error messages

### Changed
- **Configuration System**: Upgraded from simple model config to advanced multi-engine configuration
- **Model Interface**: Refactored to support multiple LLM engines through registry pattern
- **Architecture**: Updated system design to support pluggable LLM implementations

### Technical Details
- Set up Python 3.12.6 with pyenv for version management
- Established modular package structure (models, session, utils, prompts)
- Implemented configuration system with YAML support
- Added comprehensive .gitignore for Python projects
- Created prompt template system for different AI modes
- Set up testing infrastructure with pytest
- **Model Registry Implementation**: Created `ModelRegistry` class for dynamic LLM selection
- **Configuration Migration**: Automatic upgrade from v1 to v2 configuration format
- **Engine Abstraction**: Implemented `BaseLLM` interface with `OllamaLLM` and `MLXLLM`
- **Smart Model Parsing**: Support for "engine:model" naming convention

## [0.1.0] - TBD (First Alpha Release)

_This section will be updated when the first alpha release is made._

### Planned Features
- Working Ollama integration for local LLM inference
- Basic chat mode functionality
- Session persistence and management
- File operations with safety measures
- Initial planning mode implementation

---

## Version History

- **2024-01-27**: Project inception and initial setup
