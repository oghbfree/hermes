#!/usr/bin/env bash
# launch_2real_browser.sh — launch the ONE dedicated persistent browser all 2Real
# crons (WhatsApp/FB/Jiji posting) connect to via CDP.
#
# Why this exists:
# The fb/wa/jiji posting scripts don't launch a browser — they CONNECT to one you
# start with remote-debugging (cdp_harness.py). If that browser is started ad-hoc
# (or with an ephemeral profile), you have to re-login / re-link WhatsApp, Jiji,
# Facebook every time. THIS launcher starts Chrome with a FIXED persistent profile
# and a FIXED debug port, so:
#   - you log into WhatsApp Web, Jiji, FB Marketplace ONCE in this profile
#   - logins persist across reboots and crons
#   - every cron connects to the SAME running instance (localhost:9222)
#
# Usage:
#   bash launch_2real_browser.sh        # start/attach the browser (opens it for login first time)
#   bash launch_2real_browser.sh check  # verify the CDP port is live (no launch)
#
# After the first launch: log into whatsapp.web / jiji / facebook in this window.
# Then leave it open (or relaunch with this script) — crons will always find it.

# ---- config ----
CHROME="C:/Program Files/Google/Chrome/Application/chrome.exe"
PORT=9222
# Dedicated persistent profile — logins survive here. NOT the default Chrome profile.
# NOTE: use a NATIVE Windows path (C:/...), NOT MSYS /c/... — Chrome is a Windows
# program and would misread /c/... as C:\c\... and write to the wrong folder.
PROFILE="C:/Users/User/.hermes/workspace/Vault/business/2real/browser-profile"
# Check port already live?
RESP=$(curl -s --max-time 3 http://localhost:${PORT}/json/version 2>/dev/null)
if [ -n "$RESP" ]; then
  echo "ALREADY LIVE on :${PORT}"
  echo "$RESP" | grep -o '"Browser":"[^"]*"'
  echo "BROWSER IS UP — crons will connect here. (Profile: $PROFILE)"
  exit 0
fi
echo "No live CDP on :${PORT} — launching dedicated 2Real browser..."
mkdir -p "$PROFILE"
"$CHROME" \
  --remote-debugging-port=${PORT} \
  --user-data-dir="$PROFILE" \
  --no-first-run --no-default-browser-check \
  "https://web.whatsapp.com" &
sleep 6
RESP=$(curl -s --max-time 3 http://localhost:${PORT}/json/version 2>/dev/null)
if [ -n "$RESP" ]; then
  echo "OK — browser live on :${PORT}"
  echo "$RESP" | grep -o '"Browser":"[^"]*"'
  echo ">>> Log into WhatsApp Web / Jiji / FB Marketplace in this window ONCE."
  echo ">>> From now on run: bash launch_2real_browser.sh  (it attaches to the same profile)"
else
  echo "WARN: port didn't come up. Click 'Allow remote debugging?' if Chrome shows it."
fi