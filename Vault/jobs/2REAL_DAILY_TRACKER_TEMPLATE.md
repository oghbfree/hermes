# 2REAL_DAILY_TRACKER — Google Sheets Template
**Copy this structure to a new Google Sheet named `2REAL_DAILY_TRACKER`**  
Share with H (view access) and John (edit access)  
**Tabs:** Enquiry Log | Orders Log | Sales Log | Dispatch Log | Deliveries Log | Stock Availability | Sourcing Log | Jiji Stats | Write-Off Log | Daily Summary

---

## TAB 1: Enquiry Log
| Date/Time | Channel | Customer Name | Phone | Product/Enquiry | Urgency | Status | Quote Sent? | Quote Price | Notes |
|-----------|---------|---------------|-------|-----------------|---------|--------|-------------|-------------|-------|
| 14/07/26 06:42 | Jiji | Kwame A. | 024XXXXXXX | Makita Drill 18V | Hot | Quoted | Yes | GHS 1,250 | Replied in 3 min |
| 14/07/26 07:15 | WhatsApp | Ama K. | 020XXXXXXX | Bosch Grinder | Warm | Checking stock | No | — | Checking Zobaze now |

**Columns:**
- Date/Time: `DD/MM/YY HH:MM` (24hr)
- Channel: `Call` / `WhatsApp` / `Jiji` / `Walk-in` / `Referral`
- Urgency: `Hot` (ready to buy) / `Warm` (comparing) / `Cold` (enquiry only)
- Status: `New` / `Checking Stock` / `Quoted` / `Sourcing` / `Converted` / `Lost` / `Follow-up`
- Quote Sent?: `Yes` / `No`
- Quote Price: `GHS X,XXX` (from Zobaze or sourced)

---

## TAB 2: Orders Log
| Order ID | Date | Customer | Phone | SKU | Qty | Unit Price | Total | Payment Ref | Payment Method | Status | Rider | Dispatch Time | Notes |
|----------|------|----------|-------|-----|-----|------------|-------|-------------|----------------|--------|-------|---------------|-------|
| ORD-20260714-001 | 14/07/26 | Kwame A. | 024XXXXXXX | MAK-DRL-18V | 1 | 1,250 | 1,250 | MTN-240714-001 | MoMo | Dispatched | Yaw K. | 14/07 10:15 | Delivered 11:30 |

**Columns:**
- Order ID: `ORD-YYYYMMDD-###` (sequential daily)
- Status: `Confirmed` / `Packed` / `Dispatched` / `Delivered` / `Completed` / `Returned` / `Cancelled`
- Payment Method: `MoMo` / `Cash` / `Bank Transfer`
- Rider: Rider name + phone

---

## TAB 3: Sales Log (Daily Reconciliation)
| Date | Order ID | Channel | Customer | SKU | Qty | Unit Price | Total | Payment Method | Rider | Status |
|------|----------|---------|----------|-----|-----|------------|-------|----------------|-------|--------|
| 14/07/26 | ORD-20260714-001 | Jiji | Kwame A. | MAK-DRL-18V | 1 | 1,250 | 1,250 | MoMo | Yaw K. | Completed |

**End-of-Day Reconciliation (17:00):**
- Zobaze Total Sales (GHS): ___
- Tracker Total Sales (GHS): ___
- Variance: ___ (must be 0)
- Notes on any variance: ___

---

## TAB 4: Dispatch Log
| Order ID | Date | Time Dispatched | Rider Name | Rider Phone | Rider Plate | Tracking Link | Items Dispatched | Packed By | Photo Sent? |
|----------|------|-----------------|------------|-------------|-------------|---------------|------------------|-----------|-------------|
| ORD-20260714-001 | 14/07/26 | 10:15 | Yaw K. | 024XXXXXXX | GT-XXXX-24 | [Yango link] | MAK-DRL-18V x1 | John | Yes |

---

## TAB 5: Deliveries Log
| Order ID | Date Delivered | Time Delivered | Rider | Customer Confirmed? | Confirmation Time | Issue? | Issue Details | Status |
|----------|----------------|----------------|-------|---------------------|-------------------|--------|---------------|--------|
| ORD-20260714-001 | 14/07/26 | 11:30 | Yaw K. | Yes | 11:35 | No | — | Completed |

**Rule:** Call customer within 30 min of drop-off. Log confirmation time.

---

## TAB 6: Stock Availability (Top 50 SKUs — Updated Daily 07:00)
| SKU | Product Name | Category | Zobaze Qty | Physical Count | Variance | Min Stock | Reorder? | Location (Shelf) | Last Updated |
|-----|--------------|----------|------------|----------------|----------|-----------|----------|------------------|--------------|
| MAK-DRL-18V | Makita 18V Drill | Power Tools | 3 | 3 | 0 | 2 | No | A-1-Top | 14/07 07:05 |
| BOS-GRD-900 | Bosch 900W Grinder | Power Tools | 0 | 0 | 0 | 1 | **YES** | — | 14/07 07:05 |

**Conditional formatting:** Red if Variance ≠ 0, Red if Reorder? = YES

---

## TAB 7: Sourcing Log (Out-of-Stock Requests)
| Date | Customer | Phone | SKU/Description | Urgency | Quote 1 (Source/Price) | Quote 2 (Source/Price) | Quote 3 (Source/Price) | H Decision | Final Price | Status |
|------|----------|-------|-----------------|---------|------------------------|------------------------|------------------------|------------|-------------|--------|
| 14/07/26 | Kwame A. | 024XXXXXXX | DeWalt 20V Impact | High | UK eBay / GHS 1,850 | Direct / GHS 1,650 | Jiji Comp / GHS 2,100 | Pending | — | Sourcing |

**SLA:** 3 quotes in WhatsApp group within 24h of logging.

---

## TAB 8: Jiji Stats (Daily 16:00–17:00 Block)
| Date | Priority Listings Active | Total Views | Total Chats | Avg Response Time (min) | Leads Generated | Converted to Sale | Price Adjustments | Expired Listings Relisted |
|------|--------------------------|-------------|-------------|--------------------------|-----------------|-------------------|-------------------|---------------------------|
| 14/07/26 | 20/20 | 1,240 | 47 | 3.2 | 12 | 3 | 2 (MAK-DRL-18V -2%) | 0 |

---

## TAB 9: Write-Off Log
| Date | SKU | Product | Qty | Reason | Value (GHS) | Photo? | Approved By | Disposed? |
|------|-----|---------|-----|--------|-------------|--------|-------------|-----------|
| 14/07/26 | BOS-GRD-900 | Bosch Grinder | 1 | Damaged in transit | 450 | Yes | H | Yes |

---

## TAB 10: Daily Summary (Auto-filled via formulas or manual at 17:00)
| Metric | Today | This Week | Target | Variance |
|--------|-------|-----------|--------|----------|
| Enquiries Logged | ___ | ___ | — | — |
| Enquiries → Quotes | ___ | ___ | 80% | ___ |
| Conversion Rate | ___% | ___% | 25% | ___ |
| Orders Processed | ___ | ___ | — | — |
| Revenue (GHS) | ___ | ___ | — | — |
| Dispatched | ___ | ___ | — | — |
| Delivered & Confirmed | ___ | ___ | 100% | ___ |
| Avg Dispatch→Delivery (hrs) | ___ | ___ | <4 | ___ |
| Jiji Avg Response (min) | ___ | ___ | <5 | ___ |
| Stock Variance (Top 50) | ___% | ___% | <2% | ___ |
| Sourcing Requests | ___ | ___ | — | — |
| Sourcing Completed (24h) | ___% | ___% | 100% | ___ |

**Notes / Issues / Escalations:**  
___  
___  

**Sent to H (WhatsApp) at:** ___

---

## FORMULAS / AUTOMATION HINTS
- **Order ID:** `="ORD-"&TEXT(TODAY(),"YYYYMMDD")&"-"&TEXT(ROW()-1,"000")`
- **Daily Revenue:** `=SUMIFS(Sales_Log!H:H, Sales_Log!A:A, TODAY())`
- **Conversion Rate:** `=COUNTIF(Enquiry_Log!F:F,"Converted")/COUNTA(Enquiry_Log!A2:A)`
- **Stock Variance %:** `=ABS(SUM(Stock!D:D)-SUM(Stock!E:E))/SUM(Stock!D:D)`
- **Jiji Response Avg:** `=AVERAGE(Jiji_Stats!E:E)`

---

## SHARING & PERMISSIONS
| User | Access |
|------|--------|
| H (Owner) | View + Comment |
| John | Edit |
| (Optional) Accountant | View (Sales Log only) |

---

## TEMPLATE LOCATION
`/c/Users/User/.hermes/workspace/Vault/jobs/2REAL_DAILY_TRACKER_TEMPLATE.md`  
**Action:** John creates Google Sheet from this template Day 1, shares with H, bookmarks in browser.