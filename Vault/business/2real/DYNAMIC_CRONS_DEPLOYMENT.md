# DYNAMIC WHATSAPP CHECK-IN CRONS — DEPLOYMENT PLAN
**Date:** 27/11/26  
**Status:** Ready to deploy  

---

## ✅ CONFIRMED NUMBERS & SCHEDULES

### **1. Dad (Robert Herbert-Blankson)**
**Number:** +44 7983 254695 (447983254695@s.whatsapp.net)  
**Schedule:** Existing schedule confirmed (no changes)  
**Type:** DYNAMIC (learns from past conversations)  
**Age:** 91, wheelchair-bound, UK  
**Topics:** Health, mobility, wheelchair, stump, carer needs  
**Existing cron:** CHECK IF EXISTS

---

### **2. Kwasi (Apiary/Hive Manager)**
**Number:** +233 24 758 2932 (233247582932@s.whatsapp.net)  
**Schedule:** Existing schedule confirmed (biweekly Thursdays 8:25 AM)  
**Type:** DYNAMIC (learns from past conversations)  
**Role:** Apiary/Hive Manager (currently inactive due to funding)  
**Topics:** Wellbeing, hive status, funding status  
**Existing cron:** CHECK IF EXISTS

---

### **3. Kanzoni (Farm Contact)**
**Number:** +233 24 895 7794 (233248957794@s.whatsapp.net)  
**Schedule:** Existing schedule confirmed (weekly Tuesdays 7 AM)  
**Type:** DYNAMIC (learns from past conversations)  
**Role:** Farm contact, apiary transport  
**Topics:** Wellbeing, farm visit, bee status  
**Existing cron:** CHECK IF EXISTS

---

### **4. Godfred Odoom** ⭐ NEW
**Number:** +233 24 048 4465 (233240484465@s.whatsapp.net)  
**Schedule:** Weekly Mondays 8:00 AM (per logs)  
**Type:** DYNAMIC (learns from past conversations)  
**Role:** Site contact — New Amanful (Takoradi)  
**Topics:** Site status, weeding/spraying, weed burning, coconut trees, encroachment, needs/observations  
**Existing cron:** May exist (check logs show "Godfred/Amanful site Mon")  
**Related:** Neighbour with clearing crew (mother: 0540267026)

---

### **5. Matthias** ⭐ NEW
**Number:** +233 54 489 8392 (233544898392@s.whatsapp.net)  
**Schedule:** Weekly Fridays 8:00 PM (20:00 UTC per logs)  
**Type:** DYNAMIC (learns from past conversations)  
**Role:** Site Supervisor/Mason — New Amanful + Borkro ONLY (NOT Senya farm)  
**Topics:** Ground operations, New Amanful plans, site visits, wall build status, encroachment monitoring (geolocation photos/videos)  
**Existing cron:** May exist (check logs show "project-logistics-checkin-matthias")  
**Note:** Lives in Agona, trusted 6+ years, has car problems affecting travel

---

## 📋 DEPLOYMENT STEPS

### **STEP 1: Check Existing Crons**
Search jobs.json for existing crons:
- Dad check-in
- Kwasi check-in
- Kanzoni check-in
- Godfred/Amanful site
- Matthias logistics

### **STEP 2: Create Missing Crons**
For any that don't exist, create with:
- `context_from: ["self"]` — learns from past runs
- Random offset (0-12 min)
- Reads vault state files
- Uses wa_send.py
- Never repeats wording
- Telegram delivery for confirmation

### **STEP 3: Update Existing Crons**
For any that exist but aren't dynamic:
- Add `context_from: ["self"]`
- Ensure they read state files
- Ensure random offset
- Confirm proper phone numbers

---

## 🔄 UNCLE PETER & BEN FEEDBACK ROUTING

**Uncle Peter:** +233 24 809 7935  
**Ben:** +233 24 412 0093

**Their replies go to H's WhatsApp → Hermes processes automatically**

**Setup needed:**
- [ ] Confirm WhatsApp gateway monitors H's number
- [ ] Tag Peter/Ben messages as "goat project" context
- [ ] Auto-update GOAT_FARMING_RESTART.md when quotes/photos arrive
- [ ] Notify H via Telegram when new quote received

---

## 📞 FULL CONTACT ROSTER (Dynamic Crons)

| Contact | Number | Schedule | Role | Topics | Status |
|---------|--------|----------|------|--------|--------|
| **Mum (Stephanie)** | 233548236698 | 2x/day 9AM+5PM | Carer check-in | Health, BP, meals, mobility | ✅ LIVE (cron #924) |
| **Dad** | 447983254695 | Existing | Health check | Wheelchair, stump, carers | ⏳ Check |
| **Kwasi** | 233247582932 | Thu 8:25 AM biweekly | Apiary | Wellbeing, hives, funding | ⏳ Check |
| **Kanzoni** | 233248957794 | Tue 7 AM weekly | Farm contact | Wellbeing, farm, bees | ⏳ Check |
| **Godfred Odoom** | 233240484465 | Mon 8 AM weekly | Amanful site | Site status, weeding, encroachment | ⏳ Check |
| **Matthias** | 233544898392 | Fri 8 PM weekly | Site supervisor | Ground ops, Amanful, Borkro | ⏳ Check |
| **Kyei** | 233503344556 | 4 PM daily | Staff coverage | "Who's around?" | ✅ LIVE (cron bfc4a2cf907a) |

---

## ✅ DEPLOYMENT COMPLETE

**Date:** 27/11/26  
**Status:** ALL DYNAMIC CRONS DEPLOYED

### **Deployed Crons:**

| Contact | Number | Schedule | Cron ID | Status |
|---------|--------|----------|---------|--------|
| **Dad** | 447983254695 | Tue/Fri 10 AM | a0f6dee3f0ab | ✅ LIVE |
| **Kwasi** | 233247582932 | Thu 8:25 AM biweekly | c277d4bb3383 | ✅ LIVE |
| **Kanzoni** | 233248957794 | Tue 7 AM weekly | 502f0f3b77a6 | ✅ LIVE |
| **Godfred Odoom** | 233240484465 | Mon 8 AM weekly | d39d75e5bec1 | ✅ LIVE |
| **Matthias** | 233544898392 | Fri 8 PM weekly | 94fd232fc7fe | ✅ LIVE |

**All crons have:**
- ✅ `continuity: on` — learns from previous runs
- ✅ Random offset (0-12 min) built into prompt
- ✅ Reads vault state files
- ✅ Uses wa_send.py for delivery
- ✅ Never repeats wording
- ✅ Telegram confirmation delivery
- ✅ H's greeting rule enforced (NEVER time-of-day greetings)

---

**Last Updated:** 27/11/26  
**Ready to deploy:** Awaiting confirmation of existing crons
