# Meal Plan Template — Elder Care Nutrition

## Purpose

This template governs how to build weekly meal plans for H's elderly parents and household members. It integrates:
1. Clinical dietary constraints (diabetes, CKD, HTN, obesity, chewing difficulty)
2. Doctor-recommended dietary protocols (e.g., Dr Ferguson's alkaline/plant-based protocol)
3. Local Ghanaian cuisine adaptation
4. Available ingredient inventory (e.g., UK food haul)
5. Separate texture/seasoning requirements for patient vs. other household members

## Trigger Conditions

Create a meal plan when H:
- Sends a list of available ingredients and asks to build meals around them
- References a dietary protocol (e.g., "Dr Ferguson's plan") and wants it adapted
- Asks for weekly planning for a parent's carer to follow
- Mentions clinical dietary restrictions alongside food

## Required Inputs

When building a meal plan, gather or confirm:

1. **Patient clinical profile** — conditions, recent lab values, BMI, chewing/swallowing ability
2. **Dietary protocol** — any doctor-recommended diet (alkaline, low-sodium, renal diabetic, etc.)
3. **Available ingredients** — inventory of what's on hand (food haul, pantry, local market staples)
4. **Household members** — who else is eating and their dietary needs/texture tolerance
5. **Cooking capacity** — what equipment is available, complexity the carer can handle

## Clinical Constraints — Quick Reference

### Diabetes (controlled, HbA1c ~41)
- No added sugar; honey ≤ ½ tsp if needed
- Fruit portions controlled (½ banana, small pawpaw per sitting)
- Rice portions moderate, not heaped
- Favour low-glycaemic staples: millet (koko), banku over white rice

### CKD Stage 3b (eGFR 41)
- Protein portions moderate (not excessive — strains kidneys)
- Soak dried/salted fish thoroughly to reduce sodium
- Adequate hydration between meals
- Limit high-potassium excess (don't give multiple whole bananas in a day)

### Hypertension
- Minimal added salt in all cooking
- Use pepper, ginger, garlic, dawadawa (sparingly) for flavour
- Avoid heavy palm oil soups

### Obesity (BMI 39.2)
- Portion control — smaller plates
- No frying; steam, bake, poach, stew only
- Butter/oil sparingly

### Chewing/Dysphagia Difficulty
- All food soft: stewed, flaked, mashed
- No crunchy textures
- Smaller, more frequent meals if appetite is low

## Dr Ferguson's Core Protocol

Dr Stephen Ferguson (ND, PhD) promotes an alkaline/plant-based/living-foods protocol. Key principles:

1. **Alkaline-focused** — green vegetables, fruits, nuts; minimise acid-forming foods
2. **Plant-based first** — vegetables, legumes, whole grains as foundation
3. **Limited animal protein** — small portions of fish preferred; red meat sparingly (1-2x/week max)
4. **No processed food / no refined sugar**
5. **Living enzyme-rich** — raw or lightly cooked where possible; steaming > frying
6. **Green smoothie daily** — leafy greens + fruit + water (no sugar) as staple breakfast/drink
7. **Hydration** — water, herbal teas throughout the day
8. **Plate size matters** — 6-inch saucer, 7 spoons total per meal (Fish | Rice+Potato | Veg+Salad)

### ⚠️ Handwritten Overrides for Comfort (Mum) — THESE TAKE PRIORITY

The original document has handwritten overrides that make Mum's version **stricter** than the printed protocol:
- **NO NUTS** (all nuts and seeds — cashews, almonds, linseeds, sunflower, pumpkin)
- **NO MEAT** (all — chicken, turkey, lamb, pork, beef)
- **NO DAIRY** (cheese, milk, yogurt, ice cream)
- **NO EGGS**
- **NO WHEAT/BREAD/PASTA** (all forms including brown pasta)
- **NO PLANTAIN** and **NO WHITE RICE** (both acid-forming; carbs only 1 small meal/week)
- **NO SALT** (handwritten override on printed "sea salt")
- **NO TINNED FISH, NO SMOKED FISH** (only fresh fish allowed)
- **NO FRYING** (steam, bake, poach, stew only)
- **NO VINEGAR** except organic apple cider vinegar

**This makes Mum's diet essentially: vegan + fresh fish, no grains/starches, zero processed food.**

### What Mum CAN Eat (Definitive List)
- Vegetables (raw/lightly cooked): avocado(unlimited), kale, broccoli, watercress, cabbage, garlic, tomato, onion, cucumber, green beans, callaloo, rocket, peas, celery, parsley, asparagus, cauliflower, baby spinach, Chinese sprouts, spring greens
- Fruits (any kind): 1 whole lemon daily (mandatory), bananas 2x/week before 12pm, strawberries, blueberries, raspberries
- Fresh fish only: trout, seabass, red snapper, sardines, mackerel, salmon, pilchards, tuna (fresh only), halibut, herring, swordfish, kippers
- Legumes (small amounts): quinoa, black eye peas, pinto beans, lentil dhal, millet, aduki beans, bulgar, fasolia beans, haricot beans, red lentils, split peas, soya beans, chickpeas, kidney beans, spelt
- Oils (no frying): olive oil, hemp oil, flax oil, avocado oil (use sparingly)
- Seasonings: curry powder, turmeric, bay leaves, fresh ginger, cinnamon, cayenne, nutmeg, parsley (NO SALT)
- Drinks: warm — boiled water/lemon, herbal tea, mint, ginger tea, camomile, fennel tea; cold — rice milk, oat milk, coconut water, sorrel (homemade), fresh grapefruit, coconut milk (fresh); water 1.5-2L daily
- Other: apple cider vinegar, almond butter

### Reference File
See `references/dr-ferguson-meal-plan.md` for the full transcribed original with all 6 pages, all handwritten overrides, the detox cycle protocol, herbal supplement instructions, plate diagram, eating schedule, and daily routine.

### Ghanaian Cuisine Compatibility

Many Ghanaian staples are naturally alkaline-forming and fit Dr Ferguson's protocol well:
- **Alkaline:** kontomire (cocoyam leaves), alefu (amaranth greens), okro, tomato-based light soups, yam, cassava, groundnuts
- **Use sparingly:** dawadawa (sodium), palm oil (fat, offsets alkaline benefit), saltfish (soak well)
- **Avoid on this protocol:** heavy palm oil soups, fried foods, processed items, excess red meat

### Foods to Restrict on Dr Ferguson's Plan
| Food | Reason | Limit |
|------|--------|-------|
| Red meat (beef, lamb, duck) | Acid-forming | 1-2x/week |
| Cheese/dairy | Acid-forming | Small amounts only |
| Fried foods | Destroy enzymes | Never use frying |
| Processed/refined | Against protocol | Avoid entirely |
| Excess palm oil | Offsets alkaline benefit | Minimal only |

## Meal Plan Output Format

Save completed plans as `MEAL_PLAN_<context>.md` in the workspace root (NOT in care log files).

Structure:
```
# 🍽️ Weekly Meal Plan — [Protocol] × [Cuisine]
## [Context] | [Patient] & [Household Members]
### Created: [Date]

### Clinical Principles Applied
[Which constraints are active, key rules]

### Available Ingredients
[Inventory table with quantities]

### Local Staples Assumed Available
[What can be sourced locally — rice, yam, plantain, kontomire, etc.]

### 7-Day Plan
[Day-by-day: breakfast / lunch / dinner for patient AND household members]
[Each dish: name, primary ingredient, brief method, Dr Ferguson compliance note]

### Ingredient Usage Summary
[Table: Item / Total / Used / Remaining]

### Clinical Notes for Carer
[Specific warnings tied to patient conditions]

### Carer Cooking Instructions
[Prep ahead, batch cook, separate seasoning, texture check, no frying]
```

## Cooking Rules for Carer

1. **Prep the night before** — soak dried fish overnight, marinate meats early
2. **Batch cook** — rice and banku can be made in bulk for 2-3 days
3. **Separate seasoning** — cook the base stew/soup mild for the patient; add pepper/salt to other household portions after
4. **Texture check** — all fish should flake easily; all vegetables soft (not crunchy)
5. **Green smoothie daily** — blend fresh greens + banana + ginger + water every morning for the patient
6. **No frying** — always steam, bake, poach, or stew
7. **Butter/oil** — small knob per dish, not generous

## Integration with Health Logs

Meal plans are standalone files. DO NOT append to `CARE_LOG_COMFORT_YYYY-MM.md`. However:
- Reference the care log to check recent food tolerance notes (did a dish sit well? any digestive issues?)
- After meals are served, any carer observations about appetite, tolerance, or digestive response should be logged in the care log's meal sections

## See Also

- `medical-record-review-comfort.md` — Comfort's full clinical summary for lab values and trends affecting dietary choices
- `CARE_LOG_COMFORT_YYYY-MM.md` — check recent entries for food tolerance notes
