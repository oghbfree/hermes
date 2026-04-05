# Homework Planning System - Development Outline

## Project: Academic Planner for K (11) & N (10)

### Goal
Build a weekly homework planning system that integrates around extracurricular activities

### Core Features
1. **Schedule Input Module**
   - Capture activity days/times
   - School finish times
   - Homework load per subject
   - Family rules (screen time, quiet hours)

2. **Weekly Template Generator**
   - Visual time blocks (hourly slots)
   - Color-coded by activity type
   - Pre-planned homework slots
   - Free time / buffer zones

3. **Flexibility Features**
   - Weekend catch-up buffer
   - Daily adjustment capability
   - Progress tracking

### Data Structure
```json
{
  "student": "K/N",
  "age": 11/10,
  "activities": [
    {"name": "football", "day": "Mon", "time": "16:00-18:00"}
  ],
  "homework": {
    "Math": "30min/day",
    "English": "20min/day",
    "Science": "2x/week"
  },
  "schedule": {
    "school_end": "15:30",
    "dinner": "19:00",
    "bedtime": "21:00"
  }
}
```

### Development Steps
- [ ] Phase 1: Data collection template (form/questionnaire)
- [ ] Phase 2: Weekly schedule builder (algorithm)
- [ ] Phase 3: Visual output generation (text-based schedule)
- [ ] Phase 4: Integration with current workspace

### Output Format
- Text-based weekly grid
- Color-coded via emojis or ASCII
- Export to markdown for review

---

**Owner:** Librarian  
**Status:** Planning phase - awaiting details from H
