import json

path = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\inventory_agent.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total items:", len(data))

low = []   # in_stock=True and 0 < stock <= 2
oos = []   # stock <= 0 or in_stock false
neg = []

for it in data:
    stock = it.get("stock", 0)
    in_stock = it.get("in_stock", False)
    name = f"{it.get('name','')} {it.get('variant','')}".strip()
    cat = it.get("category", "")
    price = it.get("price", 0)
    if stock <= 0 or not in_stock:
        oos.append((cat, name, stock, price))
        if stock < 0:
            neg.append((cat, name, stock, price))
    elif stock <= 2:
        low.append((cat, name, stock, price))

print("\n=== LOW STOCK (in_stock=true, 1-2 units) ===")
print("count:", len(low))
for c in sorted(low, key=lambda x: x[2]):
    print(f"  {c[2]}x  {c[1]}  (GHS {c[3]})  [{c[0]}]")

print("\n=== OUT OF STOCK (stock<=0 / in_stock=false) ===")
print("count:", len(oos), " negative:", len(neg))
for c in neg:
    print(f"  NEG {c[2]}x  {c[1]}  [{c[0]}]")

# Good-stock candidates for status (stock>=8, reasonable price)
good = [(c, n, s, p) for (c, n, s, p) in
        [(it.get('category',''), f"{it.get('name','')} {it.get('variant','')}".strip(), it.get('stock',0), it.get('price',0))
         for it in data if it.get('in_stock', False) and it.get('stock',0) >= 8]]
print("\n=== GOOD STOCK (>=8 units) candidate count:", len(good))
