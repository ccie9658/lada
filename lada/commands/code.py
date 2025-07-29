"""Code command for LADA."""
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
import re

from lada.config import ConfigManager
from lada.models import ModelRegistry, LLMException, LLMConnectionError

console = Console()


def load_code_prompt_template() -> str:
    """Load the code prompt template."""
    prompt_file = Path(__file__).parent.parent / "prompts" / "code.txt"
    if not prompt_file.exists():
        raise LLMException(f"Code prompt template not found at {prompt_file}")
    return prompt_file.read_text()


async def code_mode(
    target: str,
    model: Optional[str] = None,
    output: Optional[str] = None,
    requirements: Optional[str] = None,
    refactor: bool = False
):
    """Generate or refactor code based on requirements."""
    try:
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.config
        
        # Determine which model to use
        model_name = model or config.model.get_model_for_mode('code')
        console.print(f"[cyan]Using model: {model_name}[/cyan]")
        
        # Get the LLM instance from registry
        registry = ModelRegistry()
        llm = registry.get_llm(model_name)
        engine, _ = registry._parse_model_name(model_name)
        
        # Check if the LLM service is available
        if not await llm.is_available():
            if engine == "ollama":
                console.print("❌ [red]Error:[/red] Ollama is not running. Please start it with 'ollama serve'")
            elif engine == "mlx":
                console.print("❌ [red]Error:[/red] MLX server is not running. Please start it with 'python scripts/start_mlx_server.py'")
            else:
                console.print(f"❌ [red]Error:[/red] {engine.upper()} service is not running. Please ensure the service is active.")
            return
        
        # Load the code prompt template
        prompt_template = load_code_prompt_template()
        
        # Prepare the target and content
        target_path = Path(target)
        current_content = ""
        filename = target
        
        if refactor and target_path.exists():
            # Read existing file for refactoring
            current_content = target_path.read_text()
            filename = str(target_path)
            task_type = "refactor the existing code"
        elif target_path.exists() and target_path.is_file():
            # File exists but not refactoring - read it for context
            current_content = target_path.read_text()
            filename = str(target_path)
            task_type = "generate new code based on the existing file"
        else:
            # New code generation
            task_type = "generate new code"
            
        # Get project context (current directory info)
        project_context = f"Working directory: {Path.cwd()}"
        if (Path.cwd() / ".git").exists():
            project_context += "\nThis is a Git repository."
        
        # Add requirements if provided
        if not requirements:
            requirements = f"Generate code for: {target}"
        
        # Fill in the prompt template
        prompt = prompt_template.format(
            task_type=task_type,
            filename=filename,
            current_content=current_content,
            requirements=requirements,
            project_context=project_context
        )
        
        # Generate code
        console.print("[yellow]Generating code...[/yellow]")
        response = await llm.generate(prompt)
        
        # Display the generated code
        console.print("\n[green]Generated Code:[/green]")
        console.print(Markdown(response.content))
        
        # Save to file if output path is specified
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Extract code from markdown if present
            code_content = response.content
            if "```" in response.content:
                # Extract code from markdown code blocks
                import re
                code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', response.content, re.DOTALL)
                if code_blocks:
                    code_content = "\n\n".join(code_blocks)
            
            output_path.write_text(code_content)
            console.print(f"\n[green]✓ Code saved to: {output_path}[/green]")
            
    except LLMConnectionError as e:
        console.print(f"❌ [red]Connection Error:[/red] {e}")
    except LLMException as e:
        console.print(f"❌ [red]Error:[/red] {e}")
    except Exception as e:
        console.print(f"❌ [red]Unexpected Error:[/red] {e}")
