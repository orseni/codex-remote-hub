#!/bin/bash
#
# Codex Remote Hub — Installer
# Access Codex CLI from any device via Tailscale
#
# Usage: bash install.sh
#        bash install.sh --uninstall
#

set -e

# ── Colors ──
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
DIM='\033[0;90m'
BOLD='\033[1m'
NC='\033[0m'

INSTALL_DIR="$HOME/.codex-remote-hub"
HUB_PORT=7690
LABEL="com.codex-remote-hub.server"

info()  { echo -e "${BLUE}i${NC}  $1"; }
ok()    { echo -e "${GREEN}+${NC}  $1"; }
warn()  { echo -e "${RED}!${NC}  $1"; }
step()  { echo -e "\n${BOLD}$1${NC}"; }

# ── OS Detection ──
detect_os() {
    case "$(uname -s)" in
        Darwin)
            OS="macos"
            ;;
        Linux)
            if grep -qi microsoft /proc/version 2>/dev/null; then
                OS="wsl"
            else
                OS="linux"
            fi
            ;;
        *)
            warn "Unsupported operating system: $(uname -s)"
            echo "  Codex Remote Hub supports macOS, Linux, and Windows (via WSL2)."
            exit 1
            ;;
    esac

    # Detect package manager (Linux/WSL)
    PKG_MGR=""
    if [ "$OS" = "linux" ] || [ "$OS" = "wsl" ]; then
        if command -v apt-get &>/dev/null; then
            PKG_MGR="apt"
        elif command -v dnf &>/dev/null; then
            PKG_MGR="dnf"
        elif command -v yum &>/dev/null; then
            PKG_MGR="yum"
        elif command -v pacman &>/dev/null; then
            PKG_MGR="pacman"
        fi
    fi
}

# ── Uninstall ──
do_uninstall() {
    step "Uninstalling Codex Remote Hub..."

    # Stop service
    if [ "$OS" = "macos" ]; then
        launchctl unload "$HOME/Library/LaunchAgents/${LABEL}.plist" 2>/dev/null || true
        rm -f "$HOME/Library/LaunchAgents/${LABEL}.plist"
    elif [ "$OS" = "linux" ]; then
        systemctl --user stop codex-remote-hub 2>/dev/null || true
        systemctl --user disable codex-remote-hub 2>/dev/null || true
        rm -f "$HOME/.config/systemd/user/codex-remote-hub.service"
        systemctl --user daemon-reload 2>/dev/null || true
    fi

    # Kill ttyd processes
    pkill -f "ttyd.*-p 77" 2>/dev/null || true

    # Remove files
    rm -rf "$INSTALL_DIR"
    rm -f /usr/local/bin/codex-remote-hub 2>/dev/null || sudo rm -f /usr/local/bin/codex-remote-hub 2>/dev/null || true

    ok "Codex Remote Hub has been uninstalled."
    exit 0
}

# ── Package Installation ──
install_package() {
    local name="$1"

    case "$OS" in
        macos)
            if ! command -v brew &>/dev/null; then
                warn "Homebrew not found. Installing..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install "$name"
            ;;
        linux|wsl)
            case "$PKG_MGR" in
                apt)    sudo apt-get update -qq && sudo apt-get install -y "$name" ;;
                dnf)    sudo dnf install -y "$name" ;;
                yum)    sudo yum install -y "$name" ;;
                pacman) sudo pacman -S --noconfirm "$name" ;;
                *)
                    warn "No supported package manager found."
                    echo "  Please install '$name' manually and re-run this script."
                    exit 1
                    ;;
            esac
            ;;
    esac
}

install_ttyd() {
    if command -v ttyd &>/dev/null; then
        return 0
    fi

    case "$OS" in
        macos)
            install_package ttyd
            ;;
        linux|wsl)
            if [ "$PKG_MGR" = "pacman" ]; then
                install_package ttyd
            elif command -v snap &>/dev/null; then
                info "Installing ttyd via snap..."
                sudo snap install ttyd --classic
            else
                warn "ttyd is not available in your package manager."
                echo "  Install options:"
                echo "    - Install snap: sudo apt install snapd && sudo snap install ttyd --classic"
                echo "    - Build from source: https://github.com/tsl0922/ttyd#installation"
                exit 1
            fi
            ;;
    esac
}

# ── Main ──
detect_os

# Handle --uninstall flag
if [ "${1:-}" = "--uninstall" ]; then
    do_uninstall
fi

echo ""
echo -e "${BOLD}  Codex Remote Hub — Installer${NC}"
echo -e "${DIM}  Platform: ${OS}${NC}"
echo ""

# ── 1. Check dependencies ──
step "1/6  Checking dependencies..."

# tmux
if ! command -v tmux &>/dev/null; then
    info "Installing tmux..."
    install_package tmux
fi
ok "tmux ($(tmux -V))"

# ttyd
if ! command -v ttyd &>/dev/null; then
    info "Installing ttyd..."
    install_ttyd
fi
ok "ttyd ($(ttyd --version 2>&1 | head -1))"

# Codex CLI
if ! command -v codex &>/dev/null; then
    warn "Codex CLI not found!"
    echo -e "   Install with: ${DIM}npm install -g @openai/codex${NC}"
    echo -e "   Then re-run this installer."
    exit 1
fi
ok "Codex CLI"

# Python 3
if ! command -v python3 &>/dev/null; then
    warn "Python 3 not found!"
    exit 1
fi
ok "Python 3 ($(python3 --version 2>&1))"

# Tailscale (optional)
if command -v tailscale &>/dev/null; then
    TS_STATUS=$(tailscale status --json 2>/dev/null | python3 -c "import sys,json;print(json.load(sys.stdin).get('Self',{}).get('DNSName','?'))" 2>/dev/null || echo "?")
    ok "Tailscale (${TS_STATUS})"
else
    warn "Tailscale not detected — access will be local only"
    info "Install from: https://tailscale.com/download"
fi

# ── 2. Install files ──
step "2/6  Installing Codex Remote Hub..."

mkdir -p "$INSTALL_DIR"

# Detect source directory
SRC_DIR="."
if [ ! -f "codex-remote-hub.py" ] && [ -f "$(dirname "$0")/codex-remote-hub.py" ]; then
    SRC_DIR="$(dirname "$0")"
fi

if [ ! -f "$SRC_DIR/codex-remote-hub.py" ]; then
    warn "codex-remote-hub.py not found in current directory!"
    info "Make sure to run the installer from the codex-remote-hub source directory."
    exit 1
fi

# Copy main script + templates
cp "$SRC_DIR/codex-remote-hub.py" "$INSTALL_DIR/codex-remote-hub.py"
chmod +x "$INSTALL_DIR/codex-remote-hub.py"

mkdir -p "$INSTALL_DIR/templates"
cp "$SRC_DIR/templates/"*.html "$INSTALL_DIR/templates/" 2>/dev/null

# Copy icon if available
if [ -f "$SRC_DIR/icon_cxhub.png" ]; then
    cp "$SRC_DIR/icon_cxhub.png" "$INSTALL_DIR/icon_cxhub.png"
fi

ok "Server + templates installed to $INSTALL_DIR"

# ── 3. Set up autostart ──
step "3/6  Setting up autostart..."

TTYD_PATH=$(which ttyd)
PYTHON_PATH=$(which python3)
CODEX_PATH=$(which codex)

case "$OS" in
    macos)
        PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"

        # Stop previous service if exists
        if launchctl list "$LABEL" &>/dev/null 2>&1; then
            info "Stopping previous service..."
            launchctl unload "$PLIST_PATH" 2>/dev/null || true
        fi

        cat > "$PLIST_PATH" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>${INSTALL_DIR}/codex-remote-hub.py</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/usr/sbin:/bin:$(dirname "$CODEX_PATH")</string>
        <key>TTYD_BIN</key>
        <string>${TTYD_PATH}</string>
        <key>CODEX_BIN</key>
        <string>${CODEX_PATH}</string>
        <key>HOME</key>
        <string>${HOME}</string>
        <key>CODEX_REMOTE_HUB_PORT</key>
        <string>${HUB_PORT}</string>
        <key>CODEX_REMOTE_HUB_DIR</key>
        <string>${INSTALL_DIR}</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${INSTALL_DIR}/hub.log</string>
    <key>StandardErrorPath</key>
    <string>${INSTALL_DIR}/hub-error.log</string>
    <key>WorkingDirectory</key>
    <string>${HOME}</string>
</dict>
</plist>
PLIST
        ok "macOS LaunchAgent created"
        ;;

    linux)
        mkdir -p "$HOME/.config/systemd/user"
        cat > "$HOME/.config/systemd/user/codex-remote-hub.service" << SVCEOF
[Unit]
Description=Codex Remote Hub - Codex CLI Terminal Server
After=network.target

[Service]
Type=simple
ExecStart=${PYTHON_PATH} ${INSTALL_DIR}/codex-remote-hub.py
Restart=on-failure
RestartSec=5
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin:$(dirname "$CODEX_PATH")
Environment=HOME=${HOME}
Environment=TTYD_BIN=${TTYD_PATH}
Environment=CODEX_BIN=${CODEX_PATH}
Environment=CODEX_REMOTE_HUB_PORT=${HUB_PORT}
Environment=CODEX_REMOTE_HUB_DIR=${INSTALL_DIR}
StandardOutput=append:${INSTALL_DIR}/hub.log
StandardError=append:${INSTALL_DIR}/hub-error.log

[Install]
WantedBy=default.target
SVCEOF

        systemctl --user daemon-reload
        systemctl --user enable codex-remote-hub 2>/dev/null || true

        # Enable lingering so service runs without active login session
        if command -v loginctl &>/dev/null; then
            loginctl enable-linger "$(whoami)" 2>/dev/null || true
        fi

        ok "systemd user service created"
        ;;

    wsl)
        info "WSL detected — no daemon service will be created."
        info "Start manually with: python3 ~/.codex-remote-hub/codex-remote-hub.py"
        info "Or add to your shell profile (~/.bashrc or ~/.zshrc)."
        ;;
esac

# ── 4. HTTPS certificates (Tailscale) ──
step "4/6  Setting up HTTPS certificates..."

CERT_FILE="$INSTALL_DIR/hub.crt"
KEY_FILE="$INSTALL_DIR/hub.key"

if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    ok "Certificates already exist"
elif command -v tailscale &>/dev/null; then
    TS_HOSTNAME=$(tailscale status --json 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin).get('Self',{}).get('DNSName','');print(d.rstrip('.'))" 2>/dev/null || echo "")
    if [ -n "$TS_HOSTNAME" ]; then
        info "Requesting Tailscale HTTPS certificate for $TS_HOSTNAME..."
        if sudo tailscale cert \
            --cert-file "$CERT_FILE" \
            --key-file "$KEY_FILE" \
            "$TS_HOSTNAME" 2>/dev/null; then
            # Fix ownership so the hub can read them
            sudo chown "$(whoami)" "$CERT_FILE" "$KEY_FILE"
            chmod 644 "$CERT_FILE"
            chmod 600 "$KEY_FILE"
            ok "HTTPS certificates installed for $TS_HOSTNAME"
        else
            warn "Could not obtain Tailscale certificate."
            info "You can set it up later: sudo tailscale cert --cert-file $CERT_FILE --key-file $KEY_FILE <hostname>"
        fi
    else
        warn "Tailscale hostname not detected. Skipping HTTPS setup."
    fi
else
    info "Tailscale not installed — HTTPS not configured (optional)."
    info "The hub will work over HTTP. For HTTPS, install Tailscale and re-run."
fi

# ── 5. Start service ──
step "5/6  Starting Codex Remote Hub..."

case "$OS" in
    macos)
        launchctl load "$PLIST_PATH"
        sleep 1
        if lsof -i ":${HUB_PORT}" &>/dev/null; then
            ok "Server running on port ${HUB_PORT}"
        else
            warn "Server may not have started. Check logs:"
            echo -e "   ${DIM}cat $INSTALL_DIR/hub-error.log${NC}"
        fi
        ;;
    linux)
        systemctl --user start codex-remote-hub
        sleep 1
        if systemctl --user is-active codex-remote-hub &>/dev/null; then
            ok "Server running on port ${HUB_PORT}"
        else
            warn "Server may not have started. Check logs:"
            echo -e "   ${DIM}journalctl --user -u codex-remote-hub -n 20${NC}"
        fi
        ;;
    wsl)
        nohup python3 "$INSTALL_DIR/codex-remote-hub.py" > "$INSTALL_DIR/hub.log" 2> "$INSTALL_DIR/hub-error.log" &
        echo $! > "$INSTALL_DIR/hub.pid"
        sleep 1
        if kill -0 "$(cat "$INSTALL_DIR/hub.pid" 2>/dev/null)" 2>/dev/null; then
            ok "Server running on port ${HUB_PORT} (PID $(cat "$INSTALL_DIR/hub.pid"))"
        else
            warn "Server may not have started. Check logs:"
            echo -e "   ${DIM}cat $INSTALL_DIR/hub-error.log${NC}"
        fi
        ;;
esac

# ── 6. Create control script ──
step "6/6  Creating control commands..."

cat > "$INSTALL_DIR/ctl.sh" << 'CTLEOF'
#!/bin/bash
LABEL="com.codex-remote-hub.server"
INSTALL_DIR="$HOME/.codex-remote-hub"

# Detect OS
case "$(uname -s)" in
    Darwin) OS="macos" ;;
    Linux)
        if grep -qi microsoft /proc/version 2>/dev/null; then
            OS="wsl"
        else
            OS="linux"
        fi
        ;;
esac

case "${1:-status}" in
    start)
        case "$OS" in
            macos)
                launchctl load "$HOME/Library/LaunchAgents/${LABEL}.plist" 2>/dev/null
                ;;
            linux)
                systemctl --user start codex-remote-hub
                ;;
            wsl)
                nohup python3 "$INSTALL_DIR/codex-remote-hub.py" > "$INSTALL_DIR/hub.log" 2> "$INSTALL_DIR/hub-error.log" &
                echo $! > "$INSTALL_DIR/hub.pid"
                ;;
        esac
        echo "  Codex Remote Hub started"
        ;;
    stop)
        case "$OS" in
            macos)
                launchctl unload "$HOME/Library/LaunchAgents/${LABEL}.plist" 2>/dev/null
                ;;
            linux)
                systemctl --user stop codex-remote-hub
                ;;
            wsl)
                if [ -f "$INSTALL_DIR/hub.pid" ]; then
                    kill "$(cat "$INSTALL_DIR/hub.pid")" 2>/dev/null
                    rm -f "$INSTALL_DIR/hub.pid"
                fi
                ;;
        esac
        pkill -f "ttyd.*-p 77" 2>/dev/null
        echo "  Codex Remote Hub stopped"
        ;;
    restart)
        "$0" stop && sleep 1 && "$0" start
        ;;
    status)
        running=false
        case "$OS" in
            macos)
                launchctl list "$LABEL" &>/dev/null 2>&1 && running=true
                ;;
            linux)
                systemctl --user is-active codex-remote-hub &>/dev/null && running=true
                ;;
            wsl)
                [ -f "$INSTALL_DIR/hub.pid" ] && kill -0 "$(cat "$INSTALL_DIR/hub.pid")" 2>/dev/null && running=true
                ;;
        esac
        if $running; then
            echo "  Codex Remote Hub is running"
            echo ""
            tmux list-sessions -F "   #{session_name}" 2>/dev/null | grep codex || echo "   No active sessions"
        else
            echo "  Codex Remote Hub is stopped"
        fi
        ;;
    logs)
        tail -f "$INSTALL_DIR/hub.log" "$INSTALL_DIR/hub-error.log"
        ;;
    uninstall)
        echo "Removing Codex Remote Hub..."
        "$0" stop 2>/dev/null
        case "$OS" in
            macos)
                rm -f "$HOME/Library/LaunchAgents/${LABEL}.plist"
                ;;
            linux)
                systemctl --user disable codex-remote-hub 2>/dev/null
                rm -f "$HOME/.config/systemd/user/codex-remote-hub.service"
                systemctl --user daemon-reload 2>/dev/null
                ;;
        esac
        rm -rf "$INSTALL_DIR"
        rm -f /usr/local/bin/codex-remote-hub 2>/dev/null || sudo rm -f /usr/local/bin/codex-remote-hub 2>/dev/null
        echo "  Codex Remote Hub removed"
        ;;
    *)
        echo "Usage: codex-remote-hub {start|stop|restart|status|logs|uninstall}"
        ;;
esac
CTLEOF

chmod +x "$INSTALL_DIR/ctl.sh"

# Create global symlink
ln -sf "$INSTALL_DIR/ctl.sh" /usr/local/bin/codex-remote-hub 2>/dev/null || \
    sudo ln -sf "$INSTALL_DIR/ctl.sh" /usr/local/bin/codex-remote-hub 2>/dev/null || \
    warn "Could not create symlink at /usr/local/bin (try running with sudo)"

ok "'codex-remote-hub' command available"

# ── Done ──

echo ""
echo -e "${BOLD}  Codex Remote Hub installed successfully!${NC}"
echo ""
PROTO="http"
if [ -f "$INSTALL_DIR/hub.crt" ] && [ -f "$INSTALL_DIR/hub.key" ]; then
    PROTO="https"
fi

echo -e " ${BOLD}Local access:${NC}"
echo -e "   ${PROTO}://localhost:${HUB_PORT}"
echo ""

# Re-detect Tailscale hostname if not already set
if [ -z "${TS_HOSTNAME:-}" ] && command -v tailscale &>/dev/null; then
    TS_HOSTNAME=$(tailscale status --json 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin).get('Self',{}).get('DNSName','');print(d.rstrip('.'))" 2>/dev/null || echo "")
fi

if [ -n "${TS_HOSTNAME:-}" ]; then
    echo -e " ${BOLD}Tailscale access (mobile):${NC}"
    echo -e "   ${GREEN}${PROTO}://${TS_HOSTNAME}:${HUB_PORT}${NC}"
    echo ""
fi
echo -e " ${BOLD}Commands:${NC}"
echo -e "   ${DIM}codex-remote-hub status${NC}     — check status"
echo -e "   ${DIM}codex-remote-hub stop${NC}       — stop server"
echo -e "   ${DIM}codex-remote-hub start${NC}      — start server"
echo -e "   ${DIM}codex-remote-hub restart${NC}    — restart server"
echo -e "   ${DIM}codex-remote-hub logs${NC}       — view logs"
echo -e "   ${DIM}codex-remote-hub uninstall${NC}  — uninstall"
echo ""
echo -e " ${BOLD}Tip:${NC} On your phone, open the link in your browser and"
echo -e "    use ${DIM}Share > Add to Home Screen${NC} to create an app icon!"
echo ""
