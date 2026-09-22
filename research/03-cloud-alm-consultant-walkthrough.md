# SAP Cloud ALM: what it is, and a consultant's Discover/Explore walkthrough

## What it is

SAP Cloud ALM (Application Lifecycle Management) is SAP's free, cloud-hosted project tool for
implementing and running SAP software. It is included with every SAP cloud subscription and with
Enterprise Support, so almost every SAP customer has it. It replaces SAP Solution Manager for
new projects. It is not the ERP. It sits next to the ERP and holds the project: scope, process
diagrams, requirements, tasks, tests, deployments, and later monitoring.

Two halves:
- Implementation: projects, scopes, processes, fit-to-standard workshops, requirements, user stories, tests, transports.
- Operations: monitoring of the live system after go-live.

Who uses it:
- The implementation project team: partner consultants (functional consultants per module, project manager) and the customer's IT project team. These are the daily users.
- Business process owners and key users on the customer side: given access to review diagrams and approve requirements. They rarely live in it.
- Business users being interviewed: normally never see it.

## Reading the two screenshots

Screenshot 17 (Processes app, Solution Process Flow tab)
- The diagram is not the ERP. It is the BPMN diagram of the SAP Best Practice process "Sell from Stock (BD9)".
- BD9 is SAP's standard name for order-to-cash. Screenshot 15 shows the full diagram: swimlanes for Internal Sales Representative, Sales Manager, Shipping Specialist, Billing Clerk, Accounts Receivable Accountant; steps Create Sales Order, Credit Management (set credit / review blocked orders), Advanced ATP, Approval Workflow, Create Delivery, Execute Picking, Check Batches, Post Goods Issue, Proof of Delivery, Create Billing Document, Accounts Receivable. So "our order-to-cash flow" and "BD9" are the same object.
- Screenshot 07 confirms the hierarchy above it: a Process Hierarchy node "Order-to-Cash" with 11 solution processes under it.
- The right panel belongs to the selected step ("Inform Accountant", a custom step the consultant added). Tabs: Description, Applications (the Fiori app or transaction used), Configurations (a library entry naming the relevant config), Documents. The Create button makes a Requirement attached to this step. This panel is where a consultant types during a workshop.

Screenshot 18 (Analytics app, Solution Process Traceability)
- One row per solution process, not per task. "Copy of Sell from Stock (BD9)" for scope "Plant Darmstadt", status Realization.
- Each stacked bar counts artifacts attached to that process by status: Requirements, User Stories, Project Tasks, Documents, Test Preparation, Test Execution, Defects.
- It answers "how much delivery work is attached to this process and how far along is it". It does not answer "how well do we understand this process".

## Is it the benchmark?

Yes, for two things:
1. The mental model and screen layout every SAP consultant already knows (hierarchy > process > diagram > step > configurations, diagram left, step panel right).
2. The direct competitor for the transcript step: Joule in Cloud ALM turns a pasted workshop transcript into one requirement per click, given a title.

With one honest caveat that strengthens the pitch:
- Cloud ALM's fit-to-standard flow is designed for greenfield and cloud projects: demo the SAP standard, capture deltas from it. SAP's own guidance says "Avoid documenting requirements as 'as-is'. The status quo is not your friend."
- For a brownfield conversion of an existing ERP, SAP's guidance is: run Readiness Check and the Simplification Item check, and focus workshops on the items that change. There is no tooling for "explain why the existing configuration is what it is". That job lives in Solution Manager documents (if any), in Excel, and in the consultant's head. Cloud ALM plans to add "Solution Documentation" in 2026.
- So: for the style and vocabulary, benchmark Cloud ALM. For the reconciliation job itself, there is no incumbent tool. That is the product's opening.

## Walkthrough: I am the consultant, order-to-cash, Discover and Explore

### A. Before any interview (Prepare, early Explore)

1. Projects and Setup: create the project, pick the SAP Activate roadmap (system conversion, or new implementation), set phases and sprints.
2. Manage Scopes: create scopes, e.g. "Sales EMEA", "Plant Darmstadt".
3. Processes: scope "Sell from Stock (BD9)" into "Sales EMEA". Set status Design. Assign the process owner (customer side, e.g. Head of Order Management).
4. Process Hierarchy: confirm BD9 sits under "Order-to-Cash" so the workshop schedule and reporting roll up.
5. Prepare the evidence I will bring:
   - Read the BD9 test script and diagram so I can demo it.
   - Pull the client's actual configuration for the steps in scope: SE16 on the customizing tables, or an SPRO walk with the basis team. Readiness Check and Simplification Item list for what changes in S/4HANA. This lands in a spreadsheet or Word doc. Cloud ALM has no place for the values.
   - Write my question list per step ("L3 questions": the detailed configuration questions a step needs answered).
6. Schedule the workshop or interview against the hierarchy node, invite the process owner and the subject matter experts (sales manager, order desk lead, credit controller, AR lead).

### B. The interview with the sales manager

Usual format: a two-hour workshop on the steps that belong to Sales (Create Sales Order, Credit Management, Approval Workflow, ATP), or a one-hour one-on-one if the process owner prefers. Two consultants if the partner can afford it: one drives, one documents.

1. Open Processes, BD9, Solution Process Flow. Walk the diagram step by step, and demo each step in the sandbox system.
2. Per step, ask: is this how you do it today, what is different, why, who decides, what exceptions exist. This is where the business reasons come out, verbally.
3. The documenting consultant clicks the step, opens the side panel, and creates Requirements as they are identified. Each is freeform text, tagged FIT / GAP / WRICEF, with a priority. Notes go into the requirement description or a Document.
4. Configuration values the client confirms (credit limit rules, payment terms, approval thresholds) go into the consultant's spreadsheet or a template, not into Cloud ALM as values.
5. Recording: if the call is recorded, the transcript is saved after the session.

### C. After the interview

1. Paste the transcript into a new Document in Cloud ALM, link it to BD9.
2. Optionally use Joule: for each requirement I already know exists, click Generate, type its title, pick BD9, attach the transcript, review the filled template, save. One at a time.
3. Reconcile by hand: re-read the minutes against my config spreadsheet and my memory of the IMG. Where the sales manager's description differs from the config, write it up as a requirement, a Key Design Decision, or an open question in the issues log. Where config exists that nobody mentioned, nothing prompts me. I only catch it if I notice.
4. Create follow-up Project Tasks: "Ask credit controller why the review-date check is active", assign, due date.
5. Update the process status when the design is agreed; the process owner reviews and approves requirements.
6. Analytics: the traceability report shows the project manager how many requirements and tasks are attached to BD9 and their status.

### D. Closing Explore

- Design is agreed per process, requirements prioritized into the backlog, process owner signs off, quality gate closes the phase. Realize begins.

## Where our agent slots in

Between C.1 and C.3. Today the transcript becomes a Document and the consultant does the comparison in their head. Our agent reads the transcript plus the configuration values the consultant already pulled in A.5, and produces per configuration field: state (match / contradiction / gap without data / gap without reason / not covered), quote, confidence, follow-up question and who to ask. The consultant reviews and resolves, and the step's coverage updates. The follow-up questions become the C.4 tasks automatically.

Sources: see 02-benchmark-existing-tools.md, plus
- SAP Cloud ALM overview: https://support.sap.com/en/alm/sap-cloud-alm.html
- Fit-to-standard for brownfield conversions (SAP Community Q&A): https://community.sap.com/t5/enterprise-resource-planning-q-a/fit-to-standard-process-for-on-premise-for-system-conversion-brownfield/qaq-p/12477585
- Capturing delta requirements in fit-to-standard workshops (SAP, Jan 2025): https://community.sap.com/t5/business-transformation-blog-posts/capturing-delta-requirements-a-guide-to-fit-to-standard-workshops/ba-p/13994533
- SAP Activate Explore phase (SAP, 2017): https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/sap-activate-explore-phase-use-fit-to-standard-to-confirm-business-process/ba-p/13331140
- Readiness Check in Cloud ALM for conversions: https://learning.sap.com/courses/implementing-with-sap-cloud-alm/running-your-sap-s-4hana-conversion-project-with-readiness-check-1
