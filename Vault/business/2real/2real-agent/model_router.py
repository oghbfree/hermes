#!/usr/bin/env python3
"""MODEL ROUTER (item 3, 27/10/26) — pick the cheapest tier that does the job.

Engines:
  cheap  = Ollama local (gemma4:latest chat / nomic-embed-text embeddings) — FREE
  hands  = deepseek/deepseek-v4-flash-0731 (openrouter) — the cron workhorse
  brain  = z-ai/glm-5.3-flash (root default) — synthesis/strategy, used sparingly

Rule: route to the CHEAPEST tier that does the job correctly.
- classification / transcription / summaries / embeddings / tagging  -> cheap (Ollama)
- posting / logging / checkins / daily ops / routine cron work      -> hands (deepseek)
- synthesis / tax audit / strategy / monthly review / big reasoning  -> brain (GLM)

USAGE:
  python model_router.py tier classify "text"        # run a cheap classification
  python model_router.py tier transcribe             # note: uses local STT
  python model_router.py route <task-kind>           # print which engine to use
"""
import sys, json, urllib.request

OLLAMA = 'http://localhost:11434'
OLLAMA_CHAT = 'gemma4:latest'

CHEAP_KINDS = {'classify', 'classification', 'tag', 'tagging', 'summary', 'summarize',
               'summaries', 'transcribe', 'embed', 'embedding', 'extract', 'dedupe'}
HANDS_KINDS = {'post', 'log', 'checkin', 'ops', 'daily', 'send', 'reply', 'harvest',
               'cron', 'monitor', 'ledger', 'invoice'}
BRAIN_KINDS = {'synthesis', 'synthesize', 'strategy', 'tax', 'audit', 'monthly',
               'review', 'plan', 'research', 'analyze'}


def classify(text):
    body = json.dumps({
        "model": OLLAMA_CHAT,
        "prompt": "Classify this 2Real item into ONE category: tools | electronics | "
                  "furniture | toys | sports | other. Reply with just the word.\n\nItem: " + text,
        "stream": False,
    }).encode()
    req = urllib.request.Request(OLLAMA + '/api/generate', data=body,
                                 headers={'Content-Type': 'application/json'})
    d = json.loads(urllib.request.urlopen(req, timeout=90).read())
    return d.get('response', '').strip()


def route(kind):
    k = kind.lower().replace('_', '-')
    # substring match: any kind word contained in the input OR input contained in a kind word
    for bucket, words in (('CHEAP', CHEAP_KINDS), ('HANDS', HANDS_KINDS), ('BRAIN', BRAIN_KINDS)):
        for w in words:
            if w in k or k in w:
                return bucket + ({
                    'CHEAP': ' (Ollama local, free)', 'HANDS': ' (deepseek-v4-flash-0731)',
                    'BRAIN': ' (GLM-5.3-flash)'}[bucket])
    return f'unknown kind "{kind}" — default to HANDS (deepseek)'


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(0)
    if a[0] == 'tier' and len(a) > 2 and a[1] == 'classify':
        print('category:', classify(' '.join(a[2:])))
    elif a[0] == 'route' and len(a) > 1:
        print(f'{a[1]} -> {route(a[1])}')
    else:
        print(__doc__)