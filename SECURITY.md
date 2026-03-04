# Security Policy

## Security Model

Codex Remote Hub is designed to be accessed exclusively through a [Tailscale](https://tailscale.com) mesh VPN:

- **No ports exposed to the internet** — only devices on your private Tailscale network can reach Codex Remote Hub
- **HTTPS support** with TLS 1.2+ and modern cipher suites (ECDHE+AESGCM/CHACHA20) via Tailscale's Let's Encrypt certificates
- **No additional authentication** — Tailscale already authenticates every device on the network
- **Sessions run as your OS user** — same permissions as a local terminal session
- **Input validation** — special key whitelist, path traversal prevention on folder picker, paste size limits (10KB)

## What IS a Security Concern

Please report vulnerabilities related to:

- **Privilege escalation** — any way to execute commands outside the intended tmux session
- **Authentication bypass** — accessing sessions or APIs without being on the Tailscale network
- **Path traversal** — escaping the configured DEV_ROOT in the folder picker
- **Cross-site scripting (XSS)** — injection via session names, folder names, or API responses
- **Command injection** — via session names, API parameters, or user input
- **Information disclosure** — leaking sensitive data through API endpoints or error messages

## What is NOT a Security Concern for This Project

The following should be reported to the respective upstream projects:

- **Tailscale vulnerabilities** → [Tailscale Security](https://tailscale.com/security)
- **ttyd vulnerabilities** → [ttyd GitHub Issues](https://github.com/tsl0922/ttyd/issues)
- **tmux vulnerabilities** → [tmux GitHub Issues](https://github.com/tmux/tmux/issues)

## Reporting a Vulnerability

**Please DO NOT open a public GitHub issue for security vulnerabilities.**

Instead, use [GitHub Security Advisories](https://github.com/orseni/codex-remote-hub/security/advisories/new) to report vulnerabilities privately.

Include in your report:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

We will acknowledge your report within 48 hours and work with you on a timeline for a fix.

## Supported Versions

| Version | Supported |
|---|---|
| 1.x (latest) | Yes |
