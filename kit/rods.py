"""RODS contract loader / linter (POC 03 pattern)."""
FIELDS = ("Role", "Output", "Do-Nots", "Signal")

def parse_rods(text):
    contract = {}
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        matched = None
        for f in FIELDS:
            if stripped.lower().startswith(f.lower() + ":"):
                matched = f
                if f in contract:
                    raise ValueError(f"duplicate field in contract: {f}")
                contract[f] = stripped.split(":", 1)[1].strip()
                break
        if not matched and current and stripped:
            contract[current] += " " + stripped
        elif matched:
            current = matched
    return contract

def lint_rods(contract):
    issues = []
    for f in FIELDS:
        if f not in contract or not contract[f]:
            issues.append(f"MISSING:{f}")
    sig = contract.get("Signal", "")
    if sig and sig.strip().lower() in ("done", "complete", "finished"):
        issues.append("WEAK_SIGNAL:signal is a common prose word")
    if contract.get("Output", "") and "table" not in contract["Output"].lower() and "schema" not in contract["Output"].lower() and "json" not in contract["Output"].lower():
        issues.append("VAGUE_OUTPUT:no table/schema/json shape named")
    return issues
