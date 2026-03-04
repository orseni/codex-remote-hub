# Repository Guidelines

## Project Structure & Module Organization
- `codex-remote-hub.py` — main Python server (stdlib only: HTTP, session mgmt, CLI).
- `templates/` — HTML pages: `hub.html` (dashboard), `terminal.html` (wrapper + keyboard).
- `install.sh` — cross‑platform installer (Homebrew/apt/snap, LaunchAgent/systemd).
- Docs: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `ROADMAP.md`, `SECURITY.md`.

## Build, Test, and Development Commands
- Run locally: `python3 codex-remote-hub.py` → opens `http://localhost:7690`.
- Install system‑wide: `bash install.sh` → sets up service and binaries.
- Control service: `codex-remote-hub {start|stop|restart|status|logs}`.
- Deploy local edits to installed copy (manual): copy files to `~/.codex-remote-hub` and restart (see CODEX.md).

## Coding Style & Naming Conventions
- Python: PEP 8, 4‑space indent, type hints for public functions. Keep zero‑dependency (stdlib only).
- HTML/CSS/JS: 2‑space indent; keep assets inline/minimal for mobile performance.
- Naming: `snake_case` for functions/vars, `UPPER_SNAKE` for constants, module‑level functions preferred over classes.
- File formatting enforced via `.editorconfig` (respect line endings and final newline).

## Testing Guidelines
- No automated test suite yet. Use the manual checklist in `CONTRIBUTING.md`.
- Minimum before PR: start server, create/stop sessions, verify terminal renders, and test on a real phone (iOS Safari and/or Android Chrome).
- Cross‑platform changes (e.g., `install.sh`) must be verified on at least one target (macOS/Linux/WSL2).
- If adding tests, place them under `tests/` and mirror module names (e.g., `test_sessions.py`).

## Commit & Pull Request Guidelines
- Commits: imperative, present tense; ≤72‑char subject. Examples: `Add session auto-cleanup`, `Fix iOS WebSocket reconnect`.
- Link issues in PRs (e.g., `Closes #123`). Use the PR template; include what/why/how and screenshots for UI changes.
- Keep PRs small and focused; one change per PR. Update `CHANGELOG.md` under `[Unreleased]` when user‑visible.

## Security & Configuration Tips
- Do not expose ports publicly; recommend Tailscale and HTTPS via Tailscale certs.
- Never hardcode local paths or secrets. Use env vars: `CODEX_REMOTE_HUB_PORT`, `CODEX_FONT_SIZE`, `CODEX_DEV_ROOT`, `TTYD_BIN`, `TMUX_BIN`, `CODEX_BIN`.
- Preserve the zero‑dependency design: avoid adding external Python packages.

