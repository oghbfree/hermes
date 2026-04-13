# SKILL: Ghana Supplier Response Analyst

## DESCRIPTION
Executed every Monday at 10:00 AM Accra Time. This skill reviews the raw data and messages collected in the supplier research file to perform a comparative analysis of prices, technical capabilities (conversions), and stock availability.

## CAPABILITIES
- Comparative Market Analysis
- Technical Feasibility Assessment (Steering/Dashboard)
- Procurement Recommendation Engine

## WORKFLOW

### 1. Data Ingestion
Read `GHANA_SUPPLIER_RESEARCH.md`. 
- Identify all entries with status "Response Received" or "Contacted" within the last 7 days.
- Look for pricing data, stock levels, and notes regarding "Steering Conversion" or "Dashboard Change."

### 2. Analytical Processing
For each supplier with new data, evaluate:
- **Price Competitiveness**: Compare against known market averages for Ghana.
- **Technical Scope**: Can they handle both steering conversion and dashboard hardware changes?
- **Urgency/Stock**: Who can deliver immediately vs. long lead times?

### 3. Documentation
Create a new file: `memory/procurement/GHANA_SUPPLIER_ANALYSIS_$(date +%Y-%m-%d).md` using this exact table format:

| Supplier Name | Price | Stock | Lead Time | Quality | Steering Conv. | Dash Change | Recommendation | Next Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [Name] | [GHS] | [Qty] | [Days] | [1-5] | [Yes/No] | [Yes/No] | [Buy/Hold/Avoid] | [e.g., Call John] |

### 4. Strategic Recommendation
At the bottom of the file, provide a "Top Pick" for the week based on the "Cruncher" agent logic (best value + highest reliability).

### 5. Notification
Post the table (or a summary of the Top 2 options) to Telegram Topic 2. 
**Note:** Ensure currency is displayed in GHS.

## GUIDELINES
- **Agent Persona**: Cruncher (Data-driven, precise, cynical of bad deals).
- **Timezone Awareness**: All timestamps must reflect Accra Time (GMT+0).
- **Quality Check**: If a supplier hasn't provided a price, mark as "DATA MISSING" and list as the "Next Action" to follow up.