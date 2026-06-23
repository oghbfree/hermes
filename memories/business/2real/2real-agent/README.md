# 2 Real Enterprises — AI Agent System
# Customer Inquiry Processing & UK Sourcing Automation

## Inventory Summary
- **Total Items:** 1,049
- **In Stock:** 665 items
- **Out of Stock:** 384 items  
- **Total Stock Value:** ₵493,599
- **Price Range:** ₵8 - ₵3,000
- **Categories:** Online (988), Ingco Gh (43), Ingco Import (14), Wynca (4)

## Business Rules (from SOP)

### Roles
- **H** — You. All discounts, off-zobaze pricing, final say.
- **John** — Oyarifa sales, all adverts (Jiji/WhatsApp/Facebook), UK sourcing.
- **Madam** — Oyarifa sales when working.
- **Sammy** — Kantamanto walk-in only, on-zobaze items only.

### Customer Inquiry Flow
1. Customer contacts via Jiji / WhatsApp / Facebook / Phone / Walk-in
2. Check if item is in stock (inventory_agent.json)
3. If IN STOCK → quote zobaze price, no discount without H approval
4. If OUT OF STOCK → notify John for sourcing (UK/Ghana), 24h SLA
5. If OFF-ZOBAZE → notify H with photo, H sets price
6. If DISCOUNT REQUESTED → auto-route to H
7. Payment: MoMo or cash ONLY, no credit
8. Staff enters sale into zobaze

### WhatsApp Group Format Templates

#### New In-Stock Inquiry
```
📩 NEW INQUIRY
Item: {item_name}
Price: ₵{price} (zobaze)
Stock: {stock} available
Source: {channel}
Action: Quote customer at ₵{price}
```

#### Out-of-Stock Sourcing Request
```
🔍 SOURCING NEEDED
Item: {item_name}
Customer: {customer_info}
Source: {channel}
John — need 3 comparables within 24h:
  1. UK eBay
  2. Direct manufacturer
  3. Competitive 3rd party
Post screenshots + links + GHS prices in group.
H will set final margin.
```

#### Off-Zobaze Pricing Request
```
💰 OFF-ZOBAZE PRICING
Item: {item_name}
Requested by: {staff}
Photo: {attached}
H — please set price (cost + shipping + UK shipping + margin).
```

#### Discount Request
```
🏷️ DISCOUNT REQUEST
Item: {item_name}
Zobase Price: ₵{price}
Customer offering: ₵{offer}
Requested by: {staff}
H — approve or deny?
```

#### Low Stock Alert
```
⚠️ LOW STOCK
Item: {item_name}
Stock remaining: {stock}
John — pause adverts for this item?
```

### UK Sourcing — What Agent Does Automatically
1. Search eBay UK completed listings
2. Search Amazon UK
3. Search other configured sources
4. Convert GBP → GHS (rate: to be confirmed)
5. Estimate shipping Ghana (to be confirmed)
6. Compile 3 options → post to group
7. H just reviews and sets margin

### Customer Conversion Tracking
- Every inquiry logged with: date, channel, item, customer, outcome
- Follow-up reminders for pending inquiries
- WhatsApp Status content suggestions (3-5 featured items daily)

### Stock Locations (Current)
- **Oyarifa** — Madam manages (needs to start reporting to H)
- **Kantamanto** — Sammy manages, enters into zobaze

### Stock Locations (Future — Consolidated)
- **Kantamanto only** — single location

## Files
- `inventory_agent.json` — Full inventory database
- `sop_sales.md` — Sales SOP
- `sop_inventory.md` — Inventory SOP
- `customer_leads.json` — Customer inquiry tracker (to be created)
- `sourcing_log.json` — UK sourcing history (to be created)
