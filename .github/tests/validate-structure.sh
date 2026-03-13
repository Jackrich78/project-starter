#!/bin/bash
# validate-template.sh - Verify required template files exist
# Part of FEAT-010 CI/CD Integration

set -e

REQUIRED_FILES=(
  "CLAUDE.md"
  "PROJECT.md"
  "README.md"
  "docs/features"
  ".claude/agents/README.md"
)

EXIT_CODE=0

echo "Validating template structure..."

for file in "${REQUIRED_FILES[@]}"; do
  if [ -e "$file" ]; then
    echo "  [OK] $file"
  else
    echo "  [MISSING] $file"
    EXIT_CODE=1
  fi
done

if [ $EXIT_CODE -eq 0 ]; then
  echo "Template structure validation passed."
else
  echo "Template structure validation FAILED."
fi

exit $EXIT_CODE
