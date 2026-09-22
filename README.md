# Tessera Discovery prototype

An interactive prototype of an AI discovery assistant for SAP ECC to S/4HANA migration projects.
One cycle: a consultant finishes an interview with the client's Head of Retail Sales, drops the
transcript, and an agent checks what she said against the pricing configuration and process-mining
facts for one step of Order-to-Cash. Each configuration item gets a verdict (match, contradiction,
gap: missing data, gap: missing reason), and the consultant records the judgment and reason.

Live prototype: see GitHub Pages for this repository (`docs/index.html`).

- `app/` page template, build script, and the built page
- `data/` fictional client (Halo Beverages), system extract, interview transcript, agent output
- `agent/synthesize.py` one-shot reconciliation with the Claude API (structured output)
- `research/` discovery-phase research, benchmark of SAP Cloud ALM, layout and style notes

All company, people, and data are fictional. Build with `python3 app/build.py`.
