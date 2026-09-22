# Product: the user journey for one cycle

User: the consultant. Context: just finished the interview with Dana Ruiz, Head of Retail Sales.
One page. Everything below happens on it.

## Action 1: Log in and locate the step
The user lands on the step they are reviewing. The screen shows the location in one line:
    Halo Beverages > Order-to-Cash > Standard sale to a retailer > Step 2: Price the order: discounts and approvals
Below it, the seven steps of Order-to-Cash as a flow, Step 2 highlighted, each step with its readiness.
The main area is a table of the six configuration items for Step 2. Columns: item, what the system does
(plain words), source row, verdict, evidence, my reason. Every verdict is "Not yet discussed".
Readiness: 0 of 6 explained.

## Action 2: Drop the transcript
The user drops or picks the transcript ("18 Sep, Dana Ruiz"). Clicks Synthesize.
Waiting state, a few seconds: "Reading transcript. Matching against 6 items. Checking process-mining facts."
The user can leave and come back; the state persists.

## Action 3: Check the agent's triage
The table is updated. Each item the interview touched now has one verdict:
    Match                 what she said agrees with the configuration
    Contradiction         what she said disagrees with the configuration
    Gap: missing data     she described a rule; nothing in the system produces it
    Gap: missing reason   the system has a rule; nobody explained it
Items the interview did not reach stay "Not yet discussed".
For each verdict the evidence column shows: her quote(s) verbatim with timestamp, the measured fact
from process mining if there is one, and the agent's one-line reasoning.
For a contradiction or a gap, the agent states exactly what is in conflict with what: "She says approval
starts above 10%. The system triggers at 15%. 412 orders in the last year sat between the two."
Readiness: 2 of 6 explained. 4 items need the user.

## Action 4: Make a judgment, item by item
The user opens an item that needs them. Two things are available on it:

  a) Talk to the agent. A chat box scoped to this item. The user asks the way they would ask any
     assistant: "show me the 412 orders", "what did Dana say exactly", "what would the S/4HANA
     standard do here", "draft the question for Marco". The agent answers from the evidence it has.
     It still does not decide.

  b) Write my reason. A text field under the item where the user records their own judgment and
     the reason behind it, in their words. Optional: who confirmed it, and a follow-up if one is
     still needed (question, person). Save.

Saving a reason marks the item Explained. The verdict stays visible as history (it was a
contradiction, here is how it was resolved). If the user saves a follow-up instead of a reason, the
item stays open and shows who owes the answer.

## Action 5: Close the cycle
When every one of the six items is either Match or Explained, the step is done for this cycle.
The screen says so: "Step 2: 6 of 6 explained. Ready for process owner review." The reasons and
decisions the user wrote form the record that goes to the process owner.
If items are still open with follow-ups, the screen says what is outstanding and who owes it, and the
cycle stays open until the next interview.

## Other roles (stretch)
Process owner: sees the flow with readiness per step, the items with their reasons, nothing to edit.
Interviewee: sees her own quotes, which item each supported, and the verdict. Can flag "not what I meant".

## Demo note
The page is static. Synthesize plays back the saved agent output. "Talk to the agent" plays back
prepared exchanges for each open item (two or three questions each), so it works with no network.
A live version would call the model behind both.
