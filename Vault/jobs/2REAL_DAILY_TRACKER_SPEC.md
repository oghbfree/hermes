# 2REAL_DAILY_TRACKER — Google Sheets Structure
**Owner:** John | **Location:** Google Sheets (shared with H: edit access)  
**Template:** Duplicate this structure exactly — one sheet per week (Mon–Sun)

---

## 📋 SHEET TABS (In Order)

### TAB 1: ENQUIRY_LOG
**Purpose:** Every single enquiry, logged within 5 minutes

| Col | Header | Format | Validation | Notes |
|-----|--------|--------|------------|-------|
| A | Date/Time | `yyyy-mm-dd hh:mm` | Required | Auto: `=NOW()` then paste values |
| B | Channel | Dropdown | Call / WhatsApp / Jiji / Walk-in / Referral | |
| C | Customer Name | Text | Required | |
| D | Phone | Text (Ghana format) | Required | `024XXXXXXX` |
| E | Product / Enquiry | Text | Required | SKU if known |
| F | Urgency | Dropdown | Hot / Warm / Cold | Hot = buying today |
| G | Stock Status | Dropdown | In Stock / Low (1-2) / Out / Sourcing | From Zobaze |
| H | Quote Sent (Y/N) | Checkbox | | |
| I | Quote Time | `hh:mm` | | |
| J | Quote Amount (GHS) | Number | | |
| K | Outcome | Dropdown | Pending / Quoted / Ordered / Lost / Sourcing | Update real-time |
| L | Notes | Text | | "Called back 14:30" / "Wants discount" |

**Conditional Formatting:**
- Col K = "Lost" → Row red
- Col K = "Sourcing" → Row orange
- Col F = "Hot" + Col K ≠ "Ordered" → Row yellow (flag)

---

### TAB 2: ORDERS_LOG
**Purpose:** Confirmed orders, payment received, ready to dispatch

| Col | Header | Format | Validation |
|-----|--------|--------|------------|
| A | Order ID | `2R-YYYYMMDD-###` | Required, unique |
| B | Date | `yyyy-mm-dd` | Required |
| C | Enquiry Ref | Link to Tab 1 Row | `=HYPERLINK("#gid=0&range=A"&row(),"Ref")` |
| D | Customer | Text | |
| E | Phone | Text | |
| F | SKU | Text | Exact Zobaze SKU |
| G | Qty | Number | ≥1 |
| H | Unit Price (GHS) | Number | Zobaze price |
| I | Total (GHS) | Formula | `=G*H` |
| J | Payment Method | Dropdown | MoMo / Cash |
| K | Payment Ref | Text | MoMo TXN ID / "Cash" |
| L | Status | Dropdown | Confirmed / Packed / Dispatched / Delivered / Returned |
| M | Rider Name | Text | |
| N | Rider Phone | Text | |
| O | Rider Plate | Text | |
| P | Dispatch Time | `hh:mm` | |
| Q | Delivery Time | `hh:mm` | |
| R | Customer Confirmed | Checkbox | Call confirmed |
| S | Notes | Text | |

---

### TAB 3: SALES_LOG
**Purpose:** Every completed sale — reconciles to Zobaze daily

| Col | Header | Format | Validation |
|-----|--------|--------|------------|
| A | Date | `yyyy-mm-dd` | Required |
| B | Order ID | From Tab 2 | Required |
| C | Channel | Dropdown | Jiji / WhatsApp / Walk-in / Referral |
| D | Customer | Text | |
| E | SKU | Text | |
| F | Qty | Number | |
| G | Unit Price | Number | |
| H | Total | Formula | `=F*G` |
| I | Payment Method | Dropdown | MoMo / Cash |
| J | Payment Verified | Checkbox | You confirmed |
| K | Rider | Text | |
| L | Status | Dropdown | Completed / Refunded / Disputed |

**Row at bottom:** `TOTAL` row with `=SUM(H2:H)` — must match Zobaze daily total.

---

### TAB 4: DISPATCH_LOG
**Purpose:** Rider handover tracking

| Col | Header | Format |
|-----|--------|--------|
| A | Date | `yyyy-mm-dd` |
| B | Order ID | |
| C | Rider Name | |
| D | Rider Phone | |
| E | Plate | |
| F | Handover Time | `hh:mm` |
| G | Items | Text (SKU x Qty) |
| H | Photo Sent to Customer | Checkbox |
| I | Tracking Link | URL (Yango/Bolt) |
| J | Notes | |

---

### TAB 5: DELIVERIES_LOG
**Purpose:** Confirmation loop — NO delivery closed without customer call

| Col | Header | Format |
|-----|--------|--------|
| A | Date | `yyyy-mm-dd` |
| B | Order ID | |
| C | Delivery Time | `hh:mm` |
| D | Customer Called | Checkbox |
| E | Call Time | `hh:mm` |
| F | Customer Satisfied | Checkbox |
| G | Issue (Y/N) | Checkbox |
| H | Issue Details | Text |
| I | Resolution | Text |
| J | Final Status | Completed / Return / Problem |

---

### TAB 6: STOCK_GAPS
**Purpose:** Track every out-of-stock request & sourcing status

| Col | Header | Format |
|-----|--------|--------|
| A | Date | `yyyy-mm-dd` |
| B | Enquiry Ref | Link to Tab 1 |
| C | Customer | |
| D | SKU / Description | |
| E | Urgency | Hot / Warm |
| F | Status | Sourcing / Quoted / Ordered / Arrived / Cancelled |
| G | Quote 1 (UK eBay) | GHS + Link |
| H | Quote 2 (Direct) | GHS + Link |
| I | Quote 3 (Local) | GHS + Link |
| J | H Price Set | GHS |
| K | Customer Accepted | Checkbox |
| L | PO Placed | Date |
| M | ETA | Date |
| N | Arrived | Checkbox |
| O | Zobaze Updated | Checkbox |

---

### TAB 7: JIJI_STATS
**Purpose:** Daily Jiji dominance metrics (filled 16:00–17:00)

| Col | Header | Format |
|-----|--------|--------|
| A | Date | `yyyy-mm-dd` |
| B | Active Priority Listings | Number (target 20) |
| C | Total Views (24h) | Number |
| D | Total Chats (24h) | Number |
| E | Avg Response Time | Minutes |
| F | Chats < 5 min | Number |
| G | Leads to WhatsApp | Number |
| H | Sales from Jiji | Number |
| I | Revenue from Jiji | GHS |
| J | Price Adjustments | Count |
| K | Featured Tags Active | Count |
| L | Notes | Text |

---

### TAB 8: DAILY_SUMMARY
**Purpose:** One-row-per-day snapshot for H (sent 17:30)

| Col | Header | Formula / Source |
|-----|--------|------------------|
| A | Date | `=TODAY()` |
| B | Enquiries Total | `=COUNTA(ENQUIRY_LOG!A2:A)` |
| C | Enquiries Hot | `=COUNTIF(ENQUIRY_LOG!F:F,"Hot")` |
| D | Orders Confirmed | `=COUNTIF(ORDERS_LOG!L:L,"Confirmed")+COUNTIF(ORDERS_LOG!L:L,"Packed")+COUNTIF(ORDERS_LOG!L:L,"Dispatched")+COUNTIF(ORDERS_LOG!L:L,"Delivered")` |
| E | Sales Revenue | `=SUM(SALES_LOG!H:H)` |
| F | Dispatches | `=COUNTA(DISPATCH_LOG!A2:A)` |
| G | Deliveries Confirmed | `=COUNTIF(DELIVERIES_LOG!J:J,"Completed")` |
| H | Delivery Issues | `=COUNTIF(DELIVERIES_LOG!J:J,"Problem")` |
| I | Stock Gaps New | `=COUNTIF(STOCK_GAPS!F:F,"Sourcing")` |
| J | Stock Gaps Resolved | `=COUNTIF(STOCK_GAPS!F:F,"Arrived")` |
| K | Jiji Avg Response | `=AVERAGE(JIJI_STATS!E:E)` (today only) |
| L | Jiji Sales | `=JIJI_STATS!H` (today) |
| M | Zobaze Total | Manual entry (reconcile) |
| N | Tracker Total | `=E` (should match M) |
| O | Variance | `=M-N` (target 0) |
| P | Notes / Flags | Text |

---

## 🔧 SETUP INSTRUCTIONS (John — Do This Today)

1. **Create new Google Sheet** → Name: `2REAL_DAILY_TRACKER_Week-2026-07-13`
2. **Create 8 tabs** exactly as above (right-click tab → Rename)
3. **Paste headers** row 1 for each tab
4. **Set Data Validation** on dropdown columns (Data → Data validation)
5. **Share with H** → Edit access
6. **Bookmark** in browser toolbar
7. **Test:** Log one dummy enquiry → one dummy order → verify flow

---

## 📱 DAILY WORKFLOW IN SHEETS

| Time | Action |
|------|--------|
| 06:30 | Open sheet → Tab 1 ready |
| 06:35 | Log overnight enquiries |
| 07:00 | Tab 6 check — any urgent sourcing? |
| All day | Tab 1, 2, 4, 5 updated **real-time** |
| 16:00 | Tab 7 filled during Jiji block |
| 17:00 | Tab 8 auto-calcs → Verify M=N → Screenshot Tab 8 → WhatsApp H |
| 17:30 | Close sheet |

---

## 🛡️ DATA INTEGRITY RULES

1. **Never delete rows** — mark status, filter instead
2. **Order ID format:** `2R-20260714-001` (date + sequence)
3. **One weekly sheet** — archive Sunday night → new sheet Monday
4. **H has view of all weeks** — keep in same Drive folder: `2 Real / Daily Tracker /`
5. **Backup:** File → Download → Excel (.xlsx) every Friday 17:00

---

**File Location:** `Google Drive → 2 Real Enterprises → Daily Tracker →`  
**Spec Location:** `/c/Users/User/.hermes/workspace/Vault/jobs/2REAL_DAILY_TRACKER_SPEC.md`