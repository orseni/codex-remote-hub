# Roadmap

Community-driven feature list for Codex Remote Hub. Pick any item and open a PR!

## Planned Features

### Security & Access
- [ ] **Authentication layer** — optional password or token for an extra layer of security beyond Tailscale
- [ ] **Session sharing** — read-only spectator mode for pair programming
- [ ] **Per-session permissions** — restrict which directories a session can access

### User Experience
- [ ] **Dark/light theme toggle** — user-selectable theme with system preference detection
- [ ] **Session auto-cleanup** — configurable idle timeout to automatically stop unused sessions
- [ ] **Session logging/history** — save terminal output for later review
- [ ] **Multiple terminals per session** — leverage tmux windows within a single session
- [ ] **Session renaming** — rename sessions without restarting them
- [ ] **Keyboard shortcuts** — configurable hotkeys for common actions on the dashboard

### Real-time & Performance
- [ ] **WebSocket session list** — real-time dashboard updates without polling
- [ ] **Session health monitoring** — detect and auto-restart crashed sessions
- [ ] **Resource usage display** — show CPU/memory per session

### Infrastructure
- [ ] **Docker container** — run Codex Remote Hub in a container for easier deployment
- [ ] **Homebrew tap** — `brew install codex-remote-hub` for macOS users
- [ ] **Automated test suite** — pytest for the server, Playwright for the UI
- [ ] **CI/CD pipeline** — GitHub Actions for linting, testing, and releases

### Internationalization
- [ ] **i18n framework** — support multiple languages
- [ ] **Portuguese locale** — first community translation (pt-BR)

### Platform Support
- [ ] **Native Windows support** — without requiring WSL2
- [ ] **ARM Linux support** — verified Raspberry Pi compatibility
- [ ] **FreeBSD support** — for NAS and server users

## Contributing

1. Pick an item from the list above
2. Open an issue to discuss your approach
3. Submit a PR following [CONTRIBUTING.md](CONTRIBUTING.md)

Items marked with `[ ]` are open for contribution. If you're working on something, comment on the related issue so others know.
