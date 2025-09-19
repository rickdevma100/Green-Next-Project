#!/bin/bash
set -e

echo "=== ADK Web Startup Debug ==="
echo "Working directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Files in current directory:"
ls -la
echo "Files in green_next_shopping_agent:"
ls -la green_next_shopping_agent/ || true
echo "Python can import agent:"
python -c "import green_next_shopping_agent.agent; print('Agent imported successfully')" || echo "Failed to import agent"
echo "ADK web help:"
adk web --help || echo "ADK web command not available"

echo "Starting ADK web..."
exec adk web --host 0.0.0.0 --port 8080
