# Frontend design: the discovery workspace

## Terms
BPMN = Business Process Model and Notation, the standard flowchart notation SAP tools use: boxes for
steps, arrows, horizontal "swimlanes" per role. We borrow the idea (a diagram locates you) but not the
notation. Our diagrams are simple boxes and lines in line-art.

## Navigation is a map you zoom into (one page, three levels)

Level 1, the enterprise map. Halo's end-to-end processes drawn as a row of thin outlined tiles:
    Order-to-Cash · Procure-to-Pay · Record-to-Report · Plan-to-Produce · Hire-to-Retire
Order-to-Cash is in scope for this project and drawn solid; the others are dotted "not in scope".
Each in-scope tile carries a readiness figure (steps in review / total).

Level 2, the process flow. Clicking Order-to-Cash expands it in place into the seven steps as a
left-to-right flow of outlined boxes connected by thin lines, with a readiness pill under each
(not started / in review 2 of 6 / ready). Step 2 is drawn with a solid border and a soft fill.

Level 3, the step. Clicking Step 2 does NOT open a new page. The map collapses upward into a compact
strip (five process chips, then seven step chips, Step 2 highlighted) and the step workspace slides
in below. The strip is always visible, so the user never loses where they are. Clicking any chip in
the strip zooms back out.

The strip replaces the breadcrumb. It is the breadcrumb, drawn as a diagram.

## The step workspace (Level 3 layout)

    ┌──────────────────────────────────────────────────────────┬────────────────────────┐
    │ strip: [O2C] [P2P] [R2R] ...  >  [1][2][3][4][5][6][7]    │                        │
    │ Step 2  Price the order: discounts and approvals          │   AGENT (right rail)   │
    │ Owner Dana Ruiz · Readiness 0 of 6 · Sources 5            │                        │
    ├──────────────────────────────────────────────────────────┤   drop transcript      │
    │ Configuration items (6)                                   │   ─────────────────    │
    │ ┌ item row: name · what the system does · verdict · ▸ ┐   │   chat thread          │
    │ │ expanded: quote · measured fact · reasoning         │   │   (agent status,       │
    │ │ Needs your judgment → My reason [text] [Save]       │   │    triage summary,     │
    │ └────────────────────────────────────────────────────┘   │    user questions)     │
    │ ... six rows                                              │                        │
    │ Decision log (below the table, grows as reasons are saved)│   [ask about item F2]  │
    └──────────────────────────────────────────────────────────┴────────────────────────┘

Left, main: a table of the six items. Collapsed row = name, plain description, verdict pill.
Expanded row = evidence (Dana's quote with timestamp, the measured fact, one line of reasoning), the
"Needs your judgment" block, and the "My reason" field with Save. Saving flips the verdict to
Resolved and appends to the decision log under the table.

Right, agent rail (fixed, ~360px):
- Top: drop zone "Drop an interview transcript" with the one available transcript as a chip.
- Below: a chat thread. The agent speaks first when a transcript is dropped: working status lines,
  then a summary ("Checked 6 items: 2 match, 1 contradiction, 2 gaps, 1 not discussed. 4 need you.")
  with links that scroll to the rows. The table recolours as the summary arrives.
- The user types questions. Selecting a row in the table scopes the chat to that item (a small
  "About: F2 Approval threshold" chip appears above the input; click × to unscope).
- The agent can draft a reason; a "Use as my reason" button drops the draft into that row's field.
  The user still edits and saves. The agent never saves.

## Style: Tessera's language, not SAP's

From tesseralabs.ai (measured): typeface GT Planar (licensed), text #09090B, secondary #52525B,
white background, tight letter-spacing (about -0.04em on display, -0.02em on body), weights 400/600,
black pill buttons with white text, small uppercase eyebrow labels, line-art diagrams with 1px strokes,
a faint dot grid behind hero areas, big outlined numerals as section markers.

Ours:
- Type: Inter (free, close in feel), same tightening. Display 28-32px 600, body 14-15px 400,
  labels 11px uppercase with 0.08em tracking in #52525B. Monospace (JetBrains Mono) for ids,
  system values and table names, which nods to their "WORKFLOW 1" tag.
- Surfaces: white. Hairline borders #E4E4E7. No shadows. Dot grid only behind the map.
- Diagrams: outlined boxes, 1px #09090B strokes, dotted strokes for out-of-scope, thin arrows.
- Buttons: primary black pill; secondary outlined pill.
- The four verdicts stay recognisable but muted, ink on tint:
    Match            #166534 on #ECFDF3
    Contradiction    #991B1B on #FEF2F2
    Gap (both)       #9A3412 on #FFF7ED
    Resolved         #1E40AF on #EFF6FF
    Not discussed    #52525B on #F4F4F5
- Density: calmer than SAP. Rows ~56px, one idea per row, evidence only on expand.

## What stays from the SAP research
The information architecture (process > step > configuration item), the idea that a diagram locates
you, readiness as "n of m" plus a pill, evidence in a side rail. Nothing of SAP's chrome or density.

## Build note
Static single HTML file. Level 1 and 2 are drawn with SVG/CSS. Synthesize plays the saved agent
output with timed status lines. Chat answers come from a prepared script per item (two or three
Q&A pairs each) plus a generic fallback; a live build would swap in the model.
