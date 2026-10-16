- Stop and ask before: adding a dependency, a new top-level directory, a new external service, a new architectural layer.
- Config values (URLs, keys, thresholds): from `.env` + app config, never literals — no `.env` possible → ask.
- Public methods: docblock with `@param`, `@return`, `@throws`.
- Code comments, docblocks, docs, commit messages: English, even when the conversation is Italian.
- PHP: `declare(strict_types=1)` in every file. Python: type hints everywhere.

### Tests
- Modifying code with tests: run them before and after. Without tests: write one first.
- New feature: at least one test; names `test_<action>_<expected_result>` or `should<Action><ExpectedResult>`.
- External services: mock them; tests never call real APIs.
- Test runs: the single relevant test, not the full suite.

### Git
- Main branch: never push to `main`/`master`; work on a branch.
- Commits: `feat:`/`fix:`/`refactor:`/`docs:`/`test:`/`chore:` + Linear id, e.g. `feat: add login endpoint (ABC-123)`.
- User-facing change → update `CHANGELOG.md`.

### Tracking
- Tracker: Linear is the only tracker (decided 2026-08-05) — never GitHub Issues, Asana, or local TODO files.
