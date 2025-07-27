"""
Chat command implementation for LADA.

Provides interactive conversation with the AI assistant using local models.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markup import escape

from lada.models import OllamaLLM, LLMException
from difflib import get_close_matches

console = Console()


async def chat_mode(model: str):
    """
    Starts an interactive chat session.

    Args:
        model: The LLM model to use for chat
    """
    console.print(
        Panel.fit(
            f"🤖 [bold cyan]LADA Chat Mode[/bold cyan]\n"
            f"Model: [green]{model}[/green]\n"
            "Type 'exit' or 'quit' to end the session.",
            border_style="cyan",
        )
    )

    # Check if Ollama is available
    llm = OllamaLLM(model=model)
    
    try:
        if not await llm.is_available():
            console.print("❌ [red]Error:[/red] Ollama is not running. Please start it with 'ollama serve'")
            return
            
        # Check if the requested model exists
        available_models = await llm.list_models()
        if model not in available_models:
            console.print(f"❌ [red]Error:[/red] Model '{model}' not found.")
            
            # Check for similar model names (typos)
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
                console.print("[yellow]No models found. Pull a model with:[/yellow]")
                console.print(f"  ollama pull {model}")
            return
            
    except Exception as e:
        console.print(f"❌ [red]Error connecting to Ollama:[/red] {e}")
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

