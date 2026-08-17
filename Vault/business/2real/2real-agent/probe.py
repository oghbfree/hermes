from jiji_zobaze_responder import load_zobaze, load_jiji_listings, draft_reply, jiji_match, zobaze_match

items = load_zobaze()
jiji = load_jiji_listings()
print('items', len(items), 'jiji', len(jiji))

probes = [
    'Do you have the Flopro hose spray gun?',
    'Tell me about the Lg 42 inch tv',
    'How much is hydraulic bottle jack?',
    'Can you do me a Samsung S25 ultra 512gb',
    'Makita 6280d drill',
    'Portable CD Player',
    'Poker Chip Set 300',
    'Weber bbq cover',
]
for q in probes:
    print('\nQ:', q)
    print('jiji:', jiji_match(q, jiji))
    print('jiji+reply:', draft_reply(q, items, jiji))
