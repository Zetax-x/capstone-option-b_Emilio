#!/bin/bash
echo "$(date '+%Y-%m-%d %H:%M:%S') | exit:$CLAUDE_TOOL_RESULT_EXIT_CODE | $(echo $CLAUDE_TOOL_INPUT | head -c 120)" >> session-log.md
