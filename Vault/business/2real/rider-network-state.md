# 2Real — Rider Network State (source for the Sunday availability check)

> **SOURCE OF TRUTH for riders.** The Sunday rider-check cron (`cfaf31ec0569`) reads THIS file
> and messages EVERY rider listed below. **Add a new rider = add a row; the cron picks them up next Sunday.**
>
> **How the messages evolve per rider (self-taught, once):**
> - Base location UNKNOWN → the message asks availability **+** base location (first send).
> - Base location KNOWN → the message asks **availability only** (all later sends).
> - Price is NEVER pre-asked — H quotes it on the day after the customer gives their exact drop-off landmark.
>
> **To add a rider:** tell sat-nav `2REAL: add rider <Name> +233 XX XXX XXXX` (and the base if you already
> know it). sat-nav adds a row; the cron messages them next Sunday (availability-only if you gave the base).
> **To update a base / drop a rider:** same — tell sat-nav; sat-nav edits this file.

## Riders (cron sends to ALL of these every Sunday)

| Rider | WhatsApp | Base location (Accra) | Known? | Last confirmed |
|-------|----------|----------------------|--------|----------------|
| Bernard | +233 24 544 4141 | _(pending first reply)_ | no | — |
| Jerry | +233 54 041 8575 | _(pending first reply)_ | no | — |
| Eben | +233 24 757 5993 | _(pending first reply)_ | no | — |
| Godwin (Eben's rider) | +233 54 765 2010 | Adenta | yes | 21/10/26 — returned 500W inverter from act (Eben unavailable) |
| Abdul (Yango) | +233 25 774 7640 | _(pending first reply)_ | no | — |
| Justice (Yango) | +233 59 951 3321 | _(pending first reply)_ | no | — |
| Jacob (Yango) | +233 59 844 4870 | _(pending first reply)_ | no | — |
<!-- Add new riders below this line (copy a row, keep the table format). -->

## Availability log (each week's Monday 7–9am confirmations)
| Date | Rider | Available? | Notes |
|------|-------|-----------|-------|
| _(first run)_ | — | — | — |

## Rules (from H)
- Ask **price only AFTER** the customer's exact drop-off location is known (never pre-ask a price).
- Sunday 19:00 cron `cfaf31ec0569` drafts the messages; **H sends** them from his phone.
- Once a base is confirmed once, only ask availability going forward.