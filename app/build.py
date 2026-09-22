"""Embed the data files into the page. Run after any change to data/ or app/template.html."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
model = json.loads((ROOT / "data/erp_model.json").read_text())
output = json.loads((ROOT / "data/agent_output.json").read_text())
chat = json.loads((ROOT / "data/agent_chat_script.json").read_text())
find = json.loads((ROOT / "data/agent_items.json").read_text())
transcript = (ROOT / "data/interviews/01-sales-manager.md").read_text()

extract = {}
for rel in model["node"]["system_extract_files"]:
    p = ROOT / rel
    with p.open(newline="") as fh:
        extract[p.name] = list(csv.DictReader(fh))

db = {}
for name in ["people", "product", "discount", "connections"]:
    with (ROOT / f"data/db/{name}.csv").open(newline="") as fh:
        db[name] = list(csv.DictReader(fh))
sources = [
    {"file": "people", "what": "Who works on pricing at Halo: name, title, and whether they are still here.", "source": "Client HR list, cleaned by the consultant", "table": "people"},
    {"file": "product", "what": "What Halo sells: range, list price per case, and any negotiated price with its expiry.", "source": "Product master and price list, ECC", "table": "product"},
    {"file": "discount", "what": "Every discount rule in the system: the percentage, what it applies to, its kind, and since when.", "source": "Pricing configuration, ECC", "table": "discount"},
    {"file": "connections", "what": "How the three tables link: who set which discount, which discount applies to which product, who is in charge of what.", "source": "Change history and org chart, joined by the consultant", "table": "connections"},
]

data = {"model": model, "output": output, "chat": chat, "find": find, "transcript": transcript, "extract": extract, "db": db, "sources": sources}
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = (ROOT / "app/template.html").read_text().replace("__DATA__", blob)
(ROOT / "app/index.html").write_text(html)
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs/index.html").write_text(html)
print(f"wrote app/index.html ({len(html)//1024} KB), {len(extract)} extract files, {len(sources)} sources")
