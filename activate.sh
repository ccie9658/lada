#!/bin/bash
# LADA Development Environment Activation Script

echo "🚀 Activating LADA development environment..."

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import typer" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements-dev.txt
fi

echo "✅ LADA environment activated!"
echo "💡 Run 'python lada.py --help' to get started (once implemented)"
