---
title: DEPRECATED — This directory is no longer active
status: deprecated
deprecated_date: 2026-08-12
migrated_to: Vault/business/farm/
reason: Data consolidated into primary farm operations directory
---

# ⛔ DEPRECATED — Farm Data Location

**This directory (`Vault/business/2real/Farming/farm/`) is no longer the active location for farm data.**

All data has been migrated to: **`Vault/business/farm/`**

## Migration Map

| Old Location (this dir) | New Location | Action |
|------------------------|-------------|--------|
| `crops.md` (53 crops) | → `Vault/business/farm/crops/crop-registry.md` | ✅ Migrated |
| `seedings.md` | → `Vault/business/farm/crops/seedings-log.md` | ✅ Migrated |
| `equipment.md` (53 items) | → `Vault/business/farm/equipment/equipment-register.md` | ✅ Migrated |
| `animals.md` (10+ animals) | → `Vault/business/farm/livestock/goats.md` | ✅ Appended |
| `plots.md` (14 plots) | → `Vault/business/farm/land/plots.md` | ✅ Migrated |
| `observations.md` (53 entries) | → `Vault/business/farm/observations/observation-log.md` | ✅ Migrated |
| `expenses.md` | → `Vault/business/farm/finance/expenses-2026.md` | ✅ Migrated |
| `purchases.md` (21 entries) | → `Vault/business/farm/finance/purchases-2026.md` | ✅ Migrated |
| `harvests.md` (10 entries) | → `Vault/business/farm/finance/harvests-2026.md` | ✅ Migrated |
| `sales.md` (2 entries) | → `Vault/business/farm/finance/sales-2026.md` | ✅ Migrated |
| `inputs.md` (8 entries) | → `Vault/business/farm/inputs/inputs-log.md` | ✅ Migrated |
| `activities.md` (50 entries) | → `Vault/business/farm/updates/activities-log.md` | ✅ Migrated |
| `maintenance.md` (7 entries) | → `Vault/business/farm/infrastructure/maintenance-log.md` | ✅ Migrated |
| `structures.md` (2 structures) | → `Vault/business/farm/infrastructure/structures.md` | ✅ Migrated |
| `2026-06-log.md` | → `Vault/business/farm/daily/` series | ✅ Notes absorbed into memory |
| `fetch_farmos.py` / `convert_farmos.py` | Kept here (utilities) | 🟡 Preserved as-is |
| `farmos_export*.json` | Kept here (raw export) | 🟡 Preserved as-is |

---

## Why?

The farm data was split across two locations:
1. **Primary:** `Vault/business/farm/` — workflow, operations, cron jobs, daily logs
2. **Secondary (this dir):** `Vault/business/2real/Farming/farm/` — detailed asset-level records from farmOS export

These contained the **same farm** (Senya Beraku, 7 acres) with **no overlap in data type** — one was workflow/operations, the other was asset registry. They've been merged.

---

*To delete this directory entirely when ready, run: `rm -rf "/c/Users/User/.hermes/workspace/Vault/business/2real/Farming/farm/"` (but keep it a while in case you need the farmOS UUIDs)*