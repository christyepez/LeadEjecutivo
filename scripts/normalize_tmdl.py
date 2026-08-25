from pathlib import Path

root = Path(__file__).resolve().parents[1] / "LeadEjecutivo.SemanticModel" / "definition"
changed = 0

for path in root.rglob("*.tmdl"):
    text = path.read_text(encoding="utf-8")
    lines = []
    local = False

    for line in text.splitlines(True):
        original = line

        # Normalize literal "\\t" tokens only while they are part of the
        # indentation prefix. Handles both "\\tproperty" and "\t\\tproperty".
        while True:
            prefix_len = 0
            while prefix_len < len(line) and line[prefix_len] == "\t":
                prefix_len += 1
            if line[prefix_len:prefix_len + 2] == "\\t":
                line = line[:prefix_len] + "\t" + line[prefix_len + 2:]
            else:
                break

        if line != original:
            local = True
        lines.append(line)

    if local:
        path.write_text("".join(lines), encoding="utf-8")
        changed += 1

print(f"Normalized TMDL files: {changed}")
