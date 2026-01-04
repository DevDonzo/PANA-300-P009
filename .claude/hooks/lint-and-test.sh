#!/bin/bash

# Linting and Testing Hook
# Runs linting and tests, but doesn't fail the session if they fail (warnings only)

cd "$CLAUDE_PROJECT_DIR" || exit 0

# Check for package.json (Node.js project)
if [ -f "package.json" ]; then
  # Run ESLint if available
  if grep -q '"eslint"' package.json 2>/dev/null; then
    echo "🔍 Running ESLint..."
    npm run lint 2>/dev/null || npx eslint . --max-warnings 5 2>/dev/null || echo "⚠️  ESLint warnings found"
  fi

  # Run tests if available
  if grep -q '"test"' package.json 2>/dev/null; then
    echo "🧪 Running tests..."
    npm test 2>/dev/null || echo "⚠️  Tests failed - check them out"
  fi
fi

# Check for Python project
if [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
  # Run flake8 if available
  if command -v flake8 &> /dev/null; then
    echo "🔍 Running flake8..."
    flake8 . --max-line-length=100 2>/dev/null || echo "⚠️  Flake8 issues found"
  fi

  # Run pytest if available
  if command -v pytest &> /dev/null; then
    echo "🧪 Running pytest..."
    pytest 2>/dev/null || echo "⚠️  Tests failed"
  fi
fi

exit 0
