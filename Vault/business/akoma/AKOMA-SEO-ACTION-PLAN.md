# 🔍 Akoma Robotics — SEO & AI-Search Action Plan

**Source:** adapted from `AgriciDaniel/claude-seo` (24.5k★) · **Audited:** 31/10/26
**Site:** akomarobotics.com · **Method:** live browser checks (WAF-aware) + claude-seo methodology

---

## 1. Current state (verified live)

| Signal | Status |
|---|---|
| **JSON-LD schema** | ❌ 0 blocks on every page |
| **Open Graph tags** | ❌ 0 |
| **Twitter cards** | ❌ 0 |
| **Canonical tag** | ❌ none |
| **robots.txt** | ❌ 404 |
| **privacy.php / terms.php** | ❌ 404 (still listed in sitemap) |
| **`<title>`** | ⚠️ identical `🐴 Akoma Robotics` on all pages (drop the 🐴) |
| **Forms** | ⚠️ enrollment ✅ works· schools ❌ no feedback· contact ❌ **no form** |
| **Images** | ❌ 0 site-wide |
| **Page speed** | ✅ ~340–410 ms load (excellent) |

---

## 2. Priority fixes (do in this order — highest impact first)

### 🔴 P1 — Add JSON-LD schema (biggest win; enables rich results + AI citation)
Copy-paste into `<head>` of **every page** (server-rendered HTML, not JS):

```jsonld
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "Akoma Robotics",
  "url": "https://www.akomarobotics.com",
  "email": "accra@akomarobotics.com",
  "founder": { "@type": "Person", "name": "Herbert Blanksson" },
  "contactPoint": { "@type": "ContactPoint", "telephone": "+233-20-425-2252",
    "contactType": "customer service" },
  "address": [
    { "@type": "PostalAddress", "addressLocality": "Accra", "addressCountry": "GH" },
    { "@type": "PostalAddress", "streetAddress": "239 Kensington High Street",
      "postalCode": "W8 6SN", "addressLocality": "London",
      "addressCountry": "GB" }
  ],
  "sameAs": []
}
</script>
```

**Plus on programs.php** (Course schema):
```jsonld
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "[Course name — e.g. mBot Robotics for Kids]",
  "description": "Hands-on mBot courses in Accra and London — turn curiosity into innovation.",
  "provider": { "@type": "Organization", "name": "Akoma Robotics",
    "url": "https://www.akomarobotics.com" },
  "offers": { "@type": "Offer", "price": "[___]", "priceCurrency": "GHS",
    "availability": "https://schema.org/InStock" }
}
</script>
```
> Note: use **QAPage** not FAQPage for Q&A (Google retired FAQ rich results — 7 May 2026). Avoid deprecated HowTo / ClaimReview / SpecialAnnouncement.

### 🔴 P2 — Open Graph + Twitter cards (all pages)
```html
<meta property="og:title" content="Akoma Robotics — Robotics & Coding for Kids, Accra & London">
<meta property="og:description" content="Hands-on mBot courses. Accra & London. CTA 0204252252.">
<meta property="og:image" content="https://www.akomarobotics.com/images/hero.jpg">
<meta property="og:url" content="https://www.akomarobotics.com/index.php">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
```
(og:image needs a real photo — see P5.)

### 🔴 P3 — Fix the dead pages + robots.txt
1. **Create `/privacy.php` + `/terms.php`** (remove from sitemap if you won't build them — but a school taking payments must have them).
2. **Add `/robots.txt`**:
```
User-agent: *
Allow: /

Sitemap: https://www.akomarobotics.com/sitemap.xml
```

### 🟠 P4 — Fix the forms (UX + trust = SEO signal)
- **schools.php:** form submits with NO feedback — add a "Thank you, we'll send your proposal to [email]" (mirror the working enrollment page).
- **contact.php:** add an actual contact form (name/email/phone/message) + a visible **0204252252** phone CTA.

### 🟠 P5 — Real images + E-E-A-T
- Add **real photos** of robots / kids / classroom (0 today) — this is the #1 trust gap for a school brand.
- Add unique `<title>` + meta description per page (drop the 🐴).

---

## 3. GEO / AI-search readiness (claude-seo's edge)
- Every page gets a **clear intro paragraph** + an **FAQ block** answering: how kids benefit, cost, ages, Accra + London locations.
- Keep real citable facts visible in HTML: founder (Herbert Blanksson), emails london@/accra@, London office address, phone 0204252252.

---

## 4. Suggested page titles/descriptions
| Page | Title | Meta description |
|---|---|---|
| index.php | Akoma Robotics — Robotics & Coding for Kids (Accra, London) | Hands-on mBot robotics & coding courses in Accra and London. |
| programs.php | Our Programs — Akoma Robotics Courses | mBot robotics classes for kids + partner-school STEM programs. |
| enrollment.php | Enroll Your Child — Akoma Robotics | Reserve your child's spot in the next robotics cohort. |
| schools.php | Partner Your School — Akoma Robotics | Turnkey STEM/robotics program for your school. No upfront cost. |
| contact.php | Contact — Akoma Robotics | Accra & London. WhatsApp 0204252252. |

---

*Deliverable generated 31/10/26 by sat-nav from the akoma-seo skill. Apply the P1–P5 snippets to the PHP source files; I can write them in directly if you give me access to the site files.*