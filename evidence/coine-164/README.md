# COINE-164 — with/without ablation of instruction lines

Throwaway evidence branch for the Linear ticket COINE-164 (map COINE-138). Never merged.

## Setup

- Agent: Claude Code 2.1.301, `claude -p`, model `claude-opus-5-5`, run on 2026-10-16.
- Isolation: `--setting-sources project,local --strict-mcp-config`, so the real `~/.claude/CLAUDE.md`
  and output style are not loaded. The test instructions are the run directory's `CLAUDE.md`.
- Permissions: `--permission-mode acceptEdits`, Bash limited to `python3`, `ls`, `cat`, `grep`.
- Codex: not run (the sandbox blocks its network access; running it unsandboxed was refused).

## Groups

- **A (Python, `fixture-a/`, `prompt-a.txt`)**: add a `fetch` command calling an external API.
  - `globals/global-con.md`: draft global plus the 10 lines under test (`globals/code-extra.md`).
  - `globals/global-senza.md`: the same draft without them.
  - 5 runs per side. All 10 lines are removed together, so an effect belongs to the group;
    each metric is matched to the line it tests.
- **B (static page, `fixture-b/`)**: the Paddock Design Kit line, plain (`project-plain.md`) vs
  emphasised (`project-caps.md`), each concatenated with `global-senza.md` (`b-plain.md`, `b-caps.md`).
  - `prompt-b-gap.txt`: a banner the kit cannot express (5 runs per side).
  - `prompt-b-cov.txt`: a second card, almost fully covered by the kit (3 runs per side).

## Files

- `run.sh`: one run (copy fixture, add `CLAUDE.md`, run `claude -p`, save JSON result and diff).
- `jobs.txt`: the 25 jobs, executed with `xargs -P 5 -L 1 ./run.sh < jobs.txt`.
- `measure_a.py` → `a.json`; `measure_b.py` → `b.txt`.
- `runs/*.diff`: what each session changed; `runs/*.json`: final message, cost, turns.
