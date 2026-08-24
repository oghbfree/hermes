import json, datetime

items = json.load(open(r'C:/Users/User/.hermes/workspace/Vault/business/2real/2real-agent/inventory_agent.json', encoding='utf-8'))

junk = {'none', '1 l', 'big', 'small', '1.5mm', '13mm', '19mm', '20mm', '150mm', '200mm', '250mm', '300',
        '210mm', 'rose', 'ash', 'luxury', '140kg bag', '56w', '1 padlock', '2 pack', 'graphite', 'twin pack',
        '4" brush', '04289', 'cardboard box', 'plastic box'}

# Meaningful low stock: in stock, 0<stock<=2, real name
low = []
for it in items:
    if not it.get('in_stock'):
        continue
    st = it.get('stock', 0)
    if not (0 < st <= 2):
        continue
    var = (it.get('variant') or '').strip()
    name = (it.get('name') or '').strip()
    full = (name + ' ' + var).strip()
    if not var or var.lower() in junk or len(var) < 3:
        continue
    low.append({'name': full, 'price': it.get('price', 0), 'stock': st, 'cat': it.get('category', '')})

print('meaningful low-stock items:', len(low))
low.sort(key=lambda x: (-x['price'], x['stock']))
print('--- TOP 12 BY VALUE ---')
for x in low[:12]:
    print(f"GHS {x['price']:>6} st{x['stock']} | {x['cat'][:20]:<20} | {x['name'][:55]}")

print()
print('--- ALMOST OUT: stock==1 count, stock==2 count ---')
s1 = sum(1 for x in low if x['stock'] == 1)
s2 = sum(1 for x in low if x['stock'] == 2)
print('stock=1:', s1, ' stock=2:', s2)

# total in-stock inventory for context
instock = [i for i in items if i.get('in_stock')]
print('total in_stock items:', len(instock))