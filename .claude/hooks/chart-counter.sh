#!/bin/bash
f="$CLAUDE_FILE_PATH"
if [[ "$f" == charts/*.png ]]; then
  n=$(ls charts/*.png 2>/dev/null | wc -l)
  echo "Chart saved: $(basename $f) — $n/38 charts complete"
fi
