#!/bin/bash

# Auto-commit and push script for Claude Code
# Stages all changes, creates a concise commit message, and pushes to remote

cd "$CLAUDE_PROJECT_DIR" || exit 1

# Check if there are any changes to commit
if ! git diff --quiet || ! git diff --cached --quiet; then
  # Stage all changes
  git add .

  # Get a summary of changed files
  changed_files=$(git diff --cached --name-only)
  file_count=$(echo "$changed_files" | grep -c .)

  # Build a concise commit message based on changes
  if [ "$file_count" -eq 1 ]; then
    # Single file changed
    filename=$(echo "$changed_files" | head -1)
    commit_msg="Update $(basename "$filename")"
  elif [ "$file_count" -le 3 ]; then
    # A few files changed - list them
    files=$(echo "$changed_files" | head -3 | sed 's/^/  - /' | tr '\n' ' ')
    commit_msg="Update multiple files:$files"
  else
    # Many files changed
    commit_msg="Update $file_count files"
  fi

  # Create commit
  git commit -m "$commit_msg"

  # Push to remote
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  git push origin "$current_branch" 2>/dev/null

  echo "✓ Committed and pushed: $commit_msg"
else
  echo "No changes to commit"
fi

exit 0
