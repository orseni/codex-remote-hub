# OpenAI Codex CLI Has No Remote Access Solution. So I Built One.

*Claude Code already has two options for mobile access — an official one and an open-source one. Codex CLI has zero. Until now.*

---

## The State of Remote CLI Access in 2026

If you use **Claude Code** (Anthropic's coding CLI), you have options for accessing it remotely:

1. **Remote Control** — Anthropic's official solution. Run `/rc` inside a session, scan a QR code, and continue from your phone via the Claude app. Zero config, native mobile UI, conversation sync. It works well for quick check-ins.

2. **[Claude Remote Hub](https://github.com/orseni/claude-remote-hub)** — An open-source project I built months before Remote Control existed. It runs a lightweight Python server that exposes full Claude Code terminal sessions to any browser via Tailscale. Start sessions from your phone, capture running processes, persistent tmux sessions, full CLI with every slash command and Skill.

Between those two, Claude Code users are well-served. Whether you want the polished native experience (Remote Control) or the full terminal power (Claude Remote Hub), there's a solution.

But if you use **OpenAI's Codex CLI**? Nothing. No official remote access. No community tools. You're tied to your desk.

## Why This Matters

Codex CLI (`npm install -g @openai/codex`) is a capable tool. It reads your codebase, writes code, executes commands — much like Claude Code. But unlike Claude Code, there's no way to:

- **Check on a long-running task** from your phone
- **Start a new coding session** when you're away from your computer
- **Capture an existing Codex session** and continue it from another device
- **Keep sessions alive** after closing your terminal

These aren't edge cases. They're daily workflows for anyone who uses AI coding assistants seriously.

## Introducing Codex Remote Hub

**[Codex Remote Hub](https://github.com/orseni/codex-remote-hub)** brings the same remote access capabilities to Codex CLI that Claude Remote Hub brought to Claude Code.

The architecture is identical — because it works:

```
Phone/Browser  ←── Tailscale (VPN) ──→  Your Computer
                                         ├── :7690  Dashboard (web)
                                         └── :77xx  ttyd → tmux → codex
```

### What You Get

- **Start sessions from your phone** — open the dashboard, name a session, pick a project directory, and you're in a full Codex CLI terminal
- **Persistent sessions** — powered by tmux. Close your browser, sleep your phone. Come back hours later. Everything is exactly where you left it
- **Capture running sessions** — already have Codex running in a terminal? The hub detects it and lets you fork it into a browser-accessible session with `codex fork`
- **Full CLI experience** — it's your real terminal, not a simplified chat interface. Every command, every feature, every interactive prompt
- **Secure by default** — runs over Tailscale's mesh VPN. No ports exposed to the internet. HTTPS with TLS 1.2+
- **Zero Python dependencies** — pure stdlib. One file, ~1000 lines

### Getting Started

```bash
# 1. Make sure you have Codex CLI installed
npm install -g @openai/codex

# 2. Clone and install
git clone https://github.com/orseni/codex-remote-hub.git
cd codex-remote-hub
bash install.sh

# 3. Open on your phone
# https://your-machine.tailnet.ts.net:7690
```

The installer handles everything: installs tmux and ttyd, sets up autostart (LaunchAgent on macOS, systemd on Linux), and requests HTTPS certificates from Tailscale.

## The Mapping: Claude → Codex

For those familiar with Claude Remote Hub, here's what changed:

| Claude Code | Codex CLI |
|---|---|
| `claude` binary | `codex` binary |
| `npm install -g @anthropic-ai/claude-code` | `npm install -g @openai/codex` |
| `--dangerously-skip-permissions` | `--dangerously-bypass-approvals-and-sandbox` |
| `--resume ID --fork-session` | `codex fork ID` |
| `--continue` | `codex resume --last` |
| `CLAUDECODE` env var | `CODEX_HOME` env var |
| `~/.claude/projects/` sessions | `~/.codex/sessions/` |
| Orange accent (#E8734A) | OpenAI green (#10a37f) |
| CLAUDE.md | CODEX.md |

The server architecture, security model, mobile UI, and installation process are identical. If you've used one, you already know how to use the other.

## Why Not Wait for OpenAI?

OpenAI may eventually ship their own remote access solution for Codex CLI. Anthropic did it with Remote Control. But:

1. **There's no timeline** — OpenAI hasn't announced anything
2. **The need is now** — if you use Codex CLI daily, you need mobile access today
3. **Open source fills gaps** — Claude Remote Hub existed for months before Anthropic shipped Remote Control. Both coexist because they serve different needs
4. **Full CLI vs. simplified UI** — even if OpenAI ships something, it will likely be a simplified mobile interface (like Remote Control). A terminal-based approach gives you the full CLI

## A Quick Comparison

| Feature | Claude Code | Codex CLI |
|---|---|---|
| Official remote access | Remote Control | None |
| Open-source remote hub | [Claude Remote Hub](https://github.com/orseni/claude-remote-hub) | [Codex Remote Hub](https://github.com/orseni/codex-remote-hub) |
| Start sessions from phone | Yes (both solutions) | Yes (Codex Remote Hub) |
| Persistent sessions | Yes (Claude Remote Hub) | Yes (Codex Remote Hub) |
| Session capture | Yes (Claude Remote Hub) | Yes (Codex Remote Hub) |
| Full CLI from mobile | Yes (Claude Remote Hub) | Yes (Codex Remote Hub) |

## The Stack

Same proven Unix composition:

- **Python 3** (stdlib only) — the server, ~1000 lines
- **tmux** — session persistence
- **ttyd** — terminal to web bridge
- **Tailscale** — encrypted mesh VPN + HTTPS certs

No frameworks. No cloud services. No build step. No dependencies to audit.

## Try It

Codex Remote Hub is open source under the MIT license.

**GitHub**: [github.com/orseni/codex-remote-hub](https://github.com/orseni/codex-remote-hub)

If you're using Codex CLI and want mobile access, give it a try. Stars, issues, and PRs are welcome.

And if you use Claude Code instead, check out [Claude Remote Hub](https://github.com/orseni/claude-remote-hub) — the original that started it all.

---

*I built Claude Remote Hub to solve my own problem. When Codex CLI launched without remote access, the migration was straightforward — same architecture, different CLI. The Unix philosophy of composable tools means the solution works regardless of which AI coding assistant you prefer.*

---

**Tags**: `#OpenAI` `#Codex` `#CodexCLI` `#ClaudeCode` `#AI` `#Developer-Tools` `#Open-Source` `#CLI` `#Mobile-Development` `#Tailscale` `#Python` `#Remote-Development`
