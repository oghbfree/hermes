import json
from collections import Counter

with open('inventory_agent.json') as f:
    data = json.load(f)

total = len(data)
in_stock = [i for i in data if i.get('in_stock', False)]
out_stock = [i for i in data if not i.get('in_stock', False)]
print("Total items:", total)
print("In stock:", len(in_stock))
print("Out of stock:", len(out_stock))
print()

price_ranges = Counter()
for i in in_stock:
    p = float(i.get('price', 0))
    if p <= 50: price_ranges['0-50'] += 1
    elif p <= 100: price_ranges['51-100'] += 1
    elif p <= 200: price_ranges['101-200'] += 1
    elif p <= 500: price_ranges['201-500'] += 1
    elif p <= 1000: price_ranges['501-1000'] += 1
    else: price_ranges['1000+'] += 1

print("In-stock items by price:")
for r in ['0-50','51-100','101-200','201-500','501-1000','1000+']:
    print("  GHS {}: {} items".format(r, price_ranges[r]))
print()

cats = Counter(i.get('category','Unknown') for i in in_stock)
print("Top categories (in stock):")
for cat, count in cats.most_common(15):
    print("  {}: {}".format(cat, count))
print()

high_stock = [i for i in in_stock if i.get('stock',0) >= 5]
print("Items with stock >= 5:", len(high_stock))

low_stock = [i for i in in_stock if i.get('stock',0) == 1]
print("Items with stock = 1:", len(low_stock))

single_digit = [i for i in in_stock if i.get('stock',0) <= 3]
print("Items with stock <= 3:", len(single_digit))
print()

with_margin = [i for i in in_stock if i.get('cost',0) and float(i.get('cost',0)) > 0]
print("Items with cost data:", len(with_margin))
print("Top 10 by margin:")
for i in sorted(with_margin, key=lambda x: float(x.get('price',0)) - float(x.get('cost',0)), reverse=True)[:10]:
    p = float(i.get('price',0))
    c = float(i.get('cost',0))
    print("  {} {} | GHS {:.0f} - cost {:.0f} = GHS {:.0f} margin | stock:{}".format(
        i['name'], i.get('variant',''), p, c, p-c, i.get('stock',0)))
print()

# Best selling items for Jiji - high stock + mid price
print("Best Jiji listing candidates (high stock, good price point):")
jiji_candidates = sorted([i for i in in_stock if i.get('stock',0) >= 3 and float(i.get('price',0)) <= 300], 
                         key=lambda x: -x.get('stock',0))[:15]
for i in jiji_candidates:
    print("  GHS {:.0f} | {} {} | stock:{}".format(
        float(i.get('price',0)), i['name'], i.get('variant',''), i.get('stock',0)))