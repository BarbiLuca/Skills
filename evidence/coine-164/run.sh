#!/bin/bash
# Usage: run.sh <fixture> <claude_md> <prompt_file> <run_id>
set -euo pipefail
S=$(cd "$(dirname "$0")" && pwd)
FIX=$1; MD=$2; PROMPT=$3; ID=$4
RUN=$S/runs/$ID
rm -rf "$RUN"; mkdir -p "$S/runs"; cp -R "$S/$FIX" "$RUN"
cp "$MD" "$RUN/CLAUDE.md"
(cd "$RUN" && git add CLAUDE.md && git -c user.name=fixture -c user.email=f@x commit -qm "add instructions")
BASE=$(cd "$RUN" && git rev-parse HEAD)
cd "$RUN"
claude -p "$(cat "$PROMPT")" \
  --setting-sources project,local --strict-mcp-config \
  --permission-mode acceptEdits \
  --allowedTools "Bash(python3:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(grep:*)" \
  --max-budget-usd 3 --output-format json > "$S/runs/$ID.json" 2> "$S/runs/$ID.err" || true
git add -A >/dev/null 2>&1; git diff --cached "$BASE" > "$S/runs/$ID.diff" || true
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(sys.argv[2], 'cost=%.3f'%d.get('total_cost_usd',0), 'turns=',d.get('num_turns'), 'err=',d.get('is_error'))" "$S/runs/$ID.json" "$ID" || echo "$ID: no json"
