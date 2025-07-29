"""
Main CLI application for LADA.

This module provides the command-line interface for LADA,
including the chat, plan, and code modes.
"""

from typing import Optional
import asyncio
import typer
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from lada import __version__
from lada.commands import chat_mode as run_chat_mode, plan_mode as run_plan_mode, code_mode as run_code_mode

# Initialize Typer app and Rich console
app = typer.Typer(
    name="lada",
    help="Local AI-Driven Development Assistant",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()


def version_callback(value: bool):
    """Display version information."""
    if value:
        console.print(f"LADA version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
):
    """
    LADA - Local AI-Driven Development Assistant.
    
    A local AI assistant for structured, iterative software development.
    """
    pass


@app.command()
def chat(
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="Model to use for chat (e.g., 'codellama:7b' or 'mlx:GLM-4.5-Air'). If not specified, uses configured default.",
    ),
):
    """
    Start an interactive chat session with the AI assistant.
    
    Examples:
        lada chat                    # Use configured default model
        lada chat -m codellama:7b    # Use specific Ollama model
        lada chat -m mlx:GLM-4.5-Air # Use MLX model
    """
    try:
        asyncio.run(run_chat_mode(model))
    except KeyboardInterrupt:
        console.print("\n👋 Chat interrupted.")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@app.command()
def plan(
    file: Path = typer.Argument(
        ...,
        help="File to generate implementation plan for",
        exists=True,
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="Model to use for planning (e.g., 'llama2:13b' or 'mlx:GLM-4.5-Air'). If not specified, uses configured default.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file for the plan (default: .lada/plans/<filename>.plan.md)",
    ),
):
    """
    Generate an implementation plan for a file or module.
    
    Examples:
        lada plan main.py                        # Use configured default model
        lada plan main.py -m mlx:GLM-4.5-Air     # Use MLX model for planning
        lada plan main.py -o custom-plan.md      # Save to custom location
    """
    try:
        asyncio.run(run_plan_mode(file, model, output))
    except KeyboardInterrupt:
        console.print("\n📋 Planning interrupted.")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@app.command()
def code(
    target: str = typer.Argument(help="File path or description of what to generate"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Model to use (overrides config)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    requirements: Optional[str] = typer.Option(None, "--requirements", "-r", help="Additional requirements or context"),
    refactor: bool = typer.Option(False, "--refactor", help="Refactor existing code (will read target file)")
):
    """
    Generate or refactor code with AI assistance.
    
    Examples:
        lada code hello.py                       # Generate new code file
        lada code main.py --refactor            # Refactor existing code
        lada code "FastAPI server" -o app.py    # Generate from description
    """
    try:
        asyncio.run(run_code_mode(target, model, output, requirements, refactor))
    except KeyboardInterrupt:
        console.print("\n💻 Code generation interrupted.")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@app.command()
def init():
    """
    Initialize LADA in the current directory.
    """
    console.print("🚀 Initializing LADA in current directory...")
    
    # TODO: Implement initialization functionality
    console.print("[yellow]Init command not yet implemented.[/yellow]")


if __name__ == "__main__":
    app()
