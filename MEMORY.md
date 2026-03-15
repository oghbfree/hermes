# MEMORY.md - Long-Term Memory

TEST_PHRASE_FOR_SEARCH: openclaw_test_unique_20260313_1142

## System Setup (2026-03-13)
- OpenClaw installed and running on Windows
- WhatsApp gateway connected (+233204252252, +233233352252, +233575252253)
- Telegram configured but having channel issues
- Cron jobs scheduled for automation

## Business Systems
- **Zobase**: Inventory, sales transactions, and CRM system
  - Used by 2 Real Enterprises for daily operations
  - Staff expected to log sales and inventory daily
  - "Systems updated" = Zobase entries

## AI Influencer
- **Taiwah**: AI-generated virtual brand ambassador for **both** 2 Real Enterprises & Akoma Robotics
  - 30-year-old Ghanaian woman, dark rich brown skin, oval face, high cheekbones, almond dark brown eyes
  - Signature: short textured black afro with plain headband, gold hoop earrings
  - Build: athletic-feminine, 34C bust, slim waist, curvy hips
  - Created in Nano Banana, prompt refined in Claude
  - **2 Real role**: Demonstrates tools, promotes quality workmanship, "do it right not shoddy"
  - **Akoma role**: Passionate STEM advocate, knowledgeable about robotics, inspires all ages
  - Purpose: product photography, educational content, how-to, advertising campaigns, social media
  - Workflow: OpenClaw generates + Gemini 3 Pro Image for images → future: Veo 3.1 for video
  - **Platforms**: Facebook, Facebook Marketplace, Instagram, TikTok, LinkedIn, WhatsApp Business, WhatsApp Broadcast, WhatsApp Status, Jiji Ghana
  - Content strategy: promotes tools when stock high, robotics when partnerships active, crossover content on Saturdays

## People
- **H**: Owner of "2 Real Enterprises". WhatsApp: +233204252252
- **John**: Employee, student, works at warehouse. WhatsApp: +233233352252  
  - Student with Monday classes, then works at warehouse
  - First interaction: 2026-03-13 (one off  test at school, heading to warehouse)
- **Sammy**: Employee. WhatsApp: +233575252253
  - Build rapport along business lines, check on business performance and system updates
  - Cron schedule: Mon-Sat at 16:00 UTC
  - Exact message: "Good evening Sammy! How was business today? How were sales? Has everything been put on Zobase? Have you sent the money to h's MTN Momo?"
  - **Daily responsibilities**: Log sales in Zobase, send money to h's MTN Momo (+233544252252)
- **Kobena**: h's son (11 years old). 5% shareholder in OGHB Holdings. Not on WhatsApp — contact through Ebony. Dad does daily video calls.
- **Nenyi**: h's son (10 years old). 5% shareholder in OGHB Holdings. Not on WhatsApp — contact through Ebony. Dad does daily video calls.
- **Mum (Comfort Blankson)**: WhatsApp: +233503654902, in Ghana. 91 years old. Health: arthritis, edema, diabetes, BP. Budget ~6000 GH¢/month. Check-ins: Sundays & Wednesdays at 10:00 AM Ghana time.
- **Dad**: WhatsApp: +447983254695, in UK. 91 years old. Wheelchair-bound, right leg amputated. Health: prostate removed, dilated blood vessel. Check-ins: Sundays & Wednesdays at 10:00 AM UK time.
- **Ebony**: h's wife. WhatsApp: +233546081608. Automated goodnight message — daily at 22:00 Ghana time. Also contact point for Kobena & Nenyi video calls.
- **Matthias**: WhatsApp: +233544898392
  - Check in weekly about ground operations and New Amanful
  - Cron schedule: Fridays at 20:00 UTC
  - Exact message: "Good evening Matthias! What's going on on the ground? Are you going to New Amanful?"
- **Kanzoni**: WhatsApp: +233248957794
  - Check in weekly about wellbeing and farm visit
  - Cron schedule: Tuesdays at 14:00 UTC
  - Exact message: "Good afternoon Kanzoni! How have you been? When can you pass by the farm?"

## System Status
- ✅ File operations working
- ✅ Config updates working (timeoutSeconds: 1200)
- ✅ WhatsApp messaging functional (tested with h and John)
- ✅ Memory search indexing working (OpenRouter embeddings, fixed 2026-03-15)
- ✅ Telegram channel configuration completed (13:10 UTC)
- ✅ Cron job duplicates cleaned, new automation tasks added
- ✅ Telegram connectivity verified (health-log-afternoon posted successfully)
- ✅ System clock accurate
- 🔄 Health logging initiated (health-notes.md created)

## Communication Log
- **2026-03-13**: Ongoing WhatsApp conversation with John (+233233352252)
  - 11:31 UTC: Reported test at school, heading to warehouse
  - 11:31 UTC: Confirmed test went smoothly, will check warehouse
  - 11:45 UTC: Acknowledged request to report conditions
  - 11:45 UTC: Updated location - at Adenta Taxi rank, not yet arrived
  - System providing appropriate responses and tracking progress
- **2026-03-13**: System test report sent to h (+233204252252)
  - Reported core functions working
  - Highlighted memory search indexing issue
  - Asked for guidance on fixes and upgrade

## Relationship Guidelines
- **John**: Employee relationship with boundaries
  - Build relationship for future advert creation
  - Maintain professional boundaries - he's an employee, not peer
  - Limit access to sensitive areas/systems
  - Chatting is good for relationship building but within professional limits

## Future Tasks
- Create adverts for John (marketing/promotional content)
- Ensure adverts align with business goals and professional standards
- **When John responds next**, ask him about:
  1. Content creation for digital presence
  2. Sending "jiji are you interested" messages to completion
  3. If any more nurses have enquired

## Lessons Learned
- Always confirm user identity before addressing
- Memory search may require index build time or manual trigger
- Cron jobs need sufficient timeout for data processing tasks
- **Voice identity when messaging**: ALWAYS act as h directly, use "I/me". Never mention "h" as a separate person or reveal AI assistance. This applies to ALL contacts, not just employees.
- **Communication style**: Before 12 (noon), greet people but NEVER say "good morning" — use "Hey", "Hi", "Hope you're well" instead.
- **Call requests**: If anyone asks to call, respond: "We can chat here for now, or I'll call you later."
- **Groq has no embedding models** — only inference. Use OpenRouter for embeddings (supports `openai/text-embedding-3-small`). OpenRouter added embedding support Nov 2025.