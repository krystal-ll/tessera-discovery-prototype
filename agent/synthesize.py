"""One-shot reconciliation: interview transcript vs configuration fields for one process step.

Usage:
    python3 agent/synthesize.py                 # writes data/agent_output.json
    python3 agent/synthesize.py --dry-run       # prints the prompt, no API call

Reads data/erp_model.json and data/interviews/01-sales-manager.md.
Needs ANTHROPIC_API_KEY in the environment (or an `ant auth login` profile).
"""
import json
import os
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "data" / "erp_model.json"
TRANSCRIPT_PATH = ROOT / "data" / "interviews" / "01-sales-manager.md"
OUT_PATH = ROOT / "data" / "agent_output.json"

STATES = [
    "match",
    "contradiction",
    "gap_no_data",        # the person described behaviour that no configuration produces
    "gap_no_explanation", # the configuration exists, nobody has explained it
    "not_discussed",      # the interview never touched this field
]

SYSTEM = """You are the reconciliation agent inside a discovery tool for SAP ECC to S/4HANA migration projects.
A functional consultant has just finished an interview with a client stakeholder. You compare what the
stakeholder said against the client's actual system configuration for ONE process step, field by field.

For every configuration field you assign exactly one state:
- match: the stakeholder described behaviour that agrees with the configured value.
- contradiction: the stakeholder described behaviour that disagrees with the configured value.
- gap_no_data: the stakeholder described behaviour or a rule, and no configuration produces it.
- gap_no_explanation: the configuration exists and the interview touched the topic, but nobody explained
  why this value is set. Also use this when the interview offers only an anecdote that might relate.
- not_discussed: the interview never came near this field. Do not stretch a vague remark into coverage.

Rules:
- Quote the stakeholder verbatim. Never paraphrase inside a quote. Every quote must appear in the transcript.
- A stakeholder saying "I don't know" or "maybe I'm wrong" about a field is still evidence; reflect it in confidence.
- confidence is your confidence in the STATE you assigned, 0 to 1.
- For contradiction, gap_no_data and gap_no_explanation write a one-sentence conflict_summary a consultant
  can read in five seconds, a follow_up_question the consultant should ask next, and ask_who: the role or
  named person best placed to answer. For match and not_discussed set those three to null.
- The consultant makes the judgment, not you. Do not recommend which side is right. Surface the evidence.
- system_evidence: two or three plain-language sentences stating what the configuration and the measured
  facts show for this field, each with the source row it came from. No table or column names.
- missing_side: for gap_no_data set "system" (the client described it, no data produces it); for
  gap_no_explanation and not_discussed set "client" (data exists, no one explained it); else null.
  missing_note: one sentence saying what is missing, else null.
- Claims about this step that do not map to any listed field go in unmapped_claims so nothing is lost.
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "interview_id": {"type": "string"},
        "step_id": {"type": "string"},
        "fields": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field_id": {"type": "string"},
                    "state": {"type": "string", "enum": STATES},
                    "confidence": {"type": "number"},
                    "quotes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "speaker": {"type": "string"},
                                "text": {"type": "string"},
                            },
                            "required": ["speaker", "text"],
                            "additionalProperties": False,
                        },
                    },
                    "system_evidence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"text": {"type": "string"}, "source": {"type": "string"}},
                            "required": ["text", "source"],
                            "additionalProperties": False,
                        },
                    },
                    "missing_side": {"type": ["string", "null"], "enum": ["system", "client", None]},
                    "missing_note": {"type": ["string", "null"]},
                    "reasoning": {"type": "string"},
                    "conflict_summary": {"type": ["string", "null"]},
                    "follow_up_question": {"type": ["string", "null"]},
                    "ask_who": {"type": ["string", "null"]},
                },
                "required": ["field_id", "state", "confidence", "quotes", "system_evidence", "missing_side", "missing_note", "reasoning",
                             "conflict_summary", "follow_up_question", "ask_who"],
                "additionalProperties": False,
            },
        },
        "unmapped_claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "speaker": {"type": "string"},
                    "text": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["speaker", "text", "note"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["interview_id", "step_id", "fields", "unmapped_claims"],
    "additionalProperties": False,
}


def build_user_message(model, transcript):
    step = next(s for s in model["steps"] if s["id"] == model["node_step_id"])
    fields = model["node_fields"]
    lines = [
        f"Client: {model['client']['name']}. {model['client']['profile']}",
        f"Process: {model['process']['name']} ({model['process']['id']}).",
        f"Step under review: {step['id']} {step['name']} (lane: {step['lane']}).",
        "",
        "CONFIGURATION FIELDS (system side):",
    ]
    for f in fields:
        lines += [
            f"- {f['id']}: {f['label']}",
            f"    system value: {f['system_value']}",
            f"    in plain words: {f['plain']}",
            f"    derived from: {f['derived_from']['line']}",
            f"    source rows: {', '.join(f['source_rows'])}",
        ]
    lines += [
        "",
        "SOURCE TABLES (people, product, discount, the connections between them, and measured facts):",
    ]
    for rel in model["node"]["system_extract_files"]:
        lines += [f"--- {rel} ---", (ROOT / rel).read_text().strip()]
    lines += [
        "",
        "INTERVIEW TRANSCRIPT (stakeholder side):",
        transcript,
        "",
        "Set interview_id to \"01-sales-manager\" and step_id to the step id above. "
        "Return one entry per field, all six, in order F1..F6.",
    ]
    return "\n".join(lines)


def main():
    model = json.loads(MODEL_PATH.read_text())
    transcript = TRANSCRIPT_PATH.read_text()
    user_msg = build_user_message(model, transcript)

    if "--dry-run" in sys.argv:
        print(SYSTEM)
        print("=" * 80)
        print(user_msg)
        return

    client = anthropic.Anthropic()
    with client.messages.stream(
        model="claude-opus-5",
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
        thinking={"type": "adaptive"},
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason == "refusal":
        print("Model declined the request:", response.stop_details, file=sys.stderr)
        sys.exit(1)

    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
    data["_meta"] = {
        "model": response.model,
        "generated_by": "agent/synthesize.py",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    OUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"wrote {OUT_PATH}")
    for f in data["fields"]:
        print(f"  {f['field_id']}: {f['state']} ({f['confidence']:.2f})")


if __name__ == "__main__":
    main()
