"""
Main CLI application for LADA.

This module provides the command-line interface for LADA,
including the chat, plan, and code modes.
"""

from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from lada import __version__

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
        "codellama:7b",
        "--model",
        "-m",
        help="Model to use for chat",
    ),
):
    """
    Start an interactive chat session with the AI assistant.
    """
    console.print(
        Panel.fit(
            "🤖 [bold cyan]LADA Chat Mode[/bold cyan]\n"
            "Type 'exit' or 'quit' to end the session.",
            border_style="cyan",
        )
    )
    console.print(f"Using model: [green]{model}[/green]\n")
    
    # TODO: Implement chat functionality
    console.print("[yellow]Chat mode not yet implemented.[/yellow]")


@app.command()
def plan(
    file: Path = typer.Argument(
        ...,
        help="File to generate implementation plan for",
        exists=True,
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
    """
    console.print(
        Panel.fit(
            f"📋 [bold cyan]Planning Mode[/bold cyan]\n"
            f"Analyzing: [green]{file}[/green]",
            border_style="cyan",
        )
    )
    
    # TODO: Implement planning functionality
    console.print("[yellow]Planning mode not yet implemented.[/yellow]")


@app.command()
def code(
    file: Path = typer.Argument(
        ...,
        help="File to generate or refactor code for",
    ),
    refactor: bool = typer.Option(
        False,
        "--refactor",
        "-r",
        help="Refactor existing code instead of generating new code",
    ),
):
    """
    Generate or refactor code with AI assistance.
    """
    mode = "Refactoring" if refactor else "Code Generation"
    console.print(
        Panel.fit(
            f"💻 [bold cyan]{mode} Mode[/bold cyan]\n"
            f"Target: [green]{file}[/green]",
            border_style="cyan",
        )
    )
    
    # TODO: Implement code generation functionality
    console.print(f"[yellow]{mode} mode not yet implemented.[/yellow]")


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
