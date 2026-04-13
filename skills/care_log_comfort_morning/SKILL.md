# SKILL: Geriatric Care Monitor (Comfort - Morning)

## DESCRIPTION
Executed daily at 08:00 AM. This skill facilitates the specialized health tracking for Comfort (91). It provides a structured template for the carer (H) to ensure medication, mobility, and cognitive state are recorded consistently.

## CAPABILITIES
- Clinical Data Templating
- Caregiver Support
- Longitudinal Health Archiving

## WORKFLOW

### 1. Template Deployment
Post the following message to **Telegram Topic 51 (#health-log-mum)**:

"🏥 **MUM MORNING LOG - $(date +%F)**
*Comfort (91), Carer: H (Son)*

**Breakfast:** **Drink:** **Medication taken:** [yes/no]
**Mobility:** [good/assisted/poor]
**Mood:** [good/low/confused]
**Symptoms:** [none/list]
**Severity:** [1-5]
**Notes:** *Please reply to this message with the completed details.*"

### 2. File Initialization
1. **Create**: `workspace/health/mum/$(date +%Y-%m-%d).md`.
2. **Metadata**: Pre-populate the file with the date, time of the prompt, and the carer assigned (H).

### 3. Data Processing
Upon receiving the response from Topic 51:
- **Parse**: Extract all fields from the template.
- **Alert Logic**: If **Mobility** is 'poor' OR **Mood** is 'confused' OR **Severity** is >= 4:
  - Immediately mirror the entry to Telegram Topic 141 (#urgent) with the header: "🚨 **HEALTH ALERT: COMFORT - MORNING REVIEW REQUIRED**"
- **Save**: Update the daily file and the monthly master table at `memory/health/MUM_MASTER_$(date +%Y-%m).md`.

## GUIDELINES
- **Tone**: Respectful, clinical, and supportive.
- **Priority**: This is a Tier-1 safety task.
- **Data Integrity**: Ensure the "Medication taken" field is highlighted; this is the most critical metric for the nightly synthesis.