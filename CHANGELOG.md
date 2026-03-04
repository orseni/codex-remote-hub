# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-04

### Added
- **Initial release** — migrated from [Claude Remote Hub](https://github.com/orseni/claude-remote-hub) for OpenAI Codex CLI
- **Dashboard** — web-based session manager with mobile-first dark theme (OpenAI green accent)
- **Session management** — create, stop, and list Codex CLI sessions via tmux
- **Web terminal** — ttyd-based terminal with virtual keyboard for mobile
- **Session capture** — detect running Codex CLI processes and fork them into hub-managed sessions using `codex fork`
- **Cross-platform** — macOS (LaunchAgent), Linux (systemd), Windows (WSL2)
- **Cross-platform installer** (`install.sh`) — auto-detects OS and package manager
- **HTTPS support** — automatic Tailscale certificate setup, TLS 1.2+
- **Folder picker** — browse and select project directories from the dashboard
- **Permission mode** — optional `--dangerously-bypass-approvals-and-sandbox` toggle
- **API endpoints** — 13 routes for session management, terminal control, and folder browsing
- **Zero dependencies** — pure Python stdlib, no pip packages
- Complete open source infrastructure: MIT license, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, ROADMAP.md
- GitHub issue templates (bug report, feature request) and PR template
