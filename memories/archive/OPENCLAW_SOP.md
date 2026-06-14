# OpenClaw — Standard Operating Procedure (SOP)

*Document ID: OPENCLAW-SOP-001
*Version: 1.0
*Effective Date: 2026-04-02
*Author: OpenClaw System
*Approved By: H (Owner)

## 1. Purpose

This document provides standard operating procedures for OpenClaw, the AI-powered content automation system used for 2 Real Enterprises and Akoma Robotics.

## 2. Scope

This SOP covers:
- Daily system operations
- Weekly content generation workflow
- Posting schedule and distribution
- Maintenance procedures
- Troubleshooting guidelines

## 3. Roles and Responsibilities

### 3.1 System Owner (H)
- Oversees both businesses remotely from London
- Reviews and approves content strategy
- Manages OpenClaw system configuration
- Has final say on brand voice and messaging

### 3.2 Content Poster (John)
- Receives pre-made content via WhatsApp
- Posts to Facebook, TikTok, Instagram, WhatsApp Status on schedule
- Responds to comments and enquiries within 4 hours
- Handles Akoma Robotics school enquiries

### 3.3 OpenClaw System
- Generates weekly content batch
- Creates images via Gemini 3 Pro Image API
- Delivers content to John via WhatsApp
- Maintains memory and performs maintenance

## 4. Daily Operations

### 4.1 Daily Posting Schedule

| Day | Brand | Content Type | Platform | Time |
|-----|-------|-------------|----------|------|
| Mon | Akoma Robotics | Educational | FB, WhatsApp | AM |
| Tue | 2 Real Enterprises | Product showcase | FB, TikTok, WhatsApp | AM |
| Wed | Akoma Robotics | Student spotlight | FB, WhatsApp | AM |
| Thu | 2 Real Enterprises | Tips/how-to | FB, WhatsApp, IG | AM |
| Fri | Akoma Robotics | Engagement | FB, WhatsApp | AM |
| Sat | 2 Real Enterprises | Taiwah + Deals | All platforms | AM |
| Sun | Both brands | Distribution | WhatsApp Groups | 10am |

### 4.2 Daily Posting Procedure (John)

1. Check WhatsApp for new content from OpenClaw
2. Verify content matches scheduled day and platform
3. Post to designated platform(s)
4. Respond to comments and enquiries within 4 hours
5. Log activity (optional - via Zobase inventory system)

### 4.3 Enquiry Response Procedure

1. Acknowledge enquiry within 4 hours
2. Provide accurate product/service information
3. Direct to appropriate channel if needed
4. Log significant enquiries for weekly review

1. Owner requests weekly batch
2. OpenClaw generates 6 posts (3 Akoma + 3 2 Real)
3. OpenClaw creates 6 images via Gemini 3 Pro
4. Content formatted with hashtags, CTAs, posting notes
5. Content sent to John via WhatsApp
6. Owner reviews and approves content

## 6. Maintenance Procedures

### 6.1 48-Hour Memory Maintenance

1. Read last 3 days of daily notes
2. Identify significant learnings and decisions
3. Update MEMORY.md (max 400 lines)
4. Update projects.md (max 80 lines)
5. Run memory_flush.py to sync vector DB

### 6.2 Workspace Audit (Weekly)

1. Check file organization
2. Verify critical files are readable
3. Clean orphaned temp and lock files
4. Verify vector-flush-tracker.json exists
5. Log audit results to daily note

## 7. Troubleshooting

### 7.1 No Content Received by John

1. Check WhatsApp connection status
2. Verify OpenClaw gateway is running
3. Check if weekly batch was generated
4. Contact H if issue persists

### 7.2 System Not Responding

1. Check if OpenClaw service is running
2. Verify gateway connectivity on :18789
3. Check memory directory is writable
4. Review daily log for error messages

## 8. Performance Metrics

| Metric | Target | Frequency |
|--------|--------|-----------|
| WhatsApp Status updates | 1+ per day | Daily |
| Facebook posts | 1 per brand day | Mon-Sat |
| Jiji listings | 5+ per week | Weekly |
| Customer response time | <4 hours | Ongoing |
| WhatsApp Group distribution | Top content shared | Sunday |
| Total quality posts | 12+ per month | Monthly |

## 9. Contact Information

| Role | Name | WhatsApp |
|------|------|----------|
| System Owner | H | +233204252252 |
| Content Poster | John | +233233352252 |

## 10. Document Control

- Document ID: OPENCLAW-SOP-001
- Version: 1.0
- Effective Date: 2026-04-02
- Next Review: 2026-05-02
- Author: OpenClaw System
- Approved By: H

---
*This SOP is maintained by OpenClaw and updated as procedures evolve.*
