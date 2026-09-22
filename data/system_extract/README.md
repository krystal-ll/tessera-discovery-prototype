# System extract (detailed SAP-style version, kept for reference)

The prototype now reads the simplified database in `data/db/` (people, product, discount, connections)
plus the process-mining metrics below. The SAP-style files here are the fuller version of the same facts.

# Original notes

These files mimic what a consultant pulls from the client's ERP before a pricing workshop.
Column names follow the SAP tables they came from so an SAP person recognises them; the
`plain` columns are the consultant's own annotation.

| File | What it is | SAP source |
|---|---|---|
| pricing_procedure_ZHALO01.csv | The calculation steps the system runs on every sales order line, in order | T683S (pricing procedure steps), T685 (condition types) |
| condition_records.csv | The actual rates on file: who gets what discount, valid from/to, who created it | KONP / A-tables (condition records) |
| process_mining_o2c_metrics.csv | Measured facts about how orders actually behave over 12 months: standard order-to-cash metrics plus drill-downs the consultant defined for this node | SAP Signavio Process Intelligence, O2C accelerator on ECC (event log from VBAK/VBAP/CDHDR/KONV) |
| readiness_check_summary.csv | What the conversion scan says about this area: what changes in S/4HANA, custom code that needs work, which transactions people actually use and how often | SAP Readiness Check for S/4HANA conversion |
| order_controls.csv | Non-pricing switches on the pricing step: approval block, manual limits, free goods | T685 upper/lower limits, user exit MV45AFZZ, KONP free goods (NA00) |

Everything in these files is fictional.

## A note on what the free tools give you

SAP's free Process Insights discovery edition reports throughput, backlog and exception indicators
for sales documents (documents created, document type usage, incomplete items, rejected items). It
has no pricing indicators at all. The pricing facts in process_mining_o2c_metrics.csv (M-03, M-08 to
M-14) need the full Process Intelligence edition, which has a standard "price change rate" metric and
lets the consultant define drill-downs over the order event log. Rows are labelled by which one they
come from. In a real project the consultant would either have the full edition through the partner,
or pull the same numbers with SQL over the order tables. Either way the numbers arrive as a table.
