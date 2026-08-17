import json
from pathlib import Path
from difflib import SequenceMatcher
items = json.load(open(r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\inventory_agent.json','r',encoding='utf-8'))
q='Weber bbq cover'
print('query:', q)
for it in items:
    name=it.get('variant') or it.get('name','')
    blob=f"{name} {it.get('category','')}"
    score=SequenceMatcher(None, q.lower(), blob.lower()).ratio()
    if score>0.3:
        print(score, '|', name, '|', it.get('price'), '|', it.get('stock'), '|', it.get('in_stock'))
