# Benchmark: tools consultants use today in Discover and Explore (order-to-cash)

Purpose: know the style, mental model and workflow of the incumbent tools so the prototype
reads as a plausible next step for an SAP consultant, and so the innovation is sharp.

Screenshots: `benchmark/cloud-alm/*.png` (from SAP's own end-to-end guide, Dec 2025).
Key ones: 13 (Processes list), 16 (Process Authoring, BPMN), 17 (Solution Activity side panel),
18 (Solution Process Traceability report).

---

## 1. The landscape in one table

| Tool | Who uses it | What it holds | How the "reason" side is captured | How the "system data" side is captured | Reconciliation? |
|---|---|---|---|---|---|
| **SAP Cloud ALM** (the current SAP standard for Activate projects) | Consultant, project lead; business users read | Process hierarchy, solution processes (BPMN), solution activities (steps), configurations, requirements, user stories, documents, test cases | Requirements typed by the consultant during the workshop, attached to a process step; meeting transcripts pasted as Documents; since Dec 2025 Joule can generate a requirement from a transcript | Configuration library entries attached to a step (name and category only, not the values); no read of live customizing | No. Requirements are freeform text. Nothing compares a claim to a config value. Status per process is Design / Realization / Production |
| **SAP Solution Manager 7.2** (what brownfield ECC customers already have) | Consultant, basis | Solution documentation: Scenario > Process > Step, with executables (transactions), config objects, documents | Documents uploaded per step (Word blueprints, KDD docs) | Executables and config objects linked per step; Business Process Monitoring reads live data | No. It is a filing cabinet with links |
| **SAP Signavio** (Process Manager, Collaboration Hub, Process Insights) | Process analysts author; business users comment | BPMN models, as-is mined from document tables (Process Insights), comments and approvals per diagram | Comments on diagrams in the Collaboration Hub; process owner approval workflow; read confirmations | Process mining over system tables shows the actual flow and variants | Partial. Mined as-is vs modelled to-be diagrams can be compared visually. Nothing at config-field level, nothing tied to what a person said |
| **Excel / PowerPoint / Word** (the real workhorse) | Everyone | BPML, fit-gap matrix, WRICEF register, KDD log, issues log, workshop minutes, blueprint | Minutes and KDD log, written after the session | SE16 exports pasted into sheets | Done in the consultant's head; recorded as rows in the fit-gap matrix |
| **Jira / Confluence** | Delivery team | Requirements backlog, decision pages | Confluence pages, Jira comments | none | No |
| **Tricentis LiveCompare, SAP Readiness Check, ATC** | Technical consultant | Usage stats, custom code inventory, simplification items, change impact | none | Reads the system directly | No; technical only, no business reasons |
| **Big-4 platforms** (Deloitte Ascend and DMAP, Accenture myConcerto) | Consultancy delivery teams | Accelerators, templates, diagnostics, landscape visibility, AI remediation of code | Templates for workshops | Automated diagnostics of the ECC landscape | Not visible publicly; positioned as speed and visibility, not as evidence reconciliation |
| **Joule for Consultants** | Consultant | Q&A over SAP documentation (9 TB of gated content) | n/a | n/a | No; it answers "what does SAP standard do", not "what does this client's system do and why" |

---

## 2. SAP Cloud ALM in detail (the primary benchmark)

**Mental model** (this is what consultants are trained on, and what the prototype should feel native to)

    Project
      └ Scope (e.g. "Plant Darmstadt", "Finance Germany")
          └ Solution Process (e.g. "Sell from Stock (BD9)")     status: Design / Realization / Production
              ├ Solution Value Flow (high-level business view)
              └ Solution Process Flow (BPMN diagram)
                  └ Solution Activity (a process step, e.g. "Check Batches", "Inform Accountant")
                      ├ Applications (Fiori apps / transactions)
                      ├ Configurations (config library entries)
                      ├ Documents
                      ├ Requirements  <- created from the step during the workshop
                      └ Test cases

**The workshop screen** (screenshot 17): BPMN diagram on the left, selected step highlighted, side panel on the right with tabs Description / Applications / Configurations / Documents and a Create button for Requirements. Swimlanes by role. Blue, flat SAP Fiori styling. Two consultants recommended per workshop: one drives the demo, one types requirements into this panel.

**Progress tracking** (screenshot 18): Solution Process Traceability report. One row per solution process with stacked bars counting requirements, user stories, tasks, documents, tests by status. Progress is counted in objects created, not in understanding gained.

**Requirements**: freeform text against a customer template (Context, Situation, Detailed requirement, Proposed solution with type Report / Interface / Configuration / Enhancement / Form / Workflow, Acceptance criteria). Tagged with keywords like FIT, GAP, WRICEF. Status flows to "In realization".

**AI-assisted requirement generation (Joule, GA Dec 2025)**: paste the workshop transcript as a Document, click Generate on a new requirement, give it a title, pick the template, scope and solution process (the process diagram is part of the prompt), attach the transcript, optionally SAP help docs. The LLM fills the template. Constraints stated by SAP: one requirement per generation, the consultant must already know the requirement title, review is manual, tokens are paid. First community question was whether it could find all the requirements in a transcript by itself. It cannot. SAP claims up to 50% less time writing requirements.

**What Cloud ALM does not do**

- It never reads the client's actual customizing values. "Configurations" is a library of names.
- It never compares what a person said to what the system does.
- It has no notion of evidence, confidence, or an open question per configuration field.
- Progress is a count of artifacts, not coverage of explained configuration.
- Interviewees and process owners see nothing until they are given Cloud ALM access and go looking.

---

## 3. Where the incumbent workflow leaves the consultant alone

1. After a workshop, the consultant re-reads minutes and mentally checks them against SE16 exports or their memory of the IMG. Nothing prompts "the sales manager said X, but T691F says Y".
2. Gaps of the second kind (config exists, nobody mentioned it) are invisible. No tool lists config entries that have never been discussed.
3. "How far along is discovery?" is answered by counting requirements or by gut feel.
4. Follow-up questions live in an issues log spreadsheet, not attached to the config they concern.
5. The process owner sees the blueprint at sign-off.

---

## 4. Design implications for the prototype

**Borrow, so it reads as native**

- Use the Cloud ALM hierarchy and vocabulary: Solution Process > Process Flow > Solution Activity > Configuration. Our "node" is a Solution Activity with its Configurations expanded to field level.
- Use the same layout: flow diagram left, selected step's detail panel right. That is the screen every SAP consultant already knows.
- Use flat, light, information-dense styling. No consumer-app gloss.

**Change, so the innovation is visible on the same screen**

- The side panel gets a new tab: **Evidence**. For each configuration field: system value, what people said (quote, who, when), state (Match / Contradiction / Gap: reason without data / Gap: data without reason / Not covered), confidence, suggested follow-up and who to ask.
- Steps in the diagram are colored by evidence state instead of by artifact count.
- The traceability report becomes a **coverage** report: fields explained / fields total per step, open contradictions, open gaps, and a "ready for sign-off" flag per process.
- Interview transcript is an input, not a document to file. The agent reads it and updates the Evidence tab; the consultant reviews and resolves.

**The demo contrast, in one sentence**
Cloud ALM plus Joule turns a transcript into a well-formatted requirement the consultant asked for. Our agent turns the transcript into a verdict per configuration field the consultant did not know to ask about.

---

## 5. Sources

- Cloud ALM end-to-end process management guide (Dec 2025, screenshots): https://community.sap.com/t5/technology-blog-posts-by-sap/end-to-end-guide-for-process-management-in-sap-cloud-alm-for-implementation/ba-p/14287142
- Cloud ALM AI-assisted requirement generation (Dec 2025): https://community.sap.com/t5/technology-blog-posts-by-sap/ai-goes-calm-ai-assisted-requirement-generation/ba-p/14294426
- SAP Business AI release highlights Q4 2025 (time-saving claims): https://news.sap.com/2026/01/sap-business-ai-release-highlights-q4-2025/
- Cloud ALM fit-to-standard workshop guidance: https://support.sap.com/en/alm/sap-cloud-alm/implementation.html , https://www.blue.works/en/from-process-scope-to-requirements-backlog-with-sap-cloud-alm-2/
- Solution Manager 7.2 solution documentation: https://help.sap.com/docs/SUPPORT_CONTENT/sm/3518046721.html , https://blogs.sap.com/2019/11/17/building-up-end-to-end-processes-in-sap-solution-manager-7.2/
- Signavio in S/4HANA transformation and Collaboration Hub: https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/drive-process-centric-sap-s-4hana-transformation-with-sap-signavio/ba-p/14115285 , https://www.signavio.com/products/collaboration-hub/ , https://learning.sap.com/courses/managing-business-processes-with-sap-signavio-solutions/collaborate-on-processes-in-the-hub_e28c4d24-1f1c-458e-9d77-fe1b1e1bc93d
- BPML and fit-gap templates: https://flevy.com/browse/marketplace/business-process-master-list-bpml-template-80 , https://noeldcosta.com/best-sap-implementation-templates-activate-2024/
- Jira in SAP projects: https://community.sap.com/t5/technology-blog-posts-by-members/how-to-build-clarity-in-sap-projects-with-jira/ba-p/14257145
- Tricentis LiveCompare: https://www.tricentis.com/products/impact-analysis-livecompare
- Deloitte SAP modernization / DMAP: https://www.deloitte.com/global/en/alliances/sap/about/sap-modernization.html ; Accenture myConcerto: https://www.accenture.com/us-en/services/sap/myconcerto-sap-integration
- Joule for Consultants: https://www.saptutorials.in/sap-joule-and-agentic
