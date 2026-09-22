"""Embed the data files into the page. Run after any change to data/ or app/template.html."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
model = json.loads((ROOT / "data/erp_model.json").read_text())
output = json.loads((ROOT / "data/agent_output.json").read_text())
chat = json.loads((ROOT / "data/agent_chat_script.json").read_text())
transcript = (ROOT / "data/interviews/01-sales-manager.md").read_text()

extract = {}
for rel in model["node"]["system_extract_files"]:
    p = ROOT / rel
    with p.open(newline="") as fh:
        extract[p.name] = list(csv.DictReader(fh))

readme = (ROOT / "data/system_extract/README.md").read_text()
sources = []
for line in readme.splitlines():
    if line.startswith("| ") and ".csv" in line:
        cells = [c.strip() for c in line.strip("|").split("|")]
        sources.append({"file": cells[0], "what": cells[1], "source": cells[2]})

data = {"model": model, "output": output, "chat": chat, "transcript": transcript, "extract": extract, "sources": sources}
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = (ROOT / "app/template.html").read_text().replace("__DATA__", blob)
(ROOT / "app/index.html").write_text(html)
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs/index.html").write_text(html)
print(f"wrote app/index.html ({len(html)//1024} KB), {len(extract)} extract files, {len(sources)} sources")
