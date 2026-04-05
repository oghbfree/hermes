# Nurse Applications Integration

## Form Link
**Google Form:** https://forms.gle/n83KW2FoG5ffYSJL8

## Setup Instructions

### 1. Create Google Service Account
1. Go to: https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable **Google Sheets API**
4. Create Service Account → Keys → Generate JSON key
5. Save the JSON file as `credentials.json` in this folder

### 2. Share Google Sheet
1. Open the Google Sheet linked to your form
2. Click **Share**
3. Add the service account email (from credentials.json) as viewer

### 3. Install Dependencies
```powershell
pip install gspread google-auth
```

### 4. Run the Processor
```powershell
python "C:\OpenClaw\.openclaw\workspace\raw_ingest\nurse-applications\nurse_applications.py"
```

## Workflow
1. Share form link via WhatsApp to potential nurses
2. Run processor daily to collect new applications
3. Review applications in `processed/` folder
4. Add approved nurses to your care team

## WhatsApp Integration
Use this short link for WhatsApp sharing:
```
https://forms.gle/n83KW2FoG5ffYSJL8
```

## Processing Schedule
Recommended: Run daily at 10 AM Ghana time
- New applications collected overnight
- Ready for morning review