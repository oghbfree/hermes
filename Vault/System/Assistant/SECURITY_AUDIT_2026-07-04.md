# Hermes Agent Security Audit Report
# Hermes Agent Security Audit Report
**Date:** 2026-07-04
**Time:** 18:20:34

## 1. Credential Exposure Check
Checking environment variables for potential credentials...
OPENCLAW_HOOKS_TOKEN=***
SAG_API_KEY=***
SSH_ASKPASS=/mingw64/bin/git-askpass.exe
WHISPER_API_KEY=***
HERMES_REDACT_SECRETS=true
HERMES_SESSION_KEY=agent:main:telegram:group:-1003784520976:12

Checking Hermes config files for potential credential keys (values redacted)...
In /c/Users/User/.hermes/config.yaml:
  api_max_retries: 3
  env_passthrough: []
    session_key: ''
    api_key: ''
    api_key: ''
    api_key: ''
    api_key: ''
    api_key: ''
    api_key: ''
    api_key: ''
[ENV CREDENTIALS REDACTED - live API keys (OpenRouter, XAI, Firecrawl, Telegram, Bitwarden) removed for security]

## 2. Channel Integrity Check
Gateway status:
✓ Windows login item installed: C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd
✓ Gateway process running (PID: 8924)

Channel directory (Telegram):
  "updated_at": "2026-06-18T17:22:37.145950",
  "platforms": {
    "telegram": [
      {
        "id": "-1003784520976:424",
        "name": "Agent Hermes / topic 424",
        "type": "group",
        "thread_id": "424"
      },
      {
        "id": "-1003784520976:4",
        "name": "Agent Hermes / topic 4",
        "type": "group",
        "thread_id": "4"
      },
      {
        "id": "-1003784520976:2",
        "name": "Agent Hermes / topic 2",
        "type": "group",
        "thread_id": "2"
      },
      {
        "id": "-1003784520976:6",

Telegram topic list (checking for topic 20):
  telegram:Agent Hermes / topic 2  [-1003784520976:2]
  telegram:Agent Hermes / topic 1  [-1003784520976:1]
  telegram:Agent Hermes / topic 424  [-1003784520976:424]
  telegram:Agent Hermes / topic 3225  [-1003784520976:3225]
  telegram:Agent Hermes / topic 18  [-1003784520976:18]
  telegram:Agent Hermes / topic 6  [-1003784520976:6]
  telegram:Agent Hermes / topic 14  [-1003784520976:14]
  telegram:Agent Hermes / topic 928  [-1003784520976:928]
  telegram:Agent Hermes / topic 10  [-1003784520976:10]
  telegram:Agent Hermes / topic 4  [-1003784520976:4]
  telegram:Agent Hermes / topic 5885  [-1003784520976:5885]
  telegram:Agent Hermes / topic 26  [-1003784520976:26]
  telegram:Agent Hermes / topic 12  [-1003784520976:12]

## 3. Recent Security Events Check
Checking gateway.log for security keywords (last 50 lines):
2026-06-18 09:16:19,206 WARNING gateway.run: Reconnect telegram error: telegram connect timed out after 30s, next retry in 300s
2026-06-18 09:21:23,408 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.167.220
2026-06-18 09:21:23,410 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.167.220 failed: All connection attempts failed
2026-06-18 09:21:23,411 WARNING gateway.platforms.telegram: [Telegram] Connect attempt 1/8 failed: httpx.ConnectError: All connection attempts failed — retrying in 1s
2026-06-18 09:21:24,414 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.167.220
2026-06-18 09:21:24,416 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.167.220 failed: All connection attempts failed
2026-06-18 09:21:24,417 WARNING gateway.platforms.telegram: [Telegram] Connect attempt 2/8 failed: httpx.ConnectError: All connection attempts failed — retrying in 2s
2026-06-18 09:21:26,420 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.167.220
2026-06-18 09:21:26,423 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.167.220 failed: All connection attempts failed
2026-06-18 09:21:26,424 WARNING gateway.platforms.telegram: [Telegram] Connect attempt 3/8 failed: httpx.ConnectError: All connection attempts failed — retrying in 4s
2026-06-18 09:21:30,435 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.167.220
2026-06-18 09:21:30,437 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.167.220 failed: All connection attempts failed
2026-06-18 09:21:30,438 WARNING gateway.platforms.telegram: [Telegram] Connect attempt 4/8 failed: httpx.ConnectError: All connection attempts failed — retrying in 8s
2026-06-18 09:21:38,450 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.167.220
2026-06-18 09:21:38,453 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.167.220 failed: All connection attempts failed
2026-06-18 09:21:38,453 WARNING gateway.platforms.telegram: [Telegram] Connect attempt 5/8 failed: httpx.ConnectError: All connection attempts failed — retrying in 15s
2026-06-18 09:21:52,422 WARNING gateway.run: Reconnect telegram error: telegram connect timed out after 30s, next retry in 300s
2026-06-18 17:14:19,582 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.166.110
2026-06-18 17:14:19,608 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.166.110 failed: All connection attempts failed
2026-06-18 17:14:19,670 WARNING gateway.platforms.telegram: [Telegram] Telegram network error, scheduling reconnect: httpx.ConnectError: All connection attempts failed
2026-06-18 17:14:19,719 WARNING gateway.platforms.telegram: [Telegram] Telegram network error (attempt 1/10), reconnecting in 5s. Error: httpx.ConnectError: All connection attempts failed
2026-06-18 17:14:20,752 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.166.110
2026-06-18 17:14:20,814 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.166.110 failed: All connection attempts failed
2026-06-18 17:14:29,325 INFO gateway.platforms.telegram: [Telegram] Telegram polling resumed after network error (attempt 1)
2026-06-18 17:22:15,593 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.166.110
2026-06-18 17:22:15,626 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.166.110
2026-06-18 17:22:15,681 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.166.110 failed: All connection attempts failed
2026-06-18 17:22:15,715 WARNING gateway.platforms.telegram: [Telegram] Polling heartbeat probe failed 60s after reconnect: httpx.ConnectError: All connection attempts failed
2026-06-18 17:22:15,741 WARNING gateway.platforms.telegram: [Telegram] Telegram network error (attempt 1/10), reconnecting in 5s. Error: httpx.ConnectError: All connection attempts failed
2026-06-18 17:22:15,754 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.166.110 failed: All connection attempts failed
2026-06-18 17:22:15,765 WARNING gateway.platforms.telegram: [Telegram] Telegram network error, scheduling reconnect: httpx.ConnectError: All connection attempts failed
2026-06-18 17:22:15,775 WARNING gateway.platforms.telegram: [Telegram] Telegram network error (attempt 2/10), reconnecting in 10s. Error: httpx.ConnectError: All connection attempts failed
2026-06-18 17:22:16,788 WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed ([Errno 11001] getaddrinfo failed); trying fallback IPs 149.154.166.110
2026-06-18 17:22:16,791 WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.166.110 failed: All connection attempts failed
2026-06-18 17:22:25,051 INFO gateway.platforms.telegram: [Telegram] Telegram polling resumed after network error (attempt 1)
2026-06-18 17:22:29,983 INFO gateway.platforms.telegram: [Telegram] Telegram polling resumed after network error (attempt 2)

Checking cli.log for security keywords (last 50 lines):
cli.log not found.

## Summary for Telegram
hermes send: Telegram send failed: Chat not found
Summary sent to Telegram topic 20.
