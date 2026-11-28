# BROWSER & EMAIL ACCESS SETUP — NON-INTERACTIVE GUIDE

**Created:** 30 Nov 2026  
**For:** H  
**Goal:** Read-only email access + OpenRent browser access

---

## PART 1: READ-ONLY EMAIL ACCESS (2realenterprisesgh@gmail.com)

### Step 1: Run the OAuth Setup

**Run this command in your terminal:**

```bash
cd C:/Users/User/AppData/Local/hermes/profiles/sat-nav
python skills/productivity/google-workspace/scripts/auth_readonly.py
```

**What will happen:**
1. A browser window will open
2. You'll be asked to log into your Google account (2realenterprisesgh@gmail.com)
3. Grant permissions for "Read-only Gmail + Calendar"
4. Browser will redirect to `http://localhost:1/?code=...` (this will FAIL - that's expected)
5. **Copy the ENTIRE URL** from the address bar
6. Paste it back into the terminal and press Enter

**After this completes:** I'll be able to read your emails (but NOT send/reply/delete)

---

## PART 2: BROWSER ACCESS (OpenRent + other sites)

### Option A: Use Cloud Browser (Recommended)

**Get a Browser Use API key:**
1. Go to https://browser-use.com/
2. Sign up for free tier
3. Copy your API key

**Set the key:**
```bash
hermes config set browser.use_api_key YOUR_KEY_HERE
```

**Verify:**
```bash
hermes config get browser.use_api_key
```

### Option B: Fix Local Chrome (Alternative)

**Run this to fix permissions:**
```bash
mkdir -p C:/Users/User/AppData/Local/hermes/profiles/sat-nav/cache/browser/chromium
icacls "C:/Users/User/AppData/Local/hermes/profiles/sat-nav/cache/browser" /grant Users:(OI)(CI)F /T
```

**Then restart Hermes Desktop**

---

## PART 3: TEST EMAIL ACCESS

**After Step 1 completes, test with:**

```bash
cd C:/Users/User/AppData/Local/hermes/profiles/sat-nav
python skills/productivity/google-workspace/scripts/google_api.py gmail search "is:unread" --max 5
```

**Should return:** JSON list of your 5 most recent unread emails

---

## STATUS

- ✅ Email added to vault: `2realenterprisesgh@gmail.com` (CONTACTS.md)
- ⏳ Email OAuth: Needs Step 1 above (browser flow)
- ⏳ Browser access: Needs Part 2 (cloud key OR local fix)

**Once both complete, I'll be able to:**
- Read your emails (inbox triage, search, extract info)
- Access OpenRent dashboard (check inquiries, optimize listing)
- Monitor property platforms (RightMove, Zoopla, etc.)

---

**Next:** Run Step 1 above, then tell me when it completes.
