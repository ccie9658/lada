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
from lada.commands import chat_mode as run_chat_mode

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
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file for the plan (default: .lada/plans/\u003cfilename\u003e.plan.md)",
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
    try:
        # Simulate plan generation
        plan_content = f"# Implementation Plan\n\n" \
                       f"## Overview\nAnalyze the purpose and goals of {file}.\n" \
                       f"## Steps\n1. Understand the existing code.\n2. Identify key components.\n3. Define goals and requirements.\n"

        output_path = output or Path(f".lada/plans/{file.stem}.plan.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(plan_content)
        console.print(f"🎉 Plan generated and saved to [green]{output_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error generating plan:[/red] {e}")


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
