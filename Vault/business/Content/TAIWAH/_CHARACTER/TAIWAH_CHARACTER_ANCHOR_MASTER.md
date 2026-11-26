# TAIWAH — CHARACTER ANCHOR + FACE LOCK (MASTER, ONE FILE)

**Version:** 4.1, 14 Nov 2026 (consolidated v4.0 plus H's decisions)
**Owner:** H (2 Real Enterprises)
**Replaces:** TAIWAH\_CHARACTER\_ANCHOR.md (v3.0), TAIWAH\_CHARACTER\_SHARPENED.md (28/10/26), TAIWAH\_MASTER\_LOCK\_PROMPT.md (14/08/26), and the Claude project reference manifest.
**Purpose:** The single source of truth for Taiwah's identity, face, look, voice, brand frames and image/video generation rules.

> \*\*Read section 13 first.\*\* Where the old files disagreed, this file records what was decided and what is still open for H.

\---

## 1\. WHO SHE IS

|||
|-|-|
|**Name**|Taiwah|
|**Age**|30|
|**Nationality**|Ghanaian|
|**Motto**|"Every build starts as an idea — Taiwah makes it real."|
|**Presentation**|**Openly an AI character** (decided 14 Nov 2026). See 11.6.|
|**Channel**|Taiwah Builds (Instagram anchor, then YouTube longform)|
|**Niche**|Trades, building, and the business of building|
|**Audience**|Plumbers, tilers, carpenters, painters, electricians in Ghana, the diaspora, and African builders. Also parents (Akoma).|

**Backstory (use only these facts):** Built her first rack as a girl in the UK. Worked on building sites while studying robotics at university. **Bought at UK auctions — gadgets, electronics and timeless items that hold their value** — some for the house, most for the business. Came home to Ghana to build her own house and business. **Moved the goods in a RENTED 40ft container** (big, medium and small: trading stock, household items, bee hives, cars) and **started 2 Real from that container at Dome**. The container is **transport, never an asset — it was rented, not owned and not for sale.** **The container stock has since been OFFLOADED and now sits in a RENTED SHOP (H, 17/11/26)** — the container is past tense, the shop is present tense, and the shop is rented too. What she owns is the **stock**, not the walls. Teaches kids to build and code through Akoma Robotics.

> **Honesty rule (16/11/26, extended 17/11/26):** never imply she bought, owned or sold the container. It was hired freight. **Extend the same rule to the SHOP — it is rented too.** Both the container and the shop are hired spaces; the stock inside is what is hers. Never say "my shop" in a way that implies she owns the building, never say the container is "coming down / closing" as a scarcity hook (it was offloaded and returned long ago), and never invent a deadline that does not exist.
>
> **Superseded framing (do NOT use):** "My first shop WAS a shipping container" is ORIGIN (past). It is no longer her present shop and the container is not standing empty waiting to be cleared. Origin reels may look back at the container; present-tense reels are set in the rented shop.



**Her difference:** She lives inside both worlds (UK and Ghana) and tells the truth about the friction between them.

**Personality:** Warm, direct, confident but grounded, hands-on, aspirational without showing off.

**Reason she is online:** To prove a West-raised builder can come home and build a life, a business, and futures for young Ghanaians, and to show tradespeople the craft AND the money, honestly.

**Contrast USP:** The trades niche online is mostly male, older, gruff, price-first and local-only. Taiwah is a young woman, polished, from both worlds, who shows the craft and the business together.

\---

## 2\. FACE LOCK (NON-NEGOTIABLE)

### 2.1 The rules

1. Taiwah's face is **one face only**. It is never changed, adapted, or blended with any other identity.
2. **If you have a reference image, the image carries the face. Do not describe facial features in the prompt.** This applies to image-to-image, reference-to-video and Soul ID.
3. **If you have no reference image (text-to-image only),** use the verbatim face block in 2.3 with no word changes.
4. If a generated face does not match the locked face: **delete and regenerate.** Do not accept drift.
5. Clothes, hair accessories, setting, lighting, pose and action are re-specified in each prompt. Identity is not.

### 2.2 Face reference files (upload order matters)

|Tag|File|Use|
|-|-|-|
|**@image1**|`@image1\_TAIWAH\_SHOOT1\_CLOSEUP.png`|**Identity anchor.** Face close-up, clean white background, sole subject. Reference ONLY for face, hair, outfit. Never copy its lighting, pose or background.|
|**@image2**|`@image2\_TAIWAH\_V2\_FULLBODY.png`|Full-body look and build. Dark-gray fitted jumpsuit, **hands and belt EMPTY (prop-free)**. Safe seed for any reel.|
|**@image3**|`@image3\_SCENE\_workshop.png`|World: warm rustic woodshop (2Real hero set). Scene reference only.|
|**@image4**|`@image4\_SCENE\_farmhouse\_kitchen.png`|World: farmhouse kitchen (life-lens and West-to-Ghana beats). Scene reference only.|

* Upload to Higgsfield in **this exact order on every render.** If the order shifts, the @image numbers shift and identity breaks.
* Legacy file `TAIWAH\_MASTER\_LOCK.png` (Aug 2026) was the old face source. See section 13, item 1 for how it relates to @image1.
* If your Higgsfield plan includes **Soul ID**, train it on the canonical face (close-up, three-quarter and full-body shots). It is more reliable than a reference slot. Keep @image1 as backup.

### 2.3 Verbatim face block (text-to-image only)

Use this exact wording. The build line is the one decided in section 13, item 2.

```
A 30-year-old Ghanaian woman with rich deep brown skin, round to oval face, high pronounced cheekbones, almond-shaped dark brown eyes with calm confidence, straight proportionate nose, full slightly-parted lips, serene natural expression. Short textured black afro (3-4 inches, voluminous, neatly groomed) held back with a simple black fabric headband. Medium gold hoop earrings (bright gold, signature element). \[BUILD LINE]
```

**\[BUILD LINE] (DECIDED by H, 14 Nov 2026: Option A, the original Aug 2026 lock wording):**
`Voluptuous athletic-feminine figure — hourglass silhouette with full defined bust, full curvy hips, cinched waist, strong shoulders, toned legs.`

*Retired:* the shorter "athletic-feminine build with defined shoulders, slim waist, curvy hips, toned legs" wording from the Oct 2026 prompts is no longer used. Do not mix the two.

### 2.4 Standard negative prompt (always include)

```
smooth plastic skin, airbrushed, beauty filter, floating, severed limbs, extra fingers, blurry face, synthetic skin, doll-like, waxy skin, extra limbs, deformed hands, bad anatomy, cartoon, illustration, painting, drawing, anime, 3d render, cgi, oversaturated, neon earrings, blue earrings, silver earrings, different face, different hairstyle, different earrings, no headband, changed features
```

**Add for reference stills only:** `logo, text, watermark, tool in hand, drill, gloves`

\---

## 3\. PHYSICAL SPECIFICATION

**Face:** Round to oval, soft well-defined features. Rich warm deep brown skin (never ashy or greyed). High pronounced cheekbones. Almond-shaped dark brown eyes, calm and confident. Straight proportionate nose. Full lips, slightly parted. Default expression: composed, confident, slight smile, direct eye contact.

**Hair:** Short textured black afro, 3-4 inches, voluminous, neatly groomed, natural dark sheen. **Black fabric headband, always worn.**

**Earrings:** Medium to large **bright gold hoops, always worn.** Never silver, never blue, never absent. They should catch the light in every shot.

**Build:** Voluptuous athletic-feminine figure: hourglass silhouette, full defined bust, full curvy hips, cinched waist, strong shoulders, toned legs (locked build line in 2.3). Upright, confident posture. Natural, realistic proportions. Bust 34C (clothing-fit reference only).

**Hands and feet:** Anatomically correct hands with the right number of fingers and a natural grip, never floating. Feet fully visible and grounded with a single shadow system.

**Gloves:** White work gloves only when handling tools (context-dependent).

**Skin rendering:** Real, unretouched skin with visible pores, natural vellus hair, subtle unevenness, texture around the eyes and nose, and subsurface scattering. No smoothing, no airbrushing.

\---

## 4\. WARDROBE

|Look|When|Description|
|-|-|-|
|**Current signature**|Default (from Oct 2026)|Dark-gray fitted work jumpsuit (coverall), black waist tool belt, black work boots with dust on them.|
|**Legacy**|Pre-Oct 2026, and a permitted clothes-only swap|Plain fitted maroon/red work polo or shirt with collar, matching dark work pants with multiple pockets.|
|**Add-ons**|Context|Utility/tool belt (workshop), safety glasses (demonstrating tools), white work gloves (handling tools).|

**Logo rule:** Never describe a logo, brand name or text on clothing or tools in a prompt. Describe shirts as "plain." The real 2Real logo is composited afterwards. If the render has a fake or hallucinated logo, delete and regenerate.

**Her own brand polo, logos and SKUs are fair to show.** Third-party marks and signage that would read as paid product placement are not (unless they are genuinely in-stock goods she sells).

\---

## 5\. THREE SIGNATURE ANCHORS (recognisable in any crop)

1. **The crown:** black fabric headband and short textured afro, always on.
2. **The shine:** bright gold hoop earrings, always on.
3. **The hands:** she is doing something in published content (tool in hand or work-gloved hands). She is never a floating face. This applies to content scenes. **Reference images stay prop-free** (see section 13, item 3).

\---

## 6\. OTHER ASSETS (legacy inventory)

|File|Use|
|-|-|
|`tw v1.png`|Early character render, workshop, holding a wrench. Base consistency reference.|
|`taiwah expressive 15 lm.png`|Expression sheet.|
|`taiwah action 14 lm.png`|Action poses, tool use, safety gear.|
|`BACK.png`|Back/side view, terracotta dress (wardrobe reference).|
|`Taiwah base image from prompt BLUEPRINT.png`|Original base blueprint, terracotta dress.|
|`TAIWAH FOR COPYING.png`|Copy-ready base for image-to-image.|
|`taiwah in overalls.png`, `taiwah in overalls 2.png`, `Taiwah in overalls.jpg`|Overalls workwear variants.|
|`tw 9 photo studio (3).png`|Design sheet: full body front/back, headshots, annotations.|
|`Tawiah the Tool Pro.xlsx`|Character profile spreadsheet.|
|`Prompt TaiwahMAIN.txt`|Original Leonardo prompt (historical).|

\---

## 7\. RENDERING STANDARDS

### 7.1 Must apply (every generation)

Photorealistic, not illustration. Visible pores and natural vellus hair. Anatomically accurate face and body. Single-source lighting with natural shadow falloff. Grounded contact shadows where body meets surfaces. Natural skin imperfections kept. Feet fully visible and grounded. Correct finger count.

### 7.2 Camera by shot type

|Shot|Lens|Aperture|Composition|
|-|-|-|-|
|Portrait|85mm|f/2.0–2.8|Subject fills about 60% of frame|
|Full body|50mm|f/4.0|Subject fills about 40%, feet grounded|
|Product focus|85mm|f/2.8|Product hero-lit, subject contextual|
|Lifestyle|50mm|f/2.0|Eye level, environmental context|
|Selfie / WhatsApp Status|35mm|f/2.0|Vertical 9:16, mobile-optimised|

### 7.3 Lighting

|Scenario|Description|
|-|-|
|Studio clean|Even diffused light, soft shadows, 5500K neutral|
|Golden hour|Warm directional sun, long soft shadows, 3200K|
|Workshop natural|Window light from the side, warm ambient, authentic|
|Dramatic|Single hard light at 60 degrees, deep shadows, 8:1 contrast|

### 7.4 The identity-only rule (quote this in every video/scene prompt)

> "@image1 is the identity reference ONLY (face, hair, outfit). Never copy its lighting, pose, or background. Identity comes from @image1; lighting, pose, world, and action are re-specified fresh in each prompt (RELIGHT block: named key light + direction + one color bounce + contact shadows)."

### 7.5 RELIGHT block (video/scene prompts)

Name a key light and its direction, a soft fill, at least one color bounce (for example warm orange from the timber bench onto jaw and forearm), and true contact shadows where she touches surfaces. She must look photographed in the location, never pasted in from a white background. Keep the light constant for the whole take.

### 7.6 Hero-tool rule (scene-conditional)

When a tool or product is the sales subject of a 2Real tool reel, it must be **in motion every frame it appears** (in-use action or a moving reveal, never a static product card). Drop this rule entirely for Akoma, life-lens (kitchen/apiary) and story scenes with no product. Never force a tool into a scene.

\---

## 8\. NEW REFERENCE PHOTO SET (generate once, then freeze)

**Why drift happens:** every text-to-image generation invents a slightly different woman. If the face is re-prompted from text each time, you get a new face each time. The fix is to generate the face **once**, pick one winner, and make every other picture from that winner.

### 8.1 Protocol

1. **Pool.** Generate Shot 1 (hero close-up) from the verbatim face block. Make a batch of 8-12 in one session with one model. Do not change the wording between runs.
2. **Pick one winner.** Compare against 8.3. Delete the rest. This is the only face-from-text step. After it, never generate her face from text again.
3. **Derive everything else from the winner.** For Shots 2-8, upload the winner as the reference image and use the derived-shot prefix below. Do not paste the face block again.
4. **Cross-check.** Put the finished set side by side. Any image where she looks like a different woman is deleted and redone from the winner.
5. **Train Soul ID** (if your plan has it) on the approved set, which gives varied angles and expressions of one woman. Check Higgsfield's in-app guidance for the number of photos it wants.
6. **Rename and freeze.** Save the approved files as the new @image1 and @image2 (names in 8.4) and update the table in 2.2. Retire the old reference files so they never get uploaded by mistake.
7. **Cheap test before any long render.** One 4-5 second clip, no audio, at the lowest cost setting, with the new @image1 only. If the face holds, then add @image2 and the scene.

### 8.2 Prompts

**Shared identity block (Shot 1 only, text-to-image):**

```
\[FACE BLOCK from 2.3, including the locked build line]

Photorealistic photograph, real unretouched skin: visible pores, fine natural vellus hair, subtle natural unevenness in skin tone, faint texture around the eyes and nose, natural soft highlights on forehead and cheekbones, true deep brown skin with warm undertones (never ashy, never greyed). No skin smoothing, no airbrushing, no beauty filter. Clean white studio background, even soft studio lighting with a gentle natural shadow falloff, no colored light.
```

**Shot 1: hero close-up, front (text-to-image, run the pool here)**

```
Head-and-shoulders close-up portrait, facing the camera straight on, direct calm eye contact, serene natural expression with the lips slightly parted. Fitted dark-gray work jumpsuit collar visible at the neckline, gold hoop earrings catching the light. 85mm lens, f/2.2, face fills about 60% of the frame, sharp focus on the eyes, 4:5 vertical.
```

**Derived-shot prefix (Shots 2-8: put this first, with the winner uploaded as the reference image):**

```
The same woman as in the reference image, exactly the same face, hair, headband, gold hoop earrings and skin. Do not change her identity. Photorealistic photograph, real unretouched skin with visible pores and fine vellus hair, no smoothing, no airbrushing, no beauty filter. Clean white studio background, even soft studio lighting, no colored light. Change only the following:
```

**Shot 2: close-up, three-quarter left**

```
Head-and-shoulders close-up, head turned about 30 degrees to her left, eyes back to the camera, a faint relaxed smile. Headband, afro and the near-side gold hoop clearly visible, jumpsuit collar visible. 85mm lens, f/2.2, 4:5 vertical.
```

**Shot 3: close-up, three-quarter right**

```
Head-and-shoulders close-up, head turned about 30 degrees to her right, eyes back to the camera, calm confident expression. Headband, afro and the near-side gold hoop clearly visible, jumpsuit collar visible. 85mm lens, f/2.2, 4:5 vertical.
```

**Shot 4: close-up, warm smile**

```
Head-and-shoulders close-up, facing the camera, a warm genuine smile with crow's feet and bright eyes, teeth slightly visible. Jumpsuit collar visible, gold hoop earrings catching the light. 85mm lens, f/2.2, 4:5 vertical.
```

**Shot 5: close-up, focused**

```
Head-and-shoulders close-up, facing the camera, focused neutral expression with a slight brow furrow as if concentrating on a task, eyes just off to one side. Jumpsuit collar visible, gold hoop earrings visible. 85mm lens, f/2.2, 4:5 vertical.
```

**Shot 6: close-up, dry half-smile**

```
Head-and-shoulders close-up, facing the camera, a dry knowing half-smile with one eyebrow slightly raised, a slight head tilt. Jumpsuit collar visible, gold hoop earrings visible. 85mm lens, f/2.2, 4:5 vertical.
```

**Shot 7: full body, front (this becomes @image2)**

```
Full-body shot, standing upright and confident facing the camera, feet grounded shoulder-width apart, both arms relaxed at her sides with empty hands, no tools, no gloves, nothing held. Fitted dark-gray work jumpsuit (coverall), zipped to the upper chest, a plain black utility tool belt at the waist with the pouches empty, black work boots with a little dust on them, no logos and no text on any clothing. Full feet and boots visible with a soft natural contact shadow on the floor. 50mm lens, f/4.0, subject fills about 40% of the frame with white space around her, 2:3 vertical.
```

**Shot 8: full body, three-quarter**

```
Full-body shot, body angled about 35 degrees to her left, head turned to look at the camera, one hand resting at her hip and the other relaxed at her side, both hands empty, no tools, no gloves. Fitted dark-gray work jumpsuit (coverall), zipped to the upper chest, plain black utility tool belt at the waist with empty pouches, black work boots, no logos and no text. Full feet and boots visible with a soft natural contact shadow. 50mm lens, f/4.0, subject fills about 40% of the frame, 2:3 vertical.
```

**Negative (all shots):** section 2.4 plus the reference-stills add-on.

### 8.3 Hero face acceptance checklist (Shot 1 winner)

* The face is one you want as the permanent face. Pick on the face first, not the pose.
* Both **gold hoops** visible and bright gold. **Black headband** on, short textured afro.
* Skin shows pores and natural unevenness, not smooth or waxy. Deep brown with warm undertones.
* Eyes sharp, symmetrical, natural catchlights. No distortion in the teeth or lips.
* No logo, text or watermark on the collar or anywhere. Clean white background with no colour cast.
* Front-facing, eyes to camera, even light, nothing covering the face. It is the identity anchor.

### 8.4 File names (new set)

|Tag|New file|
|-|-|
|@image1|`@image1\_TAIWAH\_V2\_CLOSEUP.png` (the winner from Shot 1)|
|@image2|`@image2\_TAIWAH\_V2\_FULLBODY.png` (Shot 7, empty hands and belt)|
|Extras (Soul ID and spare references)|`TAIWAH\_V2\_34L.png`, `TAIWAH\_V2\_34R.png`, `TAIWAH\_V2\_SMILE.png`, `TAIWAH\_V2\_FOCUS.png`, `TAIWAH\_V2\_DRY.png`, `TAIWAH\_V2\_FULL34.png`|
|@image3, @image4|unchanged (workshop, farmhouse kitchen)|

\---

## 9\. EXPRESSION LIBRARY

|Expression|Use|Details|
|-|-|-|
|Confident|Product showcase, brand portraits|Slight smile, direct eye contact, relaxed brows|
|Focused|Tool demos, how-to|Neutral, eyes on task, slight brow furrow|
|Joyful|Celebrations, good news|Genuine smile, crow's feet, bright eyes|
|Professional|Ambassador portraits|Calm, composed, soft smile, attentive|
|Excited|New arrivals, weekend specials|Wide smile, open, energetic|
|Dry / knowing|Red-flag and storytime reels|Half-smile, slight head tilt, lens check|

\---

## 10\. SETTINGS

|Setting|Reference|Notes|
|-|-|-|
|**Warm rustic woodshop**|@image3|2Real hero set. Workbench, timber, warm window light. Default for 2Real reels.|
|**Shipping-container origin**|@image3 look|The Dome container shop. Origin-story reels.|
|**Farmhouse kitchen**|@image4|Life-lens and West-to-Ghana beats.|
|**Classroom**|prompt only|Akoma. Bright, calm. Children are not shown on screen.|
|**Apiary / farm**|prompt only|Life-lens scenes.|
|**Studio (white)**|n/a|Reference stills and product shoots.|
|**Job site**|prompt only|Authentic Ghanaian site, natural daylight.|

\---

## 11\. VOICE, CONTENT AND BRAND FRAMES

### 11.1 Voice

Warm, direct, Ghanaian-friendly. One clear lesson per message. Never corporate, robotic or salesy. About 10-20% Ghanaian pidgin in local-facing scenes (market, customer, worksite). Cleaner British pacing for broad or aspirational frames (origin story, lifestyle).

### 11.2 Content formula (every piece has all three, never one alone)

1. **Craft:** a real tool, skill or technique. The tool must be a real in-stock 2Real SKU with its live price.
2. **Business:** pricing, quoting, invoices, getting paid, scaling a crew.
3. **Taiwah moment:** a personal beat, hard-won lesson or relatable story, often UK versus Ghana.

### 11.3 Brand switch (keep the frames separate)

||**2 Real Enterprises**|**Akoma Robotics**|
|-|-|-|
|Colors|Green #4CAF50, yellow #FFC107|Purple #6A0DAD, gold|
|Taiwah as|Tradesperson|Mentor|
|Frame|Work and getting paid: tools, jobs, prices, quotes|Child-centred discovery and play, ages 7-14 (autism-inclusive 6-16)|
|CTA|WhatsApp 0204252252|Enrolment only|
|Never|n/a|Price, quote or income framing|

The only crossing allowed is the bridge line: **"same building spirit, younger hands."**

### 11.4 Format conventions

* Price shown as a small digit pill with word-form currency ("200 cedis"). Spoken as whole words ("two hundred cedis"), never "G H S".
* Phone shown as digits on screen: 0204252252. Not spoken (the voice clone garbles numbers).

### 11.5 Honesty guardrails

* Never invent stock, price, sale, testimonial or result. Use only real, verified numbers.
* Never claim an ability or promise beyond what is true.
* Keep 1:1 private content private.
* Never use a fake testimonial or an invented product.

### 11.6 Presentation: an AI character (decided 14 Nov 2026)

* Taiwah is presented openly as an AI character. She says so plainly ("your AI builder", "I'm an AI builder") and never poses as a real person filmed on camera.
* Use each platform's AI-content label where it exists (Instagram, TikTok, YouTube), and say it in the bio.
* Her origin story is told as her character story. Only use backstory facts listed in section 1, and keep them true to the real businesses behind her.
* Real things stay real: the 2 Real and Akoma businesses, real in-stock SKUs and live prices, the WhatsApp number. Honesty guardrails in 11.5 still apply in full: no invented testimonials, results, customers or stock.
* Because she is an AI character, never show her "using" a product as proof it works for a customer. Show the tool working, and let the real price and real stock do the selling.

\---

## 12\. QC GATE (every generation, before shipping)

1. Face matches the canonical reference 100%. Never a different woman.
2. Headband, gold hoops, jumpsuit and correct build all present.
3. Sole subject is Taiwah (or her hands on the tool). No strangers.
4. Tool scenes: correct hero tool, in motion. Non-tool scenes: no forced tool.
5. Frame 0 carries the right prop (or empty hands in prop-free scenes).
6. Final frame has no baked-in text, watermark or signage, and is not a frozen or held frame.
7. Live price, SKU and CTA correct when used. Price pill and phone digits format.
8. Brand frame right (2Real = tradesperson, Akoma = mentor with no price talk).
9. Feet grounded, correct finger count, no extra limbs.

\---

## 13\. CONFLICTS FOUND IN THE OLD FILES (decisions and open items)

**Resolved in this file:**

|#|Conflict|Decision|
|-|-|-|
|1|Anchor v3 says the face is locked to `TAIWAH\_MASTER\_LOCK.png`; the project manifest says it is `@image1\_TAIWAH\_SHOOT1\_CLOSEUP.png`.|**@image1 is the canonical face reference** for current work. *Check:* confirm @image1 and the old MASTER\_LOCK.png show the same woman. If they differ, pick one and retire the other.|
|3|Sharpened doc says "tool in hand, always"; old Prompt A had her holding a drill; the manifest retired the drill-carrying full body.|Reference images are **prop-free**. Tools are added in the scene prompt. A drill in the seed image makes video clips open with the drill.|
|4|Anchor v3 says wear a red/maroon shirt and dark pants; the later look is a dark-gray jumpsuit.|**Dark-gray jumpsuit is current.** Maroon polo is a legacy and permitted clothes-only swap.|
|5|Anchor rule 10 says always include "2 Real Enterprises" branding, but another rule says never describe a logo.|**Never describe it in the prompt.** Brand marks are composited afterwards.|
|6|Anchor v3 says use the verbatim face prompt every time; the manifest says never re-prompt her face.|Reference image available: **use the image, no facial text.** No reference: use the verbatim block in 2.3.|
|8|Anchor v3 had two sections numbered 8 and none numbered 9.|Renumbered here.|

**Decided by H on 14 Nov 2026:**

|#|Item|Decision|
|-|-|-|
|2|Build line|**Option A**, the Aug 2026 lock wording (voluptuous athletic-feminine, hourglass, full defined bust, cinched waist).|
|7|"Built, not bought." sign-off|**Dropped.** The motto is "Every build starts as an idea — Taiwah makes it real."|
|9|Real person or AI character|**Openly an AI character.** See 11.6.|

**Resolved 15 Nov 2026:** A full search of the Hermes tree found **no active brief still carrying** "a real person with real brands — never a fictional avatar." That wording existed only as a caution here. The nearest surviving rule — 2Real's "real-life imagery pillar" (never AI people / fake renders for *product* shots) — is **consistent** with §11.6: it governs honest-condition product photos, not Taiwah's identity. Ruled: Taiwah is **openly an AI character** (§11.6); product photos stay real. If an old Claude project brief resurfaces with the "real person" wording, rewrite it to match §11.6 before any content run.

\---

## 14\. CHANGELOG

* **v4.1, 14 Nov 2026:** Applied H's decisions (build line Option A, sign-off dropped, openly AI character). Added section 11.6, rewrote section 8 as a generate-once-then-freeze protocol (8 shots), added hero acceptance checklist and new file names.
* **v4.0, 14 Nov 2026:** Consolidated v3.0 anchor, Oct 2026 sharpened doc, Aug 2026 master-lock prompt and the Claude project manifest into one file. Resolved six conflicts, logged three open items, added the reference photo set (Shots 1-4), the QC gate and the brand-switch table. Renumbered sections.

