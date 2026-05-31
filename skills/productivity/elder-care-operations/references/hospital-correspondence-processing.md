# Hospital Correspondence Processing Workflow

When hospital letters, discharge summaries, invoices, or other medical documents arrive as images:

## Step 1: Log the Document
- Add entry to the relevant structured care document's **Correspondence Log** section
- Record: date received, document type, source, key points
- For dad: `FAMILY_INSIGHTS_DAD.md` → Section 8
- For mum: Create/use equivalent care document

## Step 2: Extract Clinical Information
Read the document image carefully and extract:
- **New diagnoses** → update Active Conditions section
- **Medication changes** → update Current Medications section
- **Procedures performed** → update Medical Timeline
- **New appointments** → update Upcoming Appointments
- **Care package changes** → update Care Package section
- **Red flags** → escalate immediately if urgent

## Step 3: Update All Relevant Sections
Don't just log — actively update every section that the new information touches. A single discharge summary may update 4-5 sections.

## Step 4: Image Enhancement (if quality is poor)
For scanned/photographed documents that are hard to read, use the image enhancement pipeline. See `references/image-enhancement-pipeline.md` for the full technique.

Key points:
- Use **system Python** (`python /c/Users/User/.hermes/workspace/script.py`), NOT execute_code sandbox (no PIL in sandbox venv)
- 2x Lanczos upscaling → autocontrast → unsharp mask → contrast boost → sharpness
- Save as PNG for lossless quality
- For music notation: enhancement helps but cannot replace proper flatbed scanning at 600+ DPI

## Step 5: Cross-Reference
- Check if the new information changes any care plan items
- Update cron job prompts if care needs have changed
- Notify H of any significant changes via Telegram