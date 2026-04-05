# Mission Control Dashboard

## New Feature: PRD Generator

### ?? PRD Generator (Librarian ? Cruncher ? Architect Workflow)

**Access:** Sidebar ? "PRD Generator"

### How It Works

**1. Librarian Phase (Requirement Capture)**
- User enters project details via form
- Librarian captures requirements and context
- Form fields: Name, Description, Requirements, Stakeholders, Timeline, Budget

**2. Cruncher Phase (Technical Analysis)**
- Extracts technical requirements from input
- Analyzes constraints and dependencies
- Identifies key milestones and success criteria

**3. Architect Phase (Strategic Planning)**
- Creates strategic roadmap
- Defines phases and timeline
- Risk assessment and mitigation

**4. Document Generation**
- Standardized PRD format output
- Saved to Docs section
- Available for download

### PRD Template Sections

```
? Executive Summary
? Project Overview & Objectives
? Success Metrics
? Functional Requirements
? Non-Functional Requirements
? Stakeholder Matrix
? Timeline (Phased approach)
? Budget & Constraints
? Risk Assessment
? Technical Architecture
? Change Log
```

### Using the PRD Generator

**Step 1: Fill Out Form**
- Project Name: e.g., "Akoma Robotics School Pilot"
- Description: Project goals and objectives
- Requirements: Key requirements (one per line)
- Stakeholders: Team members and roles
- Timeline: Duration and phases
- Budget/Constraints: Resources and limitations

**Step 2: Generate**
- Click "Generate PRD"
- Review preview in real-time

**Step 3: Save or Download**
- **Save to Docs** - Stores in mission-control/docs/prds/
- **Download** - Get .md file for external use

### Sample PRD Output

```markdown
# Akoma Robotics School Pilot

## Product Requirements Document
Generated: 2026-03-31
Version: 1.0

---

## Executive Summary
Launch robotics education program in 3 schools...

## Requirements
- [ ] Secure partnerships with 3 schools
- [ ] Train 2 facilitators
- [ ] Deploy mBot kits
- [ ] Track student progress

## Timeline
Phase 1: School outreach (Week 1-2)
Phase 2: Training (Week 3-4)
Phase 3: Launch (Week 5+)
```

### Workflow Integration

```
User Input (Form)
    ?
Librarian (Capture Requirements)
    ?
Cruncher (Technical Analysis)
    ?
Architect (Strategic Planning)
    ?
Generated PRD (Standardized Document)
    ?
Saved to Docs Section
```

## All Mission Control Features

### ? Available Now
- **Dashboard** - Overview stats
- **Task Board** - All tasks from tasks-queue.md
- **?? Calendar** - Weekly schedule visualization
- **?? Past Memories** - Complete memory history
- **Daily Memory** - Memory organized by date
- **Long-Term Memory** - Strategic context
- **?? Docs & Artifacts** - All documents
- **?? PRD Generator** - NEW - Librarian?Cruncher?Architect
- **?? Memory Search** - Search everything
- **?? Heartbeat** - System status
- **??? Custom Tools** - Available tools

## Updated Navigation

```
Mission Control
+-- Dashboard
+-- Task Board
+-- ?? Calendar
+-- ?? Past Memories
+-- Daily Memory
+-- Long-Term Memory
+-- ?? Docs & Artifacts
+-- ?? PRD Generator     ? NEW - PRD workflow
+-- ?? Memory Search
+-- ?? Heartbeat
+-- ??? Custom Tools
```

## Quick Start

1. Start server:
   ```powershell
   cd "C:\Users\User\.openclaw\workspace\mission-control"
   node server.js
   ```

2. Open: http://localhost:3000

3. Navigate to: PRD Generator

4. Fill in form and generate your first PRD!
