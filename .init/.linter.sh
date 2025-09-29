#!/bin/bash
cd /home/kavia/workspace/code-generation/unified-connector-platform-167385-167394/backend_service
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

