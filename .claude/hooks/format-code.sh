#!/bin/bash

# Code Formatting Hook
# Auto-formats code using available formatters

cd "$CLAUDE_PROJECT_DIR" || exit 0

# Check for package.json (Node.js project)
if [ -f "package.json" ]; then
  # Format with Prettier if available
  if grep -q '"prettier"' package.json 2>/dev/null; then
    echo "✨ Formatting with Prettier..."
    npx prettier --write . --ignore-unknown 2>/dev/null
  fi

  # Format with ESLint if available
  if grep -q '"eslint"' package.json 2>/dev/null; then
    echo "✨ Fixing with ESLint..."
    npx eslint . --fix 2>/dev/null || true
  fi
fi

# Check for Python project
if [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
  # Format with Black if available
  if command -v black &> /dev/null; then
    echo "✨ Formatting with Black..."
    black . 2>/dev/null || true
  fi

  # Sort imports with isort if available
  if command -v isort &> /dev/null; then
    echo "✨ Sorting imports..."
    isort . 2>/dev/null || true
  fi
fi

exit 0
