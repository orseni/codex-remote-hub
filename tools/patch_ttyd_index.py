#!/usr/bin/env python3
"""Patch an installed ttyd index with Codex Remote Hub mobile controls."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

DEFAULT_INSTALL_DIR = Path(os.environ.get("CODEX_REMOTE_HUB_DIR", "~/.codex-remote-hub")).expanduser()
DEFAULT_INDEX = DEFAULT_INSTALL_DIR / "ttyd-index.html"

INJECTION = r'''
<style>
  .hub-topbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 99998;
    display: flex; align-items: center; gap: 6px;
    padding: 6px 10px; padding-top: calc(6px + env(safe-area-inset-top));
    background: #161616; border-bottom: 1px solid #2a2a2a;
    flex-shrink: 0;
  }
  .hub-back {
    background: none; border: none; color: #10a37f;
    font-size: 24px; padding: 4px 8px; cursor: pointer;
    -webkit-tap-highlight-color: transparent; text-decoration: none;
    flex-shrink: 0;
  }
  .hub-title {
    font-family: 'SF Mono', 'Menlo', monospace;
    font-size: 13px; font-weight: 600; color: #e0ddd5;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .hub-vk {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 99998;
    display: flex; flex-direction: column; gap: 3px;
    padding: 3px 4px;
    background: #161616; border-top: 1px solid #2a2a2a;
    margin-bottom: env(safe-area-inset-bottom);
  }
  .hub-vk-row {
    display: flex; gap: 3px;
    overflow-x: auto; -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .hub-vk-row::-webkit-scrollbar { display: none; }
  .hub-vk button {
    background: #0c0c0c; border: 1px solid #2a2a2a; color: #e0ddd5;
    padding: 7px 12px; border-radius: 6px;
    font-family: 'SF Mono', 'Menlo', monospace;
    font-size: 13px; font-weight: 600; cursor: pointer;
    white-space: nowrap; -webkit-tap-highlight-color: transparent;
    flex-shrink: 0; transition: all 0.1s;
  }
  .hub-vk button:active { background: #10a37f; border-color: #10a37f; color: #fff; transform: scale(0.93); }
  .hub-vk button.danger { color: #c44; border-color: rgba(204,68,68,0.3); }
  .hub-vk button.danger:active { background: #c44; border-color: #c44; color: #fff; }
  .hub-vk button.special { color: #5a9a5a; border-color: rgba(90,154,90,0.3); }
  .hub-vk button.special:active { background: #5a9a5a; border-color: #5a9a5a; color: #fff; }
  .hub-vk .sep { width: 1px; background: #2a2a2a; flex-shrink: 0; margin: 4px 2px; }

  html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; background: #0c0c0c; }
  body {
    --crh-bottom-reserve: calc(68px + env(safe-area-inset-bottom));
    --crh-keyboard-inset: 0px;
    padding-top: calc(40px + env(safe-area-inset-top)) !important;
    padding-bottom: var(--crh-bottom-reserve) !important;
    display: flex !important; flex-direction: column !important;
    box-sizing: border-box !important;
    height: 100vh !important; height: 100dvh !important;
    width: 100vw !important;
    max-width: 100vw !important;
  }
  #terminal-container, #terminal {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    min-height: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    position: relative !important;
    box-sizing: border-box !important;
    touch-action: none;
  }
  #terminal-container .terminal {
    width: 100% !important;
    max-width: 100% !important;
    height: 100% !important;
    padding: 2px 0 0 !important;
    box-sizing: border-box !important;
  }
  .xterm {
    height: 100% !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow: hidden !important;
  }
  .xterm-screen { height: 100% !important; width: 100% !important; max-width: 100% !important; }
  .xterm-viewport { overflow-y: auto !important; scrollbar-width: none !important; -webkit-overflow-scrolling: touch; }
  .xterm-viewport::-webkit-scrollbar { display: none !important; }
  body.crh-embedded {
    padding-top: 0 !important;
    --crh-bottom-reserve: 0px;
  }
  body.crh-embedded .hub-topbar,
  body.crh-embedded .hub-vk {
    display: none !important;
  }
  body.crh-no-vk {
    --crh-bottom-reserve: 0px;
  }
  body.crh-no-vk .hub-vk {
    display: none !important;
  }
  body.crh-native-keyboard {
    --crh-bottom-reserve: var(--crh-keyboard-inset);
  }
  body.crh-native-keyboard .hub-vk {
    display: none !important;
  }

  @media (hover: hover) and (pointer: fine) {
    .hub-topbar { display: none !important; }
    .hub-vk { display: none !important; }
    body {
      padding-top: 0 !important;
      padding-bottom: 0 !important;
    }
    #terminal-container, #terminal { touch-action: auto; }
  }
</style>

<div class="hub-topbar">
  <a class="hub-back" id="hub-back" onclick="hubGoBack(); return false;">&#8249;</a>
  <span class="hub-title" id="hub-title">terminal</span>
</div>

<div class="hub-vk" id="hub-vk">
  <div class="hub-vk-row">
    <button onclick="hubSK('Escape')">Esc</button>
    <button class="special" onclick="hubScroll('up')">PgUp</button>
    <button class="special" onclick="hubScroll('down')">PgDn</button>
    <button onclick="hubSK('BTab')">&#8679;Tab</button>
    <div class="sep"></div>
    <button class="special" onclick="hubSK('Enter')">&#9166;</button>
    <button onclick="hubSK('Up')">&#9650;</button>
    <button onclick="hubSK('Down')">&#9660;</button>
    <button onclick="hubSK('Left')">&#9664;</button>
    <button onclick="hubSK('Right')">&#9654;</button>
  </div>
  <div class="hub-vk-row">
    <button onclick="hubText('/')">/</button>
    <button onclick="hubSK('Tab')">Tab</button>
    <button class="danger" onclick="hubSK('C-c')">^C</button>
    <button onclick="hubSK('C-z')">^Z</button>
    <button onclick="hubSK('C-d')">^D</button>
    <button onclick="hubSK('C-l')">^L</button>
    <button onclick="hubSK('C-a')">^A</button>
    <button onclick="hubSK('C-e')">^E</button>
    <button onclick="hubSK('C-r')">^R</button>
    <button onclick="hubSK('C-u')">^U</button>
    <button onclick="hubSK('C-k')">^K</button>
    <button onclick="hubSK('C-w')">^W</button>
    <div class="sep"></div>
    <button class="special" onclick="hubPaste()">Paste</button>
  </div>
</div>

<script>
(function(){
  var hubOrigin = '';
  var sessionName = '';
  var csrfToken = '';
  var isEmbedded = false;
  var keyboardFallbackUntil = 0;

  try {
    isEmbedded = window.self !== window.top;
  } catch(e) {
    isEmbedded = true;
  }

  if (isEmbedded) document.body.classList.add('crh-embedded');

  try {
    var params = new URLSearchParams(location.hash.substring(1));
    hubOrigin = params.get('hub') || '';
    sessionName = params.get('session') || '';
    csrfToken = params.get('csrf') || '';
  } catch(e) {}

  function getStored(primary, legacy) {
    try {
      return localStorage.getItem(primary) || localStorage.getItem(legacy) || '';
    } catch(e) {
      return '';
    }
  }

  if (!hubOrigin) hubOrigin = getStored('codexRemoteHub_origin', 'codexHub_origin');
  if (!sessionName) sessionName = getStored('codexRemoteHub_session', 'codexHub_session');
  if (!csrfToken) csrfToken = getStored('codexRemoteHub_csrf', 'codexHub_csrf');

  try {
    if (hubOrigin) localStorage.setItem('codexRemoteHub_origin', hubOrigin);
    if (sessionName) localStorage.setItem('codexRemoteHub_session', sessionName);
    if (csrfToken) localStorage.setItem('codexRemoteHub_csrf', csrfToken);
  } catch(e) {}

  window.hubGoBack = function() {
    if (hubOrigin) {
      window.location.href = hubOrigin + '/';
    } else {
      history.back();
    }
  };

  var backBtn = document.getElementById('hub-back');
  if (hubOrigin) backBtn.href = hubOrigin + '/';
  if (sessionName) document.getElementById('hub-title').textContent = sessionName;

  var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (!isIOS) document.body.classList.add('crh-no-vk');

  function refitTerminal() {
    window.dispatchEvent(new Event('resize'));
  }

  function scheduleRefitTerminal() {
    setTimeout(refitTerminal, 0);
    setTimeout(refitTerminal, 80);
    setTimeout(refitTerminal, 260);
  }

  function touchDevice() {
    return window.matchMedia && window.matchMedia('(hover: none), (pointer: coarse)').matches;
  }

  function virtualKeyboardInset() {
    try {
      if (navigator.virtualKeyboard && navigator.virtualKeyboard.boundingRect) {
        return Math.max(0, navigator.virtualKeyboard.boundingRect.height || 0);
      }
    } catch(e) {}
    return 0;
  }

  function updateVisualViewport() {
    var vv = window.visualViewport;
    var vvHeight = vv ? vv.height : 0;
    var layoutHeight = Math.max(window.innerHeight || 0, document.documentElement.clientHeight || 0, vvHeight || 0);
    var offsetTop = vv ? (vv.offsetTop || 0) : 0;
    var viewportInset = vv ? Math.max(0, layoutHeight - vvHeight - offsetTop) : 0;
    var inset = Math.max(viewportInset, virtualKeyboardInset());
    var fallbackActive = touchDevice() && Date.now() < keyboardFallbackUntil;
    var keyboardOpen = inset > 80 || fallbackActive;
    if (keyboardOpen && inset < 120) {
      inset = Math.round(layoutHeight * 0.42);
    }
    if (layoutHeight > 0) {
      inset = Math.min(inset, Math.round(layoutHeight * 0.65));
    }
    document.body.style.setProperty('--crh-keyboard-inset', keyboardOpen ? Math.round(inset) + 'px' : '0px');
    document.body.classList.toggle('crh-native-keyboard', keyboardOpen);
    scheduleRefitTerminal();
    if (keyboardOpen) {
      var vp = viewport();
      if (vp) vp.scrollTop = vp.scrollHeight;
    }
  }

  setTimeout(refitTerminal, 100);
  setTimeout(refitTerminal, 300);
  setTimeout(refitTerminal, 1000);
  setTimeout(refitTerminal, 3000);
  setTimeout(updateVisualViewport, 100);
  try {
    var resizeTarget = document.getElementById('terminal-container') || document.getElementById('terminal');
    if (window.ResizeObserver && resizeTarget) {
      new ResizeObserver(function() { setTimeout(refitTerminal, 0); }).observe(resizeTarget);
    }
  } catch(e) {}
  try {
    if (window.visualViewport) {
      window.visualViewport.addEventListener('resize', updateVisualViewport);
      window.visualViewport.addEventListener('scroll', updateVisualViewport);
    }
    if (navigator.virtualKeyboard) {
      navigator.virtualKeyboard.addEventListener('geometrychange', updateVisualViewport);
    }
    window.addEventListener('orientationchange', function() { setTimeout(updateVisualViewport, 300); });
    document.addEventListener('focusout', function() {
      keyboardFallbackUntil = 0;
      setTimeout(updateVisualViewport, 120);
    }, true);
  } catch(e) {}

  function headers() {
    var value = {'Content-Type': 'application/json'};
    if (csrfToken) value['X-CSRF-Token'] = csrfToken;
    return value;
  }

  function post(path, payload) {
    if (!hubOrigin || !sessionName) return Promise.resolve();
    return fetch(hubOrigin + path + encodeURIComponent(sessionName), {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify(payload || {})
    }).catch(function(){});
  }

  window.hubSK = function(key) { post('/api/send-keys/', {key: key}); };
  window.hubText = function(text) { post('/api/send-text/', {text: text}); };
  window.hubScroll = function(dir) { post('/api/scroll/', {direction: dir}); };
  window.hubFocus = function() { post('/api/focus/', {}); };
  window.hubPaste = async function() {
    try {
      var text = await navigator.clipboard.readText();
      if (text) hubText(text);
    } catch(e) {}
  };

  function viewport() {
    return document.querySelector('.xterm-viewport');
  }

  function scrollViewport(deltaY) {
    var vp = viewport();
    if (!vp) return false;
    var before = vp.scrollTop;
    vp.scrollTop += deltaY;
    return vp.scrollTop !== before;
  }

  function dispatchWheel(deltaY) {
    var target = document.querySelector('.xterm-screen') || document.querySelector('.xterm') || viewport();
    if (!target || typeof WheelEvent === 'undefined') return false;
    try {
      target.dispatchEvent(new WheelEvent('wheel', {
        deltaY: deltaY,
        deltaMode: 0,
        bubbles: true,
        cancelable: true
      }));
      return true;
    } catch(e) {
      return false;
    }
  }

  function safeFocus(element) {
    if (!element || typeof element.focus !== 'function') return;
    try {
      element.focus({preventScroll: true});
    } catch(e) {
      try { element.focus(); } catch(_) {}
    }
  }

  function focusTerminal() {
    var term = document.querySelector('.xterm');
    var helper = document.querySelector('.xterm-helper-textarea');
    if (helper) {
      helper.setAttribute('autocapitalize', 'none');
      helper.setAttribute('autocorrect', 'off');
      helper.setAttribute('spellcheck', 'false');
    }
    safeFocus(term);
    safeFocus(helper);
    hubFocus();
    keyboardFallbackUntil = Date.now() + 2500;
    setTimeout(updateVisualViewport, 80);
    setTimeout(updateVisualViewport, 300);
    setTimeout(updateVisualViewport, 700);
    setTimeout(updateVisualViewport, 1200);
  }

  (function setupTouchScroll() {
    var startX = 0;
    var startY = 0;
    var lastY = 0;
    var scrolling = false;
    var fallbackAccum = 0;
    var usedTmuxFallback = false;
    var suppressFocusUntil = 0;

    function inChrome(target) {
      if (!target || !target.closest) return false;
      if (target.closest('.hub-vk, .hub-topbar, button, a')) return true;
      if (target.closest('input')) return true;
      var textarea = target.closest('textarea');
      return !!(textarea && !textarea.classList.contains('xterm-helper-textarea'));
    }

    document.addEventListener('touchstart', function(e) {
      if (e.touches.length !== 1 || inChrome(e.target)) return;
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      lastY = startY;
      scrolling = false;
      fallbackAccum = 0;
      usedTmuxFallback = false;
    }, {capture: true, passive: true});

    document.addEventListener('touchmove', function(e) {
      if (e.touches.length !== 1 || inChrome(e.target)) return;
      var x = e.touches[0].clientX;
      var y = e.touches[0].clientY;
      var totalX = Math.abs(x - startX);
      var totalY = Math.abs(y - startY);

      if (!scrolling) {
        if (totalY < 10 || totalY < totalX * 1.2) return;
        scrolling = true;
      }

      e.preventDefault();
      var deltaY = (lastY - y) * 1.15;
      lastY = y;

      if (!scrollViewport(deltaY)) {
        dispatchWheel(deltaY);
        fallbackAccum += deltaY;
        if (Math.abs(fallbackAccum) >= 72) {
          hubScroll(fallbackAccum > 0 ? 'down' : 'up');
          usedTmuxFallback = true;
          suppressFocusUntil = Date.now() + 900;
          fallbackAccum = 0;
        }
      }
    }, {capture: true, passive: false});

    document.addEventListener('touchend', function(e) {
      if (inChrome(e.target)) return;
      if (usedTmuxFallback) {
        suppressFocusUntil = Date.now() + 900;
        return;
      }
      var changed = e.changedTouches && e.changedTouches[0];
      if (!changed) return;
      var totalX = Math.abs(changed.clientX - startX);
      var totalY = Math.abs(changed.clientY - startY);
      if (!scrolling && totalX < 12 && totalY < 12) {
        focusTerminal();
      }
    }, {capture: true, passive: true});

    document.addEventListener('click', function(e) {
      if (Date.now() < suppressFocusUntil) return;
      if (!inChrome(e.target)) focusTerminal();
    }, true);
  })();
})();
</script>
'''


def patch_index(path: Path) -> None:
    data = path.read_text(encoding="utf-8")
    if ".hub-topbar" in data:
        patched = re.sub(
            r"\n<style>\s*\.hub-topbar\b.*?</script>\s*</body></html>\s*$",
            "\n" + INJECTION + "\n</body></html>\n",
            data,
            flags=re.S,
        )
        if patched == data:
            raise RuntimeError("existing Codex Remote Hub injection was found but could not be replaced")
    else:
        if "</body></html>" not in data:
            raise RuntimeError("ttyd index does not contain a closing body/html tag")
        patched = data.replace("</body></html>", "\n" + INJECTION + "\n</body></html>\n")

    path.write_text(patched, encoding="utf-8")


def main() -> int:
    path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_INDEX
    if not path.exists():
        print(f"ttyd index not found: {path}", file=sys.stderr)
        return 1
    patch_index(path)
    print(f"patched {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
