# Layout and style references for "where am I" and the step workspace

Screenshots: research/benchmark/cloud-alm/*.png, research/benchmark/signavio-navigator/*.png

## 1. How SAP products show location in a process hierarchy

Three products, one pattern.

### SAP Cloud ALM (Processes app)
- Shell bar at the very top: product name, app name, search, notifications, user.
- Page header: object title ("Sell from Stock (BD9)"), object type under it ("Solution Process"),
  key facts in a row (Scope: Plant Darmstadt, Status: Design, Process owner).
- Tabs under the header: General Information, Description, Solution Value Flow, Solution Process Flow,
  Relations. The tab strip is the primary navigation inside an object.
- Solution Process Flow tab: BPMN diagram with role swimlanes, selected step highlighted, a side panel
  on the right for the selected step (Description / Applications / Configurations / Documents).
- Location above the object: Process Hierarchy is a separate tree app (screenshot 07): End-to-End
  Processes > Order-to-Cash > Order, each row with counts of attached objects as small stacked bars.
- Readiness: the Solution Process Traceability report (screenshot 18) is a list, one row per process,
  status pill plus stacked count bars per artifact type.

### SAP Signavio Process Navigator (in SAP for Me)
- Breadcrumb at top left: "SAP Signavio Process Navigator / Solution Scenario / SAP Best Practices
  for SAP S/4HANA Cloud /". Links, slash separators, current page not repeated.
- Object header: title "Project Billing - Project-Based Services (4E9)", type "Solution Process",
  key facts (Country/Region), then tabs (Diagrams, Used In, Accelerators, Description ...).
- Inside Diagrams: a segmented toggle "Solution Process Flow | Solution Value Flow", then the BPMN.
- Scenario page: two-pane master-detail. Left: a tree of Lines of Business with counts (Sales 78).
  Right: the list of solution processes in the selected node. Related Assets as tiles below.

### SAP Fiori design guidelines (the rules behind both)
- Breadcrumb: secondary navigation for drilldown, shown above the object title, links only, the
  current object is the title itself, not the last crumb. Collapses from the left when narrow.
- Object Page floorplan: header with title, subtitle (object type), key facts; anchor bar of tabs;
  sections below. This is the standard container for "one thing and everything about it".
- Process Flow control: lanes as columns for stages, nodes inside, aggregated status per lane shown
  as a coloured segment bar in the lane header. Used for document flows and approvals.

### What is standard, in one sentence
Location is shown by three stacked devices: a breadcrumb of the ancestors, an object header that
names the thing and its type, and a diagram or list that shows the thing among its siblings with the
current one highlighted. Readiness is shown as a status pill plus a count bar, never as a percentage
alone.

## 2. Recommended layout for our first screen

    Shell bar        [Tessera]  Discovery                                  search  bell  user
    Breadcrumb       Halo Beverages / Order-to-Cash / Standard sale to a retailer
    Object header    Step 2: Price the order: discounts and approvals
                     Process step  ·  Owner: Dana Ruiz (Head of Retail Sales)  ·  Readiness: In review 0 of 6
    Process flow     [1 Receive order] > [2 Price the order] > [3 Check credit] > [4 Confirm delivery] > [5 Ship] > [6 Invoice] > [7 Collect]
                      not started       IN REVIEW 0/6        not started ...
    Tabs             Configuration items (6)  ·  Interviews (1)  ·  Decision log (0)  ·  Sources (5)
    Body             the items table / evidence cards, right rail with interviews + Synthesize

Notes
- The flow is our version of the Process Flow control: seven stage boxes in a row, the current one
  emphasised with the brand border, a small readiness pill under each. No swimlanes at this level;
  swimlanes belong to the BPMN inside a step and would drown the point.
- The object header carries the readiness pill, the flow carries it per step, the shell/breadcrumb
  carries nothing about status. That matches Fiori: status lives on objects, not in navigation.
- Two-pane master-detail (Signavio) is the fallback if the flow gets crowded: left tree of steps,
  right the selected step.

## 3. Style: SAP Fiori, Horizon theme (Morning Horizon), exact tokens

Font: "72", fallback Arial, Helvetica, sans-serif. Base size 14px (0.875rem). Headings 72 Bold.
Since "72" is SAP-licensed, use the fallback stack or Inter; the feel comes from weight and density.

Colours (light theme)
    Brand / emphasised buttons / selected border   #0070F2
    Links, highlight                                #0064D9
    Text                                            #131E29
    Label / secondary text                          #556B82
    Page background                                 #F5F6F7
    Shell / header background                       #EFF1F2 (shell), #FFFFFF (page header, object header)
    Card, list, tile background                     #FFFFFF
    Borders                                         #E5E5E5 (lists), #556B81 (input fields)
    Selected row background                         #EBF8FF

Semantic (state) colours: text colour + tinted background + border
    Positive (Match)        text #256F3A   bg #F5FAE5   border #30914C
    Negative (Contradiction) text #AA0808  bg #FFEAF4   border #E90B0B
    Critical (Gaps)         text #B44F00   bg #FFF8D6   border #DD6100
    Informative (Resolved)  text #0064D9   bg #E1F4FF   border #0070F2
    Neutral (Not discussed) text #131E29   bg #EFF1F2   border #788FA6

Shape and density
    Corner radius: 0.75rem elements, 0.5rem buttons, 1rem tiles/cards.
    Flat surfaces, hairline borders, very light shadow on cards only.
    Dense: 14px body, 12px labels, rows about 40px high, generous horizontal padding (1rem).
    Status shown as a pill (rounded, tinted background, coloured text), never as a filled block.
    Object Status pattern: label on the left in grey, value on the right in text colour.

Iconography: SAP Icons are licensed; use simple line icons (Lucide) at 16px, same grey as labels.

## 4. Inspirations to steal from, and what to avoid

Steal
- Cloud ALM: header + tab strip + diagram-left, panel-right. The consultant's muscle memory.
- Signavio Navigator: breadcrumb with slashes, object type under title, segmented toggle for views,
  master-detail tree with counts.
- Fiori Process Flow: stage boxes in a row with aggregated status per stage.
- Fiori Object Status: label/value pairs in the header for owner, status, readiness.

Avoid
- Full BPMN swimlanes on the landing screen. The seven-step strip is enough to locate; the BPMN
  can live behind a "View diagram" link.
- Progress rings and percentages as the only readiness signal. Use "0 of 6" plus a pill.
- Consumer-app gloss: large hero areas, gradients, big rounded cards with heavy shadows.
- Dark mode for the demo. Morning Horizon is what consultants see all day.
