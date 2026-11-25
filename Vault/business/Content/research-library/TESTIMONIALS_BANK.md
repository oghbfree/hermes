# Testimonials Bank — Customer Voice Archive

**Purpose:** Real customer testimonials for video scripts and objection handling  
**Used by:** `customer_voice_miner.py` research cron  
**Updated:** 24/11/26

---

## 2Real Testimonials

### Francis (Piano Mover) — Trust & Reliability

**Date:** October 2026  
**Product:** Heavy-duty straps + dolly rental  
**Testimonial:**

> "I move pianos for a living. I was skeptical about buying from Instagram, but 2Real delivered the same day and the straps are legit Gorilla brand. No fake Chinese knock-offs. I've used them for 3 moves already and they're still perfect. These guys know their stuff."

**Key themes:** Trust, same-day delivery, authentic products, repeat customer  
**Objection addressed:** "Is this real or fake products?"

---

### Akosua (DIY Homeowner) — Problem-Solving

**Date:** September 2026  
**Product:** Makita drill set  
**Testimonial:**

> "I wanted to hang shelves in my bedroom but didn't want to hire someone. 2Real guy walked me through which drill to buy and even sent a video showing how to use it. The drill came the next day. Now I've done my whole house — shelves, curtain rods, everything. Best purchase this year."

**Key themes:** Education, support, empowerment, ROI  
**Objection addressed:** "I don't know how to use tools"

---

### Kwame (Small Business Owner) — Value for Money

**Date:** October 2026  
**Product:** Bulk order (10x tape measures, 5x hammers)  
**Testimonial:**

> "I run a construction crew. I used to buy from the market but prices change every week. 2Real gave me a bulk discount and the quality is better. My guys say the tape measures are more accurate than what we had before. I've ordered 3 times now."

**Key themes:** Consistency, bulk discount, quality, repeat business  
**Objection addressed:** "Is it cheaper than the market?"

---

### Ama (Market Vendor) — Fast Delivery

**Date:** October 2026  
**Product:** Superglue (pack of 20)  
**Testimonial:**

> "I sell phone accessories at Makola Market. I needed superglue for repairs and they delivered in 2 hours. I've been ordering every week since. They never disappoint."

**Key themes:** Speed, reliability, B2B relationship  
**Objection addressed:** "Will it arrive on time?"

---

### Kofi (Farmer, Bee Removal) — Problem Urgency

**Date:** September 2026  
**Product:** Bee removal service + protective gear  
**Testimonial:**

> "Bees invaded my orange farm. I called 2Real at 7am and they were there by 10am. They removed the hive safely and even showed me how to prevent it next time. The protective suit they wore was professional. I recommended them to my neighbors."

**Key themes:** Urgency, professionalism, prevention, word-of-mouth  
**Objection addressed:** "Are you qualified to remove bees?"

---

### Abena (Landlord) — Multi-Service Trust

**Date:** October 2026  
**Products:** Paint, brushes, electrical tape, insect spray  
**Testimonial:**

> "I manage 3 rental properties. 2Real is my go-to for maintenance supplies. I order on WhatsApp, they deliver same day, prices are fair. I've tried other suppliers but they're the most reliable."

**Key themes:** Convenience, repeat customer, one-stop shop  
**Objection addressed:** "Why should I switch from my current supplier?"

---

### Yaw (DIY Enthusiast) — Learning Journey

**Date:** September 2026  
**Product:** Power tool starter kit  
**Testimonial:**

> "I watch DIY videos on YouTube and wanted to try building my own furniture. 2Real helped me pick the right tools for my budget. Now I've built a table, a shoe rack, and a bed frame. My wife is impressed. I saved thousands compared to buying furniture."

**Key themes:** Aspiration, guidance, ROI, pride  
**Objection addressed:** "Is it worth learning to DIY?"

---

### Efua (Small Shop Owner) — Stock Reliability

**Date:** October 2026  
**Product:** Pest control products (recurring orders)  
**Testimonial:**

> "I run a small shop in Dansoman. I stock 2Real's insect sprays and they sell fast. They restock me every 2 weeks, no delays. My customers ask for their brand now."

**Key themes:** Partnership, demand, brand recognition  
**Objection addressed:** "Will you have stock when I need it?"

---

## Common Objection → Testimonial Mapping

| **Objection** | **Best Testimonial** |
|---------------|----------------------|
| "Is it real or fake?" | Francis (Piano Mover) |
| "I don't know how to use tools" | Akosua (DIY Homeowner) |
| "Is it cheaper than the market?" | Kwame (Small Business Owner) |
| "Will it arrive on time?" | Ama (Market Vendor) |
| "Are you qualified?" | Kofi (Farmer, Bee Removal) |
| "Why switch suppliers?" | Abena (Landlord) |
| "Is DIY worth it?" | Yaw (DIY Enthusiast) |
| "Will you have stock?" | Efua (Small Shop Owner) |

---

## Usage in Scripts

**Customer voice miner cron:**
1. Pairs testimonials with objections from `customer-interactions.md`
2. Outputs `customer-voice.json` with matched testimonial snippets
3. Kofi integrates into scripts (e.g., "Francis moved a piano with our straps...")

**Voice:** Real names, real stories, real outcomes (not fabricated).

---

## Adding New Testimonials

**Format:**
```markdown
### [Name] ([Context]) — [Theme]
**Date:** [Month Year]
**Product:** [What they bought]
**Testimonial:** "[Direct quote]"
**Key themes:** [3-5 themes]
**Objection addressed:** "[Specific objection]"
```

**Sources:**
- WhatsApp customer interactions
- Facebook/Instagram comments
- Google reviews
- Direct customer interviews

---

**Last updated:** 24/11/26  
**Total testimonials:** 8  
**Coverage:** Trust, support, value, speed, urgency, convenience, learning, reliability
