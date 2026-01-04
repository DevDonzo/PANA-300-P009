#!/bin/bash

# Auto-commit and push script for Claude Code
# Stages all changes, creates descriptive commit messages, and pushes to remote

cd "$CLAUDE_PROJECT_DIR" || exit 1

# Check if there are any changes to commit
if ! git diff --quiet || ! git diff --cached --quiet; then
  # Stage all changes
  git add .

  # Get detailed info about changes
  changed_files=$(git diff --cached --name-only)
  file_count=$(echo "$changed_files" | grep -c .)

  # Categorize changes by type
  added=$(git diff --cached --name-status | grep "^A" | cut -f2 | wc -l)
  modified=$(git diff --cached --name-status | grep "^M" | cut -f2 | wc -l)
  deleted=$(git diff --cached --name-status | grep "^D" | cut -f2 | wc -l)

  # Get file extensions and types
  extensions=$(git diff --cached --name-only | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -3 | awk '{print $2}' | paste -sd ',' -)

  # Categorize by directory
  directories=$(git diff --cached --name-only | cut -d'/' -f1 | sort | uniq -c | sort -rn | head -2 | awk '{print $2}' | paste -sd ',' -)

  # Build descriptive commit message
  commit_msg=""

  if [ "$file_count" -eq 1 ]; then
    # Single file - be specific
    filename=$(echo "$changed_files" | head -1)
    if [ "$added" -eq 1 ]; then
      commit_msg="Add $(basename "$filename")"
    elif [ "$deleted" -eq 1 ]; then
      commit_msg="Remove $(basename "$filename")"
    else
      commit_msg="Update $(basename "$filename")"
    fi
  else
    # Multiple files - describe the changes
    changes=""
    [ "$added" -gt 0 ] && changes="${changes}+${added} "
    [ "$modified" -gt 0 ] && changes="${changes}~${modified} "
    [ "$deleted" -gt 0 ] && changes="${changes}-${deleted}"

    if [ -n "$directories" ]; then
      commit_msg="Update ${directories}: ${changes}files"
    else
      commit_msg="Update ${file_count} files (${changes})"
    fi
  fi

  # Create commit with description
  git commit -m "$commit_msg"
  commit_status=$?

  if [ $commit_status -eq 0 ]; then
    # Push to remote
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    if git push origin "$current_branch" 2>&1; then
      echo "✓ Committed and pushed: $commit_msg"
    else
      echo "✗ Commit created but push failed: $commit_msg"
      exit 1
    fi
  else
    echo "✗ Commit failed"
    exit 1
  fi
else
  echo "ℹ No changes to commit"
fi

exit 0
