import json

items = json.load(open(r'C:/Users/User/.hermes/workspace/Vault/business/2real/2real-agent/inventory_agent.json', encoding='utf-8'))
print('total items:', len(items))

junk = {'none', '1 l', 'big', 'small', '1.5mm', '13mm', '19mm', '20mm', '150mm', '200mm', '250mm', '300',
        '210mm', 'rose', 'ash', 'luxury', '140kg bag', '56w', '1 padlock', '2 pack', 'graphite', 'twin pack',
        '4" brush', '04289', '1  l'}

seen = set()
cands = []
for it in items:
    if not it.get('in_stock'):
        continue
    st = it.get('stock', 0)
    if st < 5:
        continue
    p = it.get('price', 0)
    name = (it.get('name') or '').strip()
    var = (it.get('variant') or '').strip()
    full = (name + ' ' + var).strip()
    cat = it.get('category', '')
    if p < 15 or p > 400:
        continue
    if not var or var.lower() in junk or len(var) < 3:
        continue
    if full.lower() in seen:
        continue
    seen.add(full.lower())
    cost = it.get('cost') or 0
    margin = p - (cost if cost else p * 0.7)
    cands.append({'cat': cat, 'name': full, 'price': p, 'stock': st, 'margin': margin})

cands.sort(key=lambda x: (-x['margin'], -x['stock']))
print('candidates:', len(cands))

picked = {}
picks = []
for c in cands:
    if c['cat'] not in picked:
        picked[c['cat']] = True
        picks.append(c)
    if len(picks) >= 12:
        break

print('--- DIVERSIFIED PICKS (max 1 per category) ---')
for p in picks:
    print(f"{p['price']:>6} stock{p['stock']:>3} mg{p['margin']:>7.0f} | {p['cat'][:20]:<20} | {p['name'][:55]}")

print()
print('--- ALL CANDIDATES SCORED (top 20) ---')
for c in cands[:20]:
    print(f"{c['price']:>6} stock{c['stock']:>3} mg{c['margin']:>7.0f} | {c['cat'][:20]:<20} | {c['name'][:50]}")