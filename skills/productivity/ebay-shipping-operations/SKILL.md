---
name: ebay-shipping-operations
description: End-to-end eBay shipping workflow — inventory packing, barcode labeling, spreadsheet tracking, QR code label dispatch via Post Office. Use when H asks about packing eBay orders, printing shipping labels, tracking dispatched items, or managing the eBay inventory-to-dispatch pipeline.
---

# eBay Shipping Operations

## Overview

H sells on eBay from the UK (SE14 area). Workflow: pack items → apply barcode labels → track in spreadsheet → download eBay QR code → dispatch at Post Office.

## Key Files

- **Inventory master**: `EBAY S.xlsx` — old stock (barcodes `103859845xxx`, 497 items, mostly inactive)
- **Active listings export**: eBay Seller Hub → Reports → Active listings (CSV format)
- **Barcode label sheets**: 40 labels per sheet (10×4 grid), format `10-3859-8456-XX`, say "shed" above barcode

## Important Data Facts

- EBAY S.xlsx Item IDs (`2724...`) and current active listing IDs (`3872...`, `8000...`) have **zero overlap** — they are different eras of listings
- Always use the **latest eBay active listings CSV** as the source of truth for what's currently for sale
- Barcode label numbers are **independent** from eBay Item IDs — labels are sequentially assigned during packing

## Packing Workflow (for helper/worker)

1. Print barcode label sheets (40 per sheet; 5 sheets = 200 labels)
2. Open the packing spreadsheet (see template below)
3. For each item:
   - Pack item in bag/box
   - Apply next sequential barcode label to outside
   - Write barcode number on package with pen (backup)
   - Update spreadsheet: Status → "Packed", add packed date
   - Stack package in numerical order on shelf
4. When item sells:
   - Find item in spreadsheet → note barcode label number
   - Pull matching package from shelf
   - eBay Seller Hub → Orders → Shipping Labels → download QR code
   - Take package + QR code to Post Office

## Post Office Details

- **New Cross**: 500 New Cross Road, SE14 6TL
- **New Cross Gate**: 165-167 New Cross Road, SE14 5DG (open till 8pm weekdays)
- eBay QR code labels: scan at counter → Post Office prints shipping label → no home printer needed

## Spreadsheet Columns

Create a packing spreadsheet with:

| Column | Purpose |
|---|---|
| Package # | Sequential (001, 002...) — matches barcode label |
| Barcode Label | e.g. `10-3859-8456-62` |
| Item Number | eBay Item ID |
| Title | Item title from eBay export |
| Status | Available / Packed / Sold / Dispatched |
| Packed Date | Date packed |
| Buyer Name | Filled when sold |
| Dispatch Date | Date taken to Post Office |
| Tracking No | From eBay label |
| Notes | |

## Generating the Packing Sheet

When H sends a new eBay active listings CSV:

1. Read CSV — key columns: `Item number`, `Title`, `Available quantity`, `Current price`
2. Assign sequential package numbers (001, 002...) to each row
3. Assign sequential barcode label numbers matching the printed label sheets
4. Create the packing spreadsheet with columns above
5. Save as new Excel file and send to H

## Pitfalls

- Don't assume EBAY S.xlsx is current — always check against latest eBay export
- Barcode label numbers and eBay Item IDs are NOT the same — never mix them up
- If items > labels printed, print more sheets before starting
- Always write the number on the package as backup — labels can fall off
- Keep packages in numerical order on shelf — critical for fast dispatch
