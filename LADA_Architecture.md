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
                    │ Model Registry │
                    └───────┬───────┘
                            ▼
                 ┌──────────┴──────────┐
                 ▼                     ▼
         ┌──────────────┐     ┌──────────────┐
         │ Ollama LLM   │     │   MLX LLM    │
         └──────┬───────┘     └──────┬───────┘
                 └──────────┬─────────┘
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
- **Command Handlers**: Individual async functions for each mode
- **Modular Commands**: Each command imports from dedicated module

**Commands**:
- `chat`: Interactive AI conversation mode
  - Options: `--model` to specify LLM model
  - Implemented: Multi-engine support, error handling, model selection
  - Future: Streaming responses, conversation history
- `plan`: Generate implementation plans
  - Arguments: Target file path
  - Options: `--model` for model override, `--output` for custom location
  - Implemented: Flexible prompts, markdown preview, file saving
  - Future: Multi-file analysis, project-wide planning
- `code`: Code generation and refactoring
  - Arguments: Target file path or description
  - Options: `--model`, `--refactor`, `--requirements`, `--output`
  - Implemented: Full code generation, refactoring, markdown extraction
  - Future: Diff preview, automatic testing
- `init`: Project initialization
  - Future: Interactive setup wizard

### 2. LLM Interface (`lada/models/`)

**Purpose**: Multi-engine LLM support with flexible model selection.

**Architecture**:
```python
# base.py - Abstract base class
class BaseLLM:
    async def generate(prompt: str, **kwargs) -> LLMResponse
    async def stream(prompt: str, **kwargs) -> AsyncIterator[str]
    async def list_models() -> List[str]
    async def is_available() -> bool

# registry.py - Model Registry
class ModelRegistry:
    def get_llm(model_name: str) -> BaseLLM
    def _parse_model_name(model_name: str) -> Tuple[engine, model]

# ollama.py - Ollama implementation
class OllamaLLM(BaseLLM):
    - HTTP client for Ollama API
    - Model management
    - Error handling and retries

# mlx.py - MLX implementation
class MLXLLM(BaseLLM):
    - HTTP client for MLX FastAPI server
    - GLM and other MLX model support
    - Memory-efficient processing

# Future: openai.py, anthropic.py, etc.
```

**Key Features**:
- **Model Registry**: Factory pattern for LLM instantiation
- **Engine Detection**: Smart parsing of model names (e.g., "mlx:GLM-4.5-Air")
- **Per-Mode Models**: Different models for chat, planning, and coding
- **Flexible Configuration**: Mix and match engines based on task requirements
- **Streaming Support**: Better UX with real-time responses
- **Retry Logic**: Automatic retry with exponential backoff
- **Error Handling**: Engine-specific error messages and recovery

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
- `plan.txt`: Adaptive planning template that adjusts to input type
- `code.txt`: Flexible code generation template with multiple modes

**Implemented Features**:
- **Adaptive Templates**: Prompts adjust based on context and input type
- **Context Injection**: Templates include project context and file content
- **Mode-Specific Behavior**: Different guidance for new code vs refactoring

**Planned Features**:
- Template versioning
- Custom prompt override support
- Template hot-reloading

### 5. Configuration System (`lada/config.py`)

**Purpose**: Advanced configuration with per-mode model selection and multi-engine support.

**Key Features**:
- **Per-Mode Models**: Configure different models for chat, plan, and code modes
- **Multi-Engine Support**: Configure multiple LLM engines (Ollama, MLX, etc.)
- **Automatic Migration**: Seamlessly upgrades from v1 to v2 configuration format
- **Type-Safe Validation**: Pydantic models ensure configuration correctness
- **Backward Compatibility**: Old configurations continue to work

**Configuration Schema (v2)**:
```yaml
version: 2  # Configuration version

model:
  # Per-mode model selection
  chat_model: str?      # e.g., "codellama:7b" or "mlx:GLM-4.5-Air"
  plan_model: str?      # Different model for planning
  code_model: str?      # Specialized model for coding
  
  # Legacy/fallback
  default_model: str    # Used when mode-specific model not set
  
  # Engine configurations
  engines:
    ollama:
      host: str         # Default: "http://localhost:11434"
      timeout: int      # Default: 120
      max_retries: int  # Default: 3
    mlx:
      host: str         # Default: "http://localhost:8000"
      timeout: int      # Default: 120
      extra_params: dict  # Engine-specific parameters
  
  # Global parameters
  temperature: float    # Default: 0.7
  max_tokens: int?      # Optional token limit

# Session and storage
session_dir: Path       # Default: ".lada/sessions"
plan_dir: Path          # Default: ".lada/plans"
backup_dir: Path        # Default: ".lada/backups"
auto_save: bool         # Default: true
auto_save_interval: int # Default: 300 seconds
```

**Configuration Classes**:
- `EngineConfig`: Engine-specific settings
- `ModelConfig`: Model selection and parameters
- `LADAConfig`: Main configuration container
- `ConfigManager`: Handles loading, saving, and migration

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

## Command Implementation Pattern

All commands follow a consistent async pattern:

1. **Module Structure** (`lada/commands/{command}.py`):
   ```python
   async def {command}_mode(args...):
       # Load configuration
       # Get model from registry
       # Check availability
       # Load prompt template
       # Execute LLM operation
       # Display/save results
   ```

2. **CLI Integration** (`lada/cli.py`):
   ```python
   @app.command()
   def {command}(args...):
       asyncio.run(run_{command}_mode(args...))
   ```

3. **Error Handling**:
   - LLMConnectionError for service issues
   - LLMException for general errors
   - Graceful degradation with helpful messages

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
