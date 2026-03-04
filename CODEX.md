# CODEX.md

This file provides guidance when working with code in this repository.

## Project Overview

Codex Remote Hub is a lightweight Python web server that exposes Codex CLI sessions on mobile browsers via Tailscale. It manages multiple persistent sessions using tmux and serves web terminals through ttyd.

**Stack**: Python 3 (stdlib only, zero dependencies) + ttyd + tmux + Tailscale
**Platforms**: macOS, Linux, Windows (WSL2)

## Architecture

```
Phone/Browser  ←── Tailscale (VPN) ──→  Computer
                                         ├── :7690  codex-remote-hub.py (HTTP dashboard)
                                         └── :77xx  ttyd → tmux → codex (per session)
```

- `codex-remote-hub.py` — HTTP server (stdlib `http.server`). Config, platform detection, helpers, session management, HTTP handler, CLI.
- `templates/hub.html` — Dashboard HTML/CSS/JS. Placeholders: `{{SESSION_CARDS}}`, `{{COUNT_TEXT}}`, `{{VERSION}}`.
- `templates/terminal.html` — Terminal wrapper HTML/CSS/JS with 2-row virtual keyboard. Placeholders: `{{SESSION_NAME}}`, `{{TERMINAL_URL}}`.
- `install.sh` — Cross-platform installer (macOS/Linux/WSL2). Auto-detects OS and package manager.

### Key code sections in `codex-remote-hub.py`

- **Platform Detection** (top): `PLATFORM`, `IS_WSL`, `_find_bin()` via `shutil.which()`
- **Config**: Environment variables, port ranges (7700-7799), `INSTALL_DIR`
- **Helpers**: `_check_dependencies()`, `_load_template()`, `port_for_name()`, `get_sessions()`, `start_session()` / `stop_session()`
- **Port Detection**: `lsof` (macOS) → `ss` (Linux fallback) → socket fallback
- **HTML Rendering**: `render_hub()` and `render_terminal()` load templates and replace placeholders
- **HTTP Handler**: `HubHandler(BaseHTTPRequestHandler)` with all routes
- **CLI**: `cmd_start()`, `cmd_stop()`, `cmd_status()` subcommands

## Deployment Workflow

After editing files, deploy to the local instance:

```bash
cp codex-remote-hub.py ~/.codex-remote-hub/codex-remote-hub.py
cp templates/*.html ~/.codex-remote-hub/templates/
pkill -f "ttyd.*-p 77"
~/.codex-remote-hub/ctl.sh restart
```

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `CODEX_REMOTE_HUB_PORT` | `7690` | Dashboard port |
| `CODEX_FONT_SIZE` | `11` | Terminal font size |
| `CODEX_DEV_ROOT` | `~/Projects` | Root dir for folder picker |
| `CODEX_REMOTE_HUB_DIR` | `~/.codex-remote-hub` | Installation directory |
| `TTYD_BIN` | auto-detected | ttyd binary path |
| `TMUX_BIN` | auto-detected | tmux binary path |
| `CODEX_BIN` | auto-detected | Codex CLI path |

## Cross-Platform Notes

- Binary paths resolved via `shutil.which()` — no hardcoded paths
- Port detection: `lsof` → `ss` → socket fallback
- Autostart: LaunchAgent (macOS), systemd (Linux), manual (WSL)
- install.sh auto-detects OS and package manager

## Mobile Notes

- HTTPS required for iOS Safari (blocks ws:// in iframes)
- iOS redirected directly to ttyd URL (no iframe)
- Android works with iframe approach
- Virtual keyboard hidden on desktop via `@media (hover: hover)`
- System fonts only (no external font loading)

## Important Notes

- All code, comments, and documentation in English
- Version in `VERSION` constant in `codex-remote-hub.py`
- No automated tests or linter configured
- Session names map to ports via MD5 hash (7700-7799)
- HTTPS via Tailscale certs, TLS 1.2+
- ThreadedHTTPServer for parallel requests
- Security: Tailscale network isolation + HTTPS
