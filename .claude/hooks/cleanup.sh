#!/bin/bash

# Cleanup Hook
# Removes build artifacts, caches, and temporary files

cd "$CLAUDE_PROJECT_DIR" || exit 0

echo "🧹 Cleaning up..."

# Node.js cleanup
rm -rf node_modules/.cache 2>/dev/null
rm -rf dist build .next .nuxt coverage 2>/dev/null
find . -name "*.tsbuildinfo" -delete 2>/dev/null

# Python cleanup
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# General cleanup
rm -rf .DS_Store 2>/dev/null
find . -type f -name ".DS_Store" -delete 2>/dev/null

echo "✓ Cleanup complete"
exit 0
