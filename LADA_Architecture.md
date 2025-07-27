# LADA Technical Architecture Document

## Overview

LADA (Local AI-Driven Development Assistant) is a command-line tool that provides AI-powered development assistance using local language models. The system is designed with modularity, extensibility, and user privacy in mind.

## Design Principles

1. **Modularity**: Each component has a single, well-defined responsibility
2. **Local-First**: Prioritizes local LLM usage for privacy and offline capability
3. **Extensibility**: Plugin architecture allows for custom functionality
4. **Type Safety**: Uses Python type hints and Pydantic for runtime validation
5. **User Experience**: Rich CLI interface with intuitive commands

## System Architecture

```
┌─────────────────┐     ┌──────────────────┐
│   User Input    │────▶│    CLI (Typer)   │
└─────────────────┘     └────────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
            ┌──────────────┐         ┌────────────────┐
            │ Config Mgmt  │         │ Session Mgmt   │
            │  (Pydantic)  │         │ (JSON/Pickle)  │
            └──────┬───────┘         └────────┬───────┘
                   │                          │
                   └────────┬─────────────────┘
                            ▼
                    ┌───────────────┐
                    │  LLM Interface │
                    │   (Ollama)    │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │ Prompt Engine │
                    └───────────────┘
```

## Core Components

### 1. CLI Interface (`lada/cli.py`)

**Purpose**: Provides the command-line interface for user interactions.

**Key Components**:
- **Typer Application**: Main app instance with commands
- **Rich Console**: For formatted output and user feedback
- **Command Handlers**: Individual functions for each mode

**Commands**:
- `chat`: Interactive AI conversation mode
  - Options: `--model` to specify LLM model
  - Future: Streaming responses, conversation history
- `plan`: Generate implementation plans
  - Arguments: Target file path
  - Options: `--output` for custom output location
  - Future: Multi-file analysis, project-wide planning
- `code`: Code generation and refactoring
  - Arguments: Target file path
  - Options: `--refactor` flag for refactoring mode
  - Future: Diff preview, automatic testing
- `init`: Project initialization
  - Future: Interactive setup wizard

### 2. LLM Interface (`lada/models/`)

**Purpose**: Abstract interface for LLM interactions.

**Planned Structure**:
```python
# base.py - Abstract base class
class BaseLLM:
    async def generate(prompt: str) -> str
    async def stream(prompt: str) -> AsyncIterator[str]

# ollama.py - Ollama implementation
class OllamaLLM(BaseLLM):
    - HTTP client for Ollama API
    - Model management
    - Error handling and retries

# openai.py - Optional OpenAI implementation
class OpenAILLM(BaseLLM):
    - API key management
    - Cost tracking
```

**Features**:
- Model abstraction for easy switching
- Streaming support for better UX
- Token counting and context management
- Retry logic with exponential backoff

### 3. Session Management (`lada/session/`)

**Purpose**: Maintain state across LADA invocations.

**Planned Components**:
- **Session Store**: JSON-based storage in `.lada/sessions/`
- **Context Manager**: Maintains conversation history
- **State Recovery**: Handle interrupted sessions

**Data Structure**:
```json
{
  "session_id": "uuid",
  "created_at": "timestamp",
  "mode": "chat|plan|code",
  "messages": [...],
  "context": {
    "project_path": "...",
    "files_analyzed": [...],
    "model_used": "..."
  }
}
```

### 4. Prompt Management (`lada/prompts/`)

**Purpose**: Centralized prompt template management.

**Current Templates**:
- `chat.txt`: General conversation template
- `plan.txt`: Code analysis and planning template
- `code.txt`: Code generation template

**Planned Features**:
- Template versioning
- Dynamic prompt construction
- Context injection system
- Custom prompt override support

### 5. Configuration System (`lada/config.py`)

**Purpose**: Type-safe configuration management.

**Current Implementation**:
- Pydantic models for validation
- YAML file support
- Hierarchical configuration

**Configuration Schema**:
```yaml
model:
  default_model: str
  ollama_host: str
  timeout: int
  temperature: float
  max_tokens: int?

session:
  auto_save: bool
  auto_save_interval: int
  max_history: int

project:
  ignore_patterns: list[str]
  max_file_size: int
```

### 6. File Operations (`lada/utils/file_handler.py`)

**Purpose**: Safe file operations with project awareness.

**Planned Features**:
- `.gitignore` parsing and respect
- Automatic backup before modifications
- Binary file detection
- Encoding detection
- Atomic writes

## Configuration Management
- **File**: `lada/config.py`
- **Description**: Uses Pydantic for managing configurations, allowing customization through `.lada_config.yml`.
- **Key Features**:
  - Model settings
  - Session persistence settings

## Setup and Deployment
- **Virtual Environment**: Python `venv` is used to manage dependencies.
- **Dependencies**: Listed in `requirements.txt` and `requirements-dev.txt`.

## Testing
- **Framework**: `pytest` is used for writing and running tests.
- **Location**: Tests reside in the `tests/` directory.
- **Coverage**: Initial tests for CLI commands.

## Development Workflow
1. **Setup**: Clone repository, set up virtual environment, and install dependencies.
2. **Code**: Follow modular structure, adding functionality in respective modules.
3. **Test**: Write tests and validate functionalities using `pytest`.
4. **Deploy**: Ensure the environment is configured with all dependencies before running.

## Future Plans
- **Ollama Integration**: Enable local LLM interactions.
- **Enhanced Features**: Implement AI-driven code assistance in all defined modes.
- **Session Management**: Robust session persistence for user convenience.

## Contribution
Contributions follow the guidelines defined in the `LADA_Guidelines.txt` file. Proper modular integration and adherence to coding standards are essential for any contribution.
