"""Tests for the CLI module."""

import pytest
from typer.testing import CliRunner
from lada.cli import app
from lada import __version__


runner = CliRunner()


def test_version():
    """Test version display."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"LADA version {__version__}" in result.stdout


def test_help():
    """Test help display."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Local AI-Driven Development Assistant" in result.stdout


def test_chat_help():
    """Test chat command help."""
    result = runner.invoke(app, ["chat", "--help"])
    assert result.exit_code == 0
    assert "interactive chat session" in result.stdout


def test_plan_help():
    """Test plan command help."""
    result = runner.invoke(app, ["plan", "--help"])
    assert result.exit_code == 0
    assert "implementation plan" in result.stdout


def test_code_help():
    """Test code command help."""
    result = runner.invoke(app, ["code", "--help"])
    assert result.exit_code == 0
    assert "Generate or refactor code" in result.stdout
