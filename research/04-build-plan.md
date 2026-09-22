# Build plan: one cycle, one task (3 hours)

## The user journey we are building

Persona: SAP functional consultant, Explore phase, brownfield order-to-cash.
Task in Cloud ALM terms: the "Credit Management" step of Sell from Stock (BD9).

| Step | What the consultant sees | What the agent does |
|---|---|---|
| 0. Before | The credit management step, six configuration fields, all grey "Not discussed". Coverage 0 of 6. | nothing |
| 1. Drop the transcript | Picks "Interview: Sales Manager, 18 Sep 2026" (or pastes text). Clicks Synthesize. | Reads transcript, ties every claim to a field |
| 2. Triage lands | Each field gets a state, a quote, who said it, confidence. Steps in the diagram recolour. Coverage moves. | Classifies each field: Match / Contradiction / No data behind it / No one explained it / Not discussed |
| 3. Call-out | Fields in Contradiction or either Gap show a "Needs your judgment" card: the conflict in one sentence, the system value, the quote, a suggested follow-up question and who to ask. | Writes the summary and the follow-up |
| 4. Judgment | Consultant picks a decision (Trust client account / Trust system / Needs follow-up) and types the reason. Submits. | nothing; this is human |
| 5. Updated | Field flips to Resolved with the decision logged, or Open with the follow-up assigned. Coverage and step status update. A decision log entry appears (this is the Key Design Decision record). | nothing |
| 6. Cycle closed | Step shows "5 of 6 explained, 1 follow-up open". Ready for the next interview. | nothing |

## State labels (plain words on screen)

Match · Contradiction · No data behind it · No one explained it · Not discussed · Resolved

## Timeline

| Block | Minutes | Deliverable |
|---|---|---|
| A. Storyboard + seed data | 0-25 | Six fields with system values and source table; the sales-manager transcript written so it lands exactly: 2 match, 1 contradiction, 1 no-data, 1 no-one-explained, 1 not-discussed |
| B. Agent output | 25-45 | One real Claude run over the transcript saved as JSON (state, quote, speaker, confidence, conflict_summary, follow_up_question, ask_who per field); hand-written if no key. Baked into the page |
| C. Page, agent half (journey steps 0-3) | 45-110 | One HTML page in Cloud ALM layout: BD9 diagram on top, step panel right with Evidence tab, Synthesize button with a short thinking animation, field cards with state colours, coverage bar, call-out cards |
| D. Page, human half (journey steps 4-6) | 110-140 | Judgment form on each call-out, state transitions, decision log, coverage recompute, "cycle closed" summary |
| E. Polish + rehearse | 140-160 | Run the demo twice end to end. Fix whatever stumbles |

## Stretch (only after E)

- Role switch: Process owner view (coverage + open contradictions), Interviewee view (their quotes and how each was used).
- Second transcript (AR lead) that answers the open follow-up, to show the cycle repeating.

## Stack

One self-contained HTML file. No server, no key needed in the room. The agent output is generated
once (a short Python script calling Claude, if ANTHROPIC_API_KEY is set) and embedded in the page.

## Demo script (90 seconds)

1. "Consultant just finished interviewing the sales manager. Here is the credit check step, nothing explained yet."
2. Pick the transcript, Synthesize.
3. "Every claim is tied to a configuration field. Two match. One contradicts the system: she thinks credit is only checked at order; the system re-checks high-risk customers at delivery. One has no data behind it: she says intercompany orders skip the check, nothing configured does that. One nobody explained: a review-date check is on and no one mentioned it. One wasn't discussed."
4. "The agent doesn't decide. It asks me." Open the contradiction call-out, choose Needs follow-up, type the reason, submit. Open the no-data gap, choose Trust client account with reason "manual release in VKM1", submit.
5. "The step is now 5 of 6 explained with one question queued for the credit controller. That decision log is what used to live in my head and an Excel file."

## Needs from you

- Optional: ANTHROPIC_API_KEY exported in your terminal before block B, so the embedded output is a real model run. Without it the output is hand-written and described as a mock.
