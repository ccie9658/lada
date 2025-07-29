"""
Chat command implementation for LADA.

Provides interactive conversation with the AI assistant using local models.
"""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.markup import escape
from difflib import get_close_matches

from lada.models import ModelRegistry, LLMException, LLMConnectionError
from lada.config import ConfigManager

console = Console()


async def chat_mode(model: Optional[str] = None):
    """
    Starts an interactive chat session.

    Args:
        model: The LLM model to use for chat. If None, uses config default.
    """
    # Initialize configuration and registry
    config_manager = ConfigManager()
    config = config_manager.config
    registry = ModelRegistry()
    
    # Use config default if no model specified
    if model is None:
        model = config.model.get_model_for_mode('chat')
        console.print(f"[dim]Using configured chat model: {model}[/dim]")
    
    # Display chat mode panel
    console.print(
        Panel.fit(
            f"🤖 [bold cyan]LADA Chat Mode[/bold cyan]\n"
            f"Model: [green]{model}[/green]\n"
            "Type 'exit' or 'quit' to end the session.",
            border_style="cyan",
        )
    )

    try:
        llm = registry.get_llm(model)
        engine, model_name = registry._parse_model_name(model)

        # Check if the LLM service is available
        if not await llm.is_available():
            if engine == "ollama":
                console.print("❌ [red]Error:[/red] Ollama is not running. Please start it with 'ollama serve'")
            elif engine == "mlx":
                console.print("❌ [red]Error:[/red] MLX server is not running. Please start it with 'python scripts/start_mlx_server.py'")
            else:
                console.print(f"❌ [red]Error:[/red] {engine.upper()} service is not running. Please ensure the service is active.")
            return
        
        # Check if the requested model exists
        available_models = await llm.list_models()
        # For multi-engine support, we need to check the actual model name, not the full engine:model string
        if model_name not in available_models:
            console.print(f"❌ [red]Error:[/red] Model '{model_name}' not found in {engine.upper()}.")
            
            # Suggest similar models
            if available_models:
                similar = get_close_matches(model, available_models, n=3, cutoff=0.6)
                if similar:
                    console.print("\n[yellow]Did you mean one of these?[/yellow]")
                    for m in similar:
                        console.print(f"  • {m}")
                
                console.print("\n[yellow]Available models:[/yellow]")
                for m in available_models:
                    console.print(f"  • {m}")
            else:
                console.print("[yellow]No models found. Please check the model name and try again.[/yellow]")
            return
            
    except LLMConnectionError as e:
        console.print(f"❌ [red]Connection Error:[/red] {e}")
        return
    except LLMException as e:
        console.print(f"❌ [red]Error:[/red] {e}")
        return
    except Exception as e:
        console.print(f"❌ [red]Unexpected Error:[/red] {e}")
        return

    while True:
        try:
            prompt = console.input("[bold green]You:[/bold green] ")

            if prompt.lower().strip() in {"exit", "quit"}:
                console.print("👋 [bold]Goodbye![/bold]")
                break

            # Show thinking indicator
            with console.status("[dim]Thinking...[/dim]", spinner="dots"):
                response = await llm.generate(prompt)
            
            # Escape response for safe display
            escaped_response = escape(response.content.strip())

            # Display response
            console.print("\n[bold blue]Assistant:[/bold blue]")
            console.print(Panel(
                escaped_response, 
                border_style="blue",
                padding=(1, 2)
            ))
            console.print()  # Add spacing

        except LLMException as e:
            console.print(f"❌ [red]Error:[/red] {e}")
        except KeyboardInterrupt:
            console.print("\n👋 [bold]Goodbye![/bold]")
            break

