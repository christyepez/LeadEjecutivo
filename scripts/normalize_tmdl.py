from pathlib import Path

root = Path(__file__).resolve().parents[1] / "LeadEjecutivo.SemanticModel" / "definition"
changed = 0
for path in root.rglob("*.tmdl"):
    text = path.read_text(encoding="utf-8")
    lines = []
    local = False
    for line in text.splitlines(True):
        original = line
        while line.startswith("\\t"):
            line = "\t" + line[2:]
        if line != original:
            local = True
        lines.append(line)
    if local:
        path.write_text("".join(lines), encoding="utf-8")
        changed += 1
print(f"Normalized TMDL files: {changed}")
