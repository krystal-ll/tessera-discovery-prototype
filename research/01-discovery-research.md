# Discovery research: how SAP consultants reconcile system data with client reasons

Purpose: ground the prototype's mock data and agent logic in how discovery actually runs
for a brownfield SAP ECC to S/4HANA migration. One sprint = one interview reconciled
against one node of the ERP model.

---

## 1. How discovery runs today (SAP Activate, brownfield)

Phases: Discover -> Prepare -> Explore -> Realize -> Deploy -> Run.
The work we care about sits in Discover and Explore.

**Two evidence streams the consultant has to hold together**

| Stream | Where it comes from | What it looks like |
|---|---|---|
| System data ("what the system does") | Customizing tables read via SE16 / SPRO (IMG tree); SAP Readiness Check; custom code inventory (ATC); transaction usage stats (ST03N); Signavio Process Insights (process mining over document tables) | Rows in config tables keyed by org unit + object type. Example: T691F row = (credit control area, risk category, credit group) -> check type, reaction, block flag, horizon |
| Client reasons ("why it does that") | Fit-to-standard workshops, 1:1 interviews with process owners and key users, questionnaires, legacy Business Blueprint / Business Process Design Document / Key Design Decision (KDD) log / Configuration Rationale doc if they exist | Narrative. Often stale, incomplete, or held only in people's heads. Interviews describe the *intended* process; system data shows the *actual* one |

**Artifacts the consultant maintains by hand to reconcile the two**

- Business Process Master List (BPML): one row per process step, columns for scope, owner, status.
- Fit-gap matrix: per requirement, fit / partial fit / gap.
- WRICEF register: every custom object (workflows, reports, interfaces, conversions, enhancements, forms) with owner and effort.
- KDD log: each design decision, the options, the choice, who approved.
- Issues / open-questions log ("parking lot"): what to ask whom next.
- Sign-off: one business process owner per module approves the process design before Realize.

**Where the pain is**

- Brownfield systems have hundreds of Z objects and config entries that nobody can explain. The people who set them up left.
- The consultant is the only integration point between the two streams. Progress lives in a spreadsheet and their head.
- Process owners see the picture only at blueprint sign-off, late.

---

## 2. Mapping the seven product pieces to what consultants do today

| Piece | Today | Artifact today |
|---|---|---|
| 1 ERP model seed | Consultant walks the IMG tree and BPML, pulls config tables | BPML rows, SE16 exports, Readiness Check |
| 2 Interview intake | Consultant takes notes in a workshop, writes minutes after | Workshop minutes, questionnaire answers |
| 3 Reconciliation | Consultant compares minutes to config from memory or by re-reading exports | Fit-gap matrix, KDD log |
| 4 Progress tracking | Column in BPML / spreadsheet, updated by hand | BPML status column |
| 5 Consultant resolution | Consultant decides, records in KDD or issues log, emails follow-ups | KDD, issues log |
| 6 Stakeholder views | Minutes emailed to interviewees; process owner sees blueprint at the end | Email, blueprint draft |
| 7 Sign-off trigger and report | Consultant judges when done, writes blueprint / process design doc | Business Blueprint, sign-off form |

Piece 3 is the one where the consultant is doing cognitive work with no tool support. That is the prototype.

---

## 3. What a "node" is, and the granularity of its data

Recommendation: a node is one **configuration object** within a process step, with a small set of
**fields** that each carry a system value and need a business reason. Nodes group under process
steps; steps chain into the process (order-to-cash). Triage happens per field, then rolls up to the node.

Why field level: an interview rarely explains a whole object at once. The sales manager explains
the reaction (block vs warn) and never mentions the horizon. Field-level state is what lets the
tracker say "this node is 60% explained" instead of guessing.

### Demo node: automatic credit check at sales order

Chosen because it is a real, well-known SAP config with obvious business reasons, and every
state (match, contradiction, both gap types) arises naturally in a sales-manager interview.

**Process step:** Order-to-cash, step 2, "Credit check" (between sales order creation and availability check).

**Configuration objects behind it**

| Object | Transaction | Table | Fields we will mock |
|---|---|---|---|
| Credit control area | OB45 | T014 | CCA id, currency, update group (12) |
| Risk category | OB01 | T691A | id, description (001 low, 002 medium, 003 high / new) |
| Credit group assignment to sales doc type | OVAK | TVAK | doc type OR -> credit group 01 (order) |
| Credit group assignment to delivery type | OVAD | TVLK | delivery type LF -> credit group 02 (delivery) or blank |
| Automatic credit control | OVA8 | T691F | keyed by (CCA, risk category, credit group). Fields: check type static/dynamic; horizon months; reaction A warning / B error / C warning + set status / D error + set status; status block flag; open items % and days; oldest open item days; max dunning level; released docs unchecked days; next review date check |
| Customer credit master | FD32 (ECC) / UKM_BP (S/4) | KNKK | per payer: credit limit, risk category, credit rep group |

**Realistic system data for the mock (one T691F row per risk category)**

| CCA | Risk cat | Credit grp | Check | Horizon | Reaction | Block | Oldest open item | Max dunning lvl |
|---|---|---|---|---|---|---|---|---|
| 1000 | 001 low (key accounts) | 01 order | dynamic | 2 months | A warning | no | 60 days | 3 |
| 1000 | 002 medium | 01 order | dynamic | 2 months | C warning + status | yes | 30 days | 2 |
| 1000 | 003 high / new | 01 order | static | n/a | D error + status | yes | 14 days | 1 |
| 1000 | 003 high / new | 02 delivery | static | n/a | D error + status | yes | 14 days | 1 |

Plus: delivery type LF assigned credit group 02 (so risk 003 is re-checked at delivery), and
a next-review-date check switched on for risk 002 with no documentation anywhere.

**How the interview will land on those fields**

| Field | What the sales manager says | State |
|---|---|---|
| Reaction for key accounts = warning only | "For our top accounts we never block, the rep just gets a warning and calls finance" | Match |
| Reaction for new customers = hard block | "New customers are blocked over limit, no exceptions" | Match |
| Re-check at delivery for risk 003 | "We only check credit when the order is created" | Contradiction: system re-checks at delivery for high risk |
| Intercompany orders skip the check | "Intercompany orders never go through credit check" | Gap, reason without data: no config exempts them; likely done by manual release in VKM1 |
| Next review date check on risk 002 | not mentioned | Gap, data without reason: field is active, nobody has explained it |
| Horizon 2 months | not mentioned | Not covered: neither match nor gap yet, needs a follow-up with finance |

The last row matters: "not covered" is different from "gap". A gap is when one side is missing
after the interview has touched the topic. Not covered means the interview never went there.
The tracker needs both or it over-reports gaps.

---

## 4. Agent logic for one sprint (one interview -> one node)

Inputs
- Node record: process step, config objects, fields, each with system value and current state.
- Interview transcript with speaker, role, date.
- Optional: legacy documentation excerpt (stale blueprint) as a third evidence source.

Step 1, synthesize
- Extract every claim in the transcript that concerns this node.
- Attach each claim to a specific field, with the verbatim quote and the speaker.

Step 2, triage per field
- Match: claim and system value agree.
- Contradiction: claim and system value disagree.
- Gap, reason without data: claim describes behaviour no config produces.
- Gap, data without reason: config exists, transcript does not explain it (only after the topic was raised).
- Not covered: transcript never touched the field.

Step 3, feed back to the consultant
- Per field: state, evidence quote, confidence, one suggested follow-up question and who should answer it.
- Per node: rolled-up coverage (fields explained / total) and the list of open items.

Step 4, consultant resolves
- Consultant accepts, overrides, or records a decision per open field (this is the KDD entry).
- Node state recomputes. When every field is explained or decided, the node is closed.

Step 5, repeat
- Next interview (e.g. accounts receivable lead) runs the same loop on the same node and picks up
  the open items. When every node in the process is closed, the agent says it is time to draft the
  process design document and take it to the process owner for sign-off.

---

## 5. Mock data to produce

- `data/erp_model.json`: order-to-cash with 8 steps listed, and the credit-check node fully populated at field level (other steps are placeholders so the tracker has a denominator).
- `data/interviews/01-sales-manager.md`: 15 to 20 minute transcript, contains the six landings in section 3.
- `data/interviews/02-ar-lead.md`: second cycle, answers the follow-ups from cycle one, opens one new contradiction.
- `data/legacy/blueprint-excerpt-2014.md` (optional): stale rationale for credit management, wrong on one point, to show the agent weighing a doc against a person.

---

## 6. Sources

- SAP Activate Explore phase and fit-to-standard: https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/sap-activate-explore-phase-use-fit-to-standard-to-confirm-business-process/ba-p/13331140 , https://learning.sap.com/courses/implementing-sap-s-4hana-cloud-public-edition/conducting-fit-to-standard-workshops , https://www.leanix.net/en/wiki/tech-transformation/sap-activate-explore-phase-activities
- Business Blueprint structure and sign-off: https://www.guru99.com/sap-business-blueprint.html
- Configuration rationale and KDD templates: https://www.coursehero.com/file/89804814/SAP-Configuration-Rationale-Templatedoc/ , https://noeldcosta.com/best-sap-implementation-templates-activate-2024/
- Brownfield discovery pain (undocumented Z objects, tribal knowledge): https://www.resulting-it.com/erp-insights-blog/how-to-reduce-sap-technical-debt-in-a-brownfield-s/4hana-migration , https://www.basistechnologies.com/blog/a-quick-guide-to-sap-s-4hana-transformation-brownfield-implementation
- Process mining vs interviews (intended vs actual process): https://www.signavio.com/wiki/process-discovery/process-mining/ , https://community.sap.com/t5/technology-blog-posts-by-sap/unlocking-the-next-steps-of-sap-signavio-process-insights-discovery-edition/ba-p/13950075
- Credit management configuration (OVA8, T691F, credit groups, risk categories): http://sap-f2.blogspot.com/2009/08/step-by-step-credit-management.html , https://www.sapdatasheet.org/abap/tabl/t691f.html , https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-members/key-learnings-on-credit-management/ba-p/13236782
- Customizing tables for order-to-cash (TVAK, TVLK, TVFK): https://beyondse16.com/2020/04/16/sap-customizing-tables-related-to-table-tvak-sales-document-types/ , https://www.se63.info/important-customizing-tables/
- Tessera Labs: https://www.tesseralabs.ai/product , https://erp.today/erp-modernization-ai-tessera-labs-funding/ , https://techfundingnews.com/tessera-labs-60m-series-a-a16z-erp-sap-migration-ai/
