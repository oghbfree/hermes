# WhatsApp Message Cron Configuration
**Date:** 27/11/26  
**Purpose:** Setup static/dynamic WhatsApp check-in crons

---

## ✅ KYEI (STATIC — ready to deploy)

**Number:** 0503344556 (233503344556@s.whatsapp.net)  
**Schedule:** 4 PM daily (`0 16 * * *`)  
**Message:** "Who's around?" (STATIC — never changes)  
**Purpose:** Coverage check during H's days off (Sun/Mon) + Saturday shifts  
**Script:** `kyei_coverage_check.py` ✅ **Created**

---

## ⚠️ NEED FULL NUMBERS FOR:

### **1. Dad (Robert Herbert-Blankson)**
**Current:** +447****4695  
**Need:** Full 13-digit UK number  
**Schedule:** TBD (suggest 2x/week: Tue/Fri 10 AM UK time)  
**Type:** DYNAMIC (learns from past messages)  
**Age:** 91, wheelchair-bound, UK  
**Topics:** Health, mobility, wheelchair, stump, carer needs

### **2. Kwasi**
**Current:** +233****2932  
**Need:** Full 12-digit Ghana number  
**Schedule:** Thursdays 8:25 AM (biweekly per CONTACTS.md)  
**Type:** DYNAMIC (learns from past messages)  
**Role:** Apiary/Hive Manager (currently inactive due to funding)  
**Topics:** Wellbeing, hive status, funding status

### **3. Kanzoni**
**Number:** 233248957794 ✅ **Found**  
**Schedule:** Tuesdays 7 AM (weekly check-in per business_interactions.md)  
**Type:** DYNAMIC (learns from past messages)  
**Role:** Farm contact, apiary transport  
**Topics:** Wellbeing, farm visit, bee status

---

## CRON STRUCTURE (Dynamic Learning Pattern)

**Based on Mum's cron (#924):**
```json
{
  "name": "<Person> — <purpose> (dynamic)",
  "prompt": "<Dynamic prompt with context reading>",
  "context_from": ["self"],  // KEY: Enables learning from past runs
  "schedule": {"kind": "cron", "expr": "<cron expr>"},
  "script": null,
  "no_agent": false,
  "deliver": "telegram:-1003784520976:1",
  "enabled_toolsets": ["terminal", "file"]
}
```

**Features:**
- ✅ `context_from: ["self"]` — learns from previous messages/responses
- ✅ Random offset (0-12 min) — varies message timing
- ✅ Reads state files (health logs, profiles, etc.)
- ✅ Uses wa_send.py script to deliver
- ✅ Never repeats wording from previous runs
- ✅ Adapts based on responses received

---

## NEXT STEPS

1. **Get full numbers from H:**
   - Dad: +447****4695 → Need full UK number
   - Kwasi: +233****2932 → Need full Ghana number

2. **Create dynamic scripts:**
   - `dad_checkin.py` (learns from past)
   - `kwasi_checkin.py` (learns from past)
   - `kanzoni_checkin.py` (learns from past)

3. **Deploy crons:**
   ```bash
   # Kyei (STATIC - ready now)
   hermes cron create "0 16 * * *" --name "Kyei — coverage check (static)" --script kyei_coverage_check.py --no-agent --deliver local
   
   # Dad (DYNAMIC - need number)
   hermes cron create "0 10 * * 2,5" --name "Dad — health check-in (dynamic)" --prompt "<prompt>" --continuity --skill <skill> --deliver telegram:-1003784520976:1
   
   # Kwasi (DYNAMIC - need number)
   hermes cron create "25 8 * * 4/2" --name "Kwasi — apiary check (dynamic biweekly Thu)" --prompt "<prompt>" --continuity --deliver telegram:-1003784520976:1
   
   # Kanzoni (DYNAMIC - ready)
   hermes cron create "0 7 * * 2" --name "Kanzoni — weekly farm check (dynamic Tue)" --prompt "<prompt>" --continuity --deliver telegram:-1003784520976:1
   ```

---

## ⚠️ CONFIRM BEFORE PROCEEDING

**Question for H:**
> I need the full WhatsApp numbers to create the dynamic check-in crons:
> 
> 1. **Dad's UK number:** Currently shows +447****4695 — what's the full number?
> 2. **Kwasi's number:** Currently shows +233****2932 — what's the full number?
> 
> Also confirm schedules:
> - Dad: 2x/week Tue/Fri 10 AM UK time?
> - Kwasi: Biweekly Thursdays 8:25 AM?
> - Kanzoni: Weekly Tuesdays 7 AM?
