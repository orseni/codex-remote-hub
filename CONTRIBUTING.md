# Contributing to Codex Remote Hub

Thank you for your interest in contributing to Codex Remote Hub! This guide will help you get started.

## Development Environment

### Prerequisites

- **Python 3.8+** (stdlib only, no pip dependencies)
- **tmux** (session multiplexer)
- **ttyd 1.7.7+** (terminal sharing over HTTP)
- **Tailscale** (optional, for remote access over VPN)

### Setup

1. Fork the repository and clone your fork:

```bash
git clone https://github.com/<your-username>/codex-remote-hub.git
cd codex-remote-hub
```

2. Run locally:

```bash
python3 codex-remote-hub.py
```

The dashboard will be available at `http://localhost:7690`.

3. For HTTPS (required for mobile/iframe WebSocket support), configure Tailscale certificates:

```bash
tailscale cert <your-hostname>.ts.net
```

### Project Structure

```
codex-remote-hub/
├── codex-remote-hub.py          # Main server (config, helpers, HTTP handler, CLI)
├── install.sh             # Setup script (Homebrew/apt, LaunchAgent/systemd)
├── templates/
│   ├── hub.html           # Dashboard template
│   └── terminal.html      # Terminal wrapper template
├── CHANGELOG.md
├── ROADMAP.md
└── ...
```

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code
- Use **type hints** for function signatures
- Write comments and docstrings in **English**
- Keep the zero-dependency philosophy: stdlib only, no pip packages
- Use 4 spaces for Python indentation, 2 spaces for HTML/CSS/JS
- See `.editorconfig` for formatting details

## Commit Messages

Use present tense, imperative mood:

- `Add session auto-cleanup feature`
- `Fix WebSocket reconnection on iOS Safari`
- `Update dashboard layout for mobile`
- `Remove deprecated port configuration`

Keep the subject line under 72 characters. Add a body for complex changes.

## Pull Request Process

1. **Fork** the repository
2. Create a **feature branch** from `main`:
   ```bash
   git checkout -b add-session-timeout
   ```
3. Make your changes with clear, focused commits
4. **Test thoroughly** (see Testing below)
5. Push to your fork and open a **Pull Request** against `main`
6. Fill out the PR template with:
   - What you changed
   - Why you changed it
   - How it works
   - Testing checklist results

### PR Guidelines

- One feature or fix per PR
- Keep changes small and reviewable
- Update `CHANGELOG.md` under `[Unreleased]` if applicable
- Ensure your code works on at least one target platform (macOS, Linux, or WSL2)

## Testing

There is no automated test suite yet (contributions welcome! See [ROADMAP.md](ROADMAP.md)).

### Manual Testing Checklist

Before submitting a PR, verify:

- [ ] Server starts without errors: `python3 codex-remote-hub.py`
- [ ] Dashboard loads at `http://localhost:7690`
- [ ] Sessions can be created and stopped
- [ ] Terminal connects and renders correctly
- [ ] Virtual keyboard works (if you changed terminal.html)
- [ ] **Mobile testing**: If you changed templates, test on a real phone or responsive mode
- [ ] **Cross-platform**: If you changed `install.sh` or platform detection, test on the relevant OS

### Testing on Mobile

The primary use case is mobile access via Tailscale. Test with:

1. Safari on iOS (primary target)
2. Chrome on Android
3. Responsive mode in desktop browsers (secondary)

## Areas for Contribution

See [ROADMAP.md](ROADMAP.md) for a list of planned features and improvements. Some good areas for first contributions:

- Documentation improvements
- Cross-platform compatibility fixes
- UI/UX enhancements for mobile
- Adding automated tests

## Questions?

Open a [Discussion](https://github.com/orseni/codex-remote-hub/discussions) or an Issue. We are happy to help!
