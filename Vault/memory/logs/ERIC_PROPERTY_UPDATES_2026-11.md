# ERIC_PROPERTY_UPDATES — 2026-11

## 2026-11-25 — Check-in FAILED (automated, 3-day cadence)
- **WhatsApp NOT delivered to Eric** (E.164 447553403038). Bridge at localhost:3000 DOWN again — curl HTTP 000 on /send, netstat empty on :3000, no node process in tasklist. 4th consecutive fail at this cadence (11-19/11-22/now, plus 11-07).
- **Message intended:** "Hi Eric, checking in on UK property matters: any updates on letters, viewings, adverts, or ground coordination needed? Also please pick up the phone from Peckham."
- **Escalated to Telegram Topic 2** (chat -1003784520976 Topic 2; Topic 141 #urgent known-dead), hermes send returned "sent" 09:3x UTC.
- **NEXT ACTION (human, CRITICAL):** bridge has been down 4 runs straight now — WA session logged out since ~11-14 and nobody re-linked it. Manual action is mandatory: relaunch `node bridge.js` (hermes-agent/scripts/whatsapp-bridge), scan QR to re-auth, then resend to 447553403038. This automated check-in cannot work until the bridge is re-linked.
- **STANDING ITEM remains open:** pick up phone from Safi at Peckham repair shop.

## 2026-11-22 — Check-in FAILED (automated, 3-day cadence)
- **WhatsApp NOT delivered to Eric** (E.164 447553403038). Bridge at localhost:3000 DOWN — no listener on port 3000 (curl HTTP 000 / netstat empty). Same recurring state as 11-19 / 11-07.
- **Message intended:** "Hi Eric, checking in on UK property matters: any updates on letters, viewings, adverts, or ground coordination needed? Also please pick up the phone from Safi at Peckham phone repair shop."
- **Escalated to Telegram Topic 2** (chat -1003784520976; Topic 141 #urgent known-dead), hermes send returned "sent" 06:0x UTC.
- **NEXT ACTION (human, still open):** relaunch bridge `node bridge.js` (hermes-agent/scripts/whatsapp-bridge), scan QR to re-authenticate (session logged out since ~11-14), then resend check-in to 447553403038. Waited 3 runs now — bridge needs human re-link.
- **STANDING ITEM remains open:** pick up phone from Safi at Peckham repair shop.

## 2026-11-19 — Check-in FAILED (automated, 3-day cadence)
- **WhatsApp NOT delivered to Eric** (E.164 447553403038). Bridge at localhost:3000 DOWN — connection refused (curl exit 7, HTTP 000). No node/bridge process running (tasklist clean).
- **Root cause (bridge.log):** session in "❌ Logged out. Delete session and restart to re-authenticate." followed by Node crash `UND_ERR_RES_CONTENT_LENGTH_MISMATCH` (2026-11-14 02:56) → process exited. WA requires QR re-link, manual action.
- **Message intended:** "Hi Eric, checking in on UK property matters: any updates on letters, viewings, adverts, or ground coordination needed? Also please pick up the phone from Peckham."
- **Escalated to Telegram Topic 2** (chat -1003784520976 Topic 2; Topic 141 #urgent known-dead), delivered "sent" 06:0x UTC via hermes send.
- **NEXT ACTION (human):** relaunch bridge `node bridge.js` (hermes-agent/scripts/whatsapp-bridge, exe at bin/hermes.exe context), scan QR to re-authenticate, then resend check-in to 447553403038.

## 2026-11-16 — Check-in sent (automated, 3-day cadence)
- **WhatsApp delivered to Eric** (E.164 447553403038), msgId `3EB07DC23D97608062E8B1` (HTTP 200 via python stdlib — curl behaved erratically in cron shell).
- **Message:** "Hi Eric, checking in on UK property matters: any updates on letters, viewings, adverts, or ground coordination needed? Also please pick up the phone from Peckham."
- **Telegram Topic 2 notified** (chat -1003784520976 Topic 2).
- Sender: coach profile cron (Eric Property Check-in).

## 2026-11-07 — Check-in FAILED (automated, 3-day cadence)
- **WhatsApp NOT delivered to Eric** (E.164 447553403038). Bridge at localhost:3000 DOWN (connect refused, exit 7) — no listener.
- **Root cause (bridge.log 05:39–05:57):** session in "❌ Logged out. Delete session and restart to re-authenticate." — WA requires QR re-link, manual action.
- **Message intended:** "Hi Eric, checking in on UK property matters: any updates on letters, viewings, adverts, or ground coordination needed? Also please pick up the phone from Peckham."
- **Escalated to Telegram Topic 2** (Topic 141 #urgent known-dead), msg_id 13114, datetime 2026-11-07 ~06:0x UTC.
- **NEXT ACTION (human):** relaunch bridge `node bridge.js` (hermes-agent/scripts/whatsapp-bridge), scan QR to re-authenticate, then resend check-in to 447553403038.

## 2026-11-04 — Check-in sent (automated, 3-day cadence)
- **WhatsApp delivered to Eric** (E.164 447553403038), msgId `3EB074F3BD6AA8FB102420`.
- **Message:** "Hi Eric, checking in on UK property matters: any updates on letters, viewings, adverts, or ground coordination needed? Also please pick up the phone from Peckham."
- **Telegram Topic 2 notified** (msg_id 13050).
- Sender: coach profile cron (Eric Property Check-in).

### Action items (awaiting Eric's reply)
- [ ] Pick up the phone from Peckham (standing item — stays until confirmed done).
- [ ] Await updates on: letters/correspondence, property viewings, adverts/listings, ground coordination.