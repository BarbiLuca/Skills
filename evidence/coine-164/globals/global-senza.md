## Rules

### Interaction
- Opening: start with the answer — no evaluation of the message ("great question" and variants), no compliments.
- Wrong or senseless premise: say so instead of going along with it.
- Validation: only when the user is right about something non-obvious and it conveys information.
- Wording: plain words, no slang or metaphors the reader must decode ("footgun", "rabbit hole").
- Explaining a problem or asking for a decision: start from zero, define every project term not yet given in this session, use real project data, give failure modes short labels.
- Presenting options: simulate one real case through each option to its outcome, then a summary table; one decision at a time, each with recommendation, reason, and plainly stated costs.

### Code
- External service: wrap as Client (one public method per endpoint, HTTP only) → Service (business logic) → application.
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
