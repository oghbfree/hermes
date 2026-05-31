# eBay Active Listings CSV Format

eBay Seller Hub → Reports → Download → "All active listings" report.

## Key Columns (30 total)

| Column | Use |
|---|---|
| Item number | eBay Item ID — unique per listing |
| Title | Item name shown on eBay |
| Available quantity | Stock count |
| Current price | Selling price (GBP) |
| Format | FIXED_PRICE or AUCTION |
| Start date | When listing went live |
| End date | When listing expires |
| Condition | New / Used / Pre-owned |
| Custom label (SKU) | Seller's own reference — often empty |
| eBay category 1/2 name | Category hierarchy |
| P:UPC / P:EAN / P:ISBN | Product identifiers |

## Notes

- Item IDs starting with `3872...` = current era listings
- Item IDs starting with `2724...` = old era (in EBAY S.xlsx, mostly inactive)
- Item IDs starting with `8000...` = newest listings
- Zero overlap between eras — always use latest CSV as source of truth
- Encoding: UTF-8 with BOM (`utf-8-sig` in Python)
