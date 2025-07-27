# Local AI-Driven Development Assistant (LADA)

## Objective

Build a local AI assistant workflow that mimics Warp's agent-style development setup using Ollama and open-source LLMs, allowing for structured, iterative, agent-guided software development.

---

## Architecture Overview

- **Frontend CLI Interface**: A terminal-style tool with prompts, colors, and mode switching (`chat`, `plan`, `code`, etc.).
- **Core Logic (Python)**:
  - Agent controller to manage phases: planning, codegen, testing, review.
  - Interface with local models using Ollama.
  - Ability to call external APIs (e.g., GPT-4) if authorized.
- **File I/O and Project Awareness**:
  - Maintain session context across directories/files.
  - Respect `.gitignore` and modular structure.
- **State Persistence**:
  - Store session metadata, plans, and iterations.
- **Optional Cloud Model Orchestration Layer**:
  - Offload strategy/QA to a cloud model when local agents stall.

---

## Phase 1: Bootstrap the Core System

### 1. Environment Setup
- Python 3.10+
- Install Ollama
- Install required packages:
  ```bash
  pip install typer rich openai pyyaml
  ```

### 2. CLI Tool Skeleton (`lada.py`)
- Use `typer` for CLI structure.
- Modes:
  - `plan`: Generates structured implementation plans.
  - `code`: Implements/refactors files.
  - `chat`: Freeform interaction.
- Pretty printing via `rich`.

### 3. Model Interface Module (`models.py`)
- Load and call:
  - Local LLMs via `subprocess` or HTTP interface from Ollama.
  - Remote GPT-4/Claude if API keys present.
- Prompt templates:
  - Agent prompt
  - Planning prompt
  - Review/refactor prompt

### 4. Session Management (`session.py`)
- Save/reload:
  - Project state
  - Plans
  - Output history

---

## Phase 2: Define Agent Workflow

### 1. Planning Phase
- Inject architectural style, dev guidelines.
- Model returns step-by-step plan.

### 2. Review Phase
- Each plan step confirmed before execution.

### 3. Code Generation
- Controlled scope
- Unit test stubs created
- Lint + syntax checking

### 4. Test Execution (Optional)
- Python files can be run/tested locally.

---

## Phase 3: Extend with Plugins

- `plugins/` folder for things like:
  - Auto unit test runner
  - Git commit hooks
  - Cloud sync

---

## Example Use

```bash
# Start planning for a module
python lada.py plan my_module.py

# Review and implement
python lada.py code my_module.py

# Freeform LLM chat
python lada.py chat
```

---

## Notes

- Models assumed to be downloaded with `ollama pull codellama:7b`.
- Optional: Add `~/.lada_config.yml` to set model prefs, API keys, rules, tone, etc.
