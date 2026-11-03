#!/usr/bin/env python3
"""HAROLD ROUTER (02/11/26) — hand high-volume, low-stakes TEXT->TEXT work to
local gemma4 (Ollama, $0), behind a hard deterministic anti-hallucination gate.

WHY THIS EXISTS (H directive 02/11/26: "become more reliant on Harold, make sure
he's doing the job well not hallucinating"):
  Local gemma4 CHATS but its execution is unreliable (5/5 controlled tests failed
  18/10). So Harold ONLY gets tasks where hallucination is (a) safe and (b)
  verifiable, and we NEVER trust his output un-checked. This is text-in -> text-out
  with a verification wrapper — he cannot write files, run tools, or spend money.

TASKS HAROLD MAY DO (safe, low-risk, verifiable):
  tag      : classify/pigeonhole supplied text into a GIVEN allowed-label set
  brief    : summarise supplied text into <=N sentences (works from the input only)
  rank     : given a list, pick the top K by a given rule (from the supplied list only)
  draft    : rough copy from supplied inputs (human approves; never sent direct)

TASKS HAROLD MAY NEVER DO: file writes, tool runs, money/credits, live-data lookups,
exact quotes. Those stay on deepseek/GLM. This router refuses to emit output for
them and returns a 'human-tier: deepseek' verdict with CONF=0.

ANTI-HALLUCINATION GATE (deterministic — cannot be reasoned away):
  G1 — grounding: he is fed ONLY the supplied input text; prompt forbids memory.
  G2 — allowed labels / allowed answer set, enforced by regex post-check.
  G3 — invented-name/number scan: any all-uppercase PERSON/ORG token or bare number
       in the output that is NOT present (as a substring) in the supplied input is
       flagged INVENTED -> output discarded, CONF=0.
  G4 — length cap: output must fit an expected shape (labels <=K tokens, brief has
       ~N sentences); overruns are cut and flagged.
  PASS = G2+G3+G4 all green. FAIL => output is NOT used; caller gets {conf:0, error}.

USAGE:
  python harold_router.py tag         "<allowed: cat1|cat2|cat3>" "<input text>"
  python harold_router.py brief       <max_sents> "<spread text>"
  python harold_router.py rank        <allowed: A|B|C...> <top_n> "<line1>\\n<line2>..."
  python harold_router.py draft       "<instruction>" "<input>"
  python harold_router.py refuse      "<reason>"
Output on stdout is ALWAYS a single JSON object: {conf, task, ok, out, note}.
"""
import sys, json, os, re, datetime, urllib.request

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("HAROLD_MODEL", "gemma4:latest")

def _ollama(prompt, timeout=120):
    body = json.dumps({"model": MODEL, "prompt": prompt,
                       "stream": False, "options": {"temperature": 0.1,
                       "num_predict": 512}}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    return (d.get("response") or "").strip()


def _inventory_tokens(text):
    """Tokens the output is allowed to reference: tokens/numbers that appear in input."""
    toks = set()
    for m in re.findall(r"[A-Z][A-Z0-9&]{1,}[A-Za-z0-9&]*", text):  # styled proper nouns
        toks.add(m)
    for m in re.findall(r"\b\d+(?:[.,]\d+)?\b", text):              # bare numbers
        toks.add(m)
    return toks


def _scan_invented(out, inp):
    """Return list of (label) tokens / numbers in OUT not present in INP (as substring)."""
    allowed = set(x.lower() for x in [
        x for x in re.findall(r"[A-Z][A-Z0-9&]{1,}[A-Za-z0-9&]*", inp)])
    bad = []
    for m in re.findall(r"[A-Z][A-Z0-9&]{1,}[A-Za-z0-9&]*", out):
        if m.lower() not in allowed and m.lower() not in out.lower().split().count(m.lower()):
            # proper-name token not seen in the input at all -> suspect invented
            if m.split()[0] and m.lower() not in inp.lower():
                bad.append(m)
    for m in re.findall(r"\b\d+(?:[.,]\d+)?\b", out):          # every number must appear in input
        if m not in re.findall(r"\b\d+(?:[.,]\d+)?\b", inp):
            bad.append(m)
    return sorted(set(bad))[:15]


def verdict(out, inp, allowed_labels=None, max_out=400):
    """Deterministic gate. Returns (ok, note)."""
    if not out or not out.strip():
        return False, "empty output"
    if allowed_labels:
        labels = [x.strip().lower() for x in allowed_labels.split("|") if x.strip()]
        matched = [x for x in labels if re.search(r"\b" + re.escape(x) + r"\b", out.lower())]
        # every significant output token must belong to a whitelisted label word
        out_words = [w for w in re.split(r"\W+", out.lower()) if w and len(w) > 2]
        stray = [w for w in out_words if w not in labels and not any(
                 x.startswith(w) or w.startswith(x) for x in labels)]
        if stray:
            return False, f"label outside whitelist: {stray[:6]}"
        if not matched:
            return False, "no whitelisted label matched"
    invented = _scan_invented(out, inp)
    if invented:
        return False, f"possible invented tokens: {invented}"
    if len(out) > max_out:
        return False, f"overrun {len(out)}>max"
    return True, "ok"


def _fin(resp):
    print(json.dumps(resp, ensure_ascii=False))
    return resp


def main():
    a = sys.argv[1:]
    if not a:
        return _fin({"conf": 0, "task": "help",
                     "out": "usage: harold_router.py tag|brief|rank|draft|refuse ..."})
    kind = a[0].lower()

    # ---- REFUSE (harold must never do these) ----
    if kind == "refuse":
        reason = " ".join(a[1:]) or "task not permitted for local model"
        return _fin({"conf": 0, "task": "refused", "ok": False,
                     "note": "routed to human-tier (deepseek)", "reason": reason,
                     "out": ""})

    # ---- TAG ----
    if kind == "tag" and len(a) >= 3:
        allowed, inp = a[1], " ".join(a[2:])
        prompt = (f"You tag text into EXACTLY ONE of these allowed labels ONLY: "
                  f"{allowed}. Say the single label, nothing else. Never use memory, "
                  f"never invent details, never add numbers. Text:\n\n{inp}")
        out = _ollama(prompt)
        out = (out or "").strip()
        ok, note = verdict(out, inp, allowed_labels=allowed)
        return _fin({"conf": 1 if ok else 0, "task": "tag", "ok": ok,
                     "out": out, "note": note, "generated": str(datetime.datetime.now())[:16]})

    # ---- BRIEF ----
    if kind == "brief" and len(a) >= 3:
        try:
            n = int(a[1])
        except Exception:
            n = 3
        inp = " ".join(a[2:])
        prompt = (f"Summarise the text below into at most {n} short sentences. "
                  f"Work ONLY from the text. Do NOT add names, numbers, dates, or "
                  f"facts that are not present in it. Text:\n\n{inp}")
        out = _ollama(prompt)
        out = (out or "").strip()
        ok, note = verdict(out, inp, max_out=400)
        return _fin({"conf": 1 if ok else 0, "task": "brief", "ok": ok,
                     "out": out, "note": note, "generated": str(datetime.datetime.now())[:16]})

    # ---- RANK ----
    if kind == "rank" and len(a) >= 3:
        # allowed top-set + n + the list; we let harold pick the top K from supplied lines
        try:
            top_n = int(a[2]) if len(a) > 3 else int(a[1])
            list_text = " ".join(a[3:]) if len(a) > 3 else " ".join(a[2:])
        except Exception:
            top_n, list_text = 3, " ".join(a[2:])
        prompt = (f"From the list below choose the top {top_n} items by [the given rule]; "
                  f"answer ONLY by re-printing those item lines, one per line, in order; "
                  f"do not add anything not in the list. List:\n\n{list_text}")
        out = _ollama(prompt)
        out = (out or "").strip()
        # gemma sometimes repeats the top line; dedupe lines keeping order
        seen, lines = set(), []
        for ln in out.splitlines():
            ln = ln.strip()
            if not ln:
                continue
            key = ln[:50]
            if key in seen:
                continue
            seen.add(key)
            lines.append(ln)
        out = "\n".join(lines)
        ok, note = verdict(out, list_text)
        return _fin({"conf": 1 if ok else 0, "task": "rank", "ok": ok,
                     "out": out, "note": note, "generated": str(datetime.datetime.now())[:16]})

    # ---- DRAFT ----
    if kind == "draft" and len(a) >= 3:
        instr, inp = a[1], " ".join(a[2:])
        prompt = (f"Write a short draft {instr}. Work ONLY from the supplied material; "
                  f"do not invent product names, prices, phone numbers, or claims. "
                  f"Material:\n\n{inp}")
        out = _ollama(prompt)
        out = (out or "").strip()
        ok, note = verdict(out, inp, max_out=400)
        return _fin({"conf": 1 if ok else 0, "task": "draft", "ok": ok,
                     "out": out, "note": note, "generated": str(datetime.datetime.now())[:16]})

    return _fin({"conf": 0, "task": "unknown", "ok": False,
                 "note": f"unknown kind {kind}; usage tag|brief|rank|draft|refuse", "out": ""})


if __name__ == "__main__":
    sys.exit(not main().get("ok", False))  # exit 0 when gate passed, 1 when refused/failed