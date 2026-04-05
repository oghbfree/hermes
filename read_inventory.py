import openpyxl
import sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('C:/OpenClaw/.openclaw/workspace/raw-data/inventory170326.xlsx')
ws = wb.active

products_2plus = []
for row in ws.iter_rows(min_row=2, values_only=True):
    cat, item_type, item_name, variant, price, cost, stock = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
    if stock and int(stock) >= 2:
        name = str(item_name or '') + ' ' + str(variant or '')
        name = name.strip()
        products_2plus.append({'name': name, 'price': price, 'stock': int(stock), 'category': cat})

products_2plus.sort(key=lambda x: x['stock'], reverse=True)

for p in products_2plus:
    n = p['name']
    pr = p['price']
    s = p['stock']
    c = p['category']
    print(f"{n} | GHS {pr} | Stock: {s} | {c}")

print(f"\n--- TOTAL PRODUCTS WITH 2+ STOCK: {len(products_2plus)} ---")
