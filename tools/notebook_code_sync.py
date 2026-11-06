"""notebook_code_sync.py - keep the code inlined in each notebook identical to the repo's kit/ and poc/ source.

Each notebook inlines the kit primitives and its POC functions so it runs standalone in Colab. This tool compares
every top-level function, class and UPPER_CASE constant defined in a notebook code cell with the definition of the same
name in kit/*.py and that notebook's poc/*.py (whitespace-normalised source text).

  python tools/notebook_code_sync.py --check          exit 1 and list every drifted definition (use in CI)
  python tools/notebook_code_sync.py --write          replace each drifted definition in the notebook with the repo's
                                                      source text, leave everything else in the cell untouched

Names that exist only in the notebook are left alone. `main` is never compared. Stored cell outputs are not changed:
re-run the notebook (or tools/run_notebook_cells.py) to confirm they still match.
"""
import ast
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"main"}


def _defs(src):
    """{name: (normalised text, lineno, end_lineno, exact text)} for top-level defs/classes/UPPER constants."""
    out = {}
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return out
    for node in tree.body:
        name = None
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id.isupper():
            name = node.targets[0].id
        if not name or name in SKIP:
            continue
        start = min([d.lineno for d in getattr(node, "decorator_list", [])] + [node.lineno])
        lines = src.splitlines(keepends=True)
        exact = "".join(lines[start - 1:node.end_lineno])
        out[name] = (re.sub(r"\s+", " ", exact).strip(), start, node.end_lineno, exact)
    return out


def repo_defs(nb_dir):
    srcs = sorted(glob.glob(os.path.join(ROOT, "kit", "*.py"))) + sorted(glob.glob(os.path.join(nb_dir, "poc", "*.py")))
    out = {}
    for p in srcs:
        with open(p, encoding="utf-8") as f:
            for k, v in _defs(f.read()).items():
                out.setdefault(k, (v, os.path.relpath(p, ROOT).replace(os.sep, "/")))
    return out


COMPARED = {"notebooks": 0, "definitions": 0}


def process(nb_path, write):
    nb_dir = os.path.dirname(nb_path)
    ref = repo_defs(nb_dir)
    COMPARED["notebooks"] += 1
    with open(nb_path, encoding="utf-8", newline="") as f:
        raw = f.read()
    nb = json.loads(raw)
    drift = []
    for ci, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        found = _defs(src)
        COMPARED["definitions"] += sum(1 for name in found if name in ref)
        repl =[(name, d) for name, d in found.items() if name in ref and d[0] != ref[name][0][0]]
        if not repl:
            continue
        for name, _ in repl:
            drift.append("%s cell %d: %s differs from %s" % (os.path.relpath(nb_path, ROOT).replace(os.sep, "/"), ci, name, ref[name][1]))
        if write:
            lines = src.splitlines(keepends=True)
            for name, d in sorted(repl, key=lambda x: -x[1][1]):          # bottom-up so line numbers stay valid
                new = ref[name][0][3]
                if not new.endswith("\n") and d[2] < len(lines):
                    new += "\n"
                lines[d[1] - 1:d[2]] = [new]
            new_src = "".join(lines)
            if src.endswith("\n") is False and new_src.endswith("\n"):
                new_src = new_src[:-1]
            parts = new_src.splitlines(keepends=True)
            cell["source"] = parts
    if write and drift:
        text = json.dumps(nb, indent=1, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")   # keep the file's own ending
        with open(nb_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    return drift


def main(argv):
    if len(argv) != 1 or argv[0] not in ("--check", "--write"):
        print(__doc__)
        return 2
    write = argv[0] == "--write"
    drift = []
    for nb in sorted(glob.glob(os.path.join(ROOT, "notebooks", "*", "*.ipynb"))):
        drift += process(nb, write)
    for d in drift:
        print(("FIXED " if write else "DRIFT ") + d)
    print("compared %d notebooks, %d inlined definitions" % (COMPARED["notebooks"], COMPARED["definitions"]))
    if COMPARED["notebooks"] == 0 or COMPARED["definitions"] == 0:   # C-1: an empty comparison is not a pass
        print("FAIL: nothing was compared (no notebooks, or no inlined definition shared with kit/ and poc/)")
        return 1
    if not drift:
        print("notebook code matches kit/ and poc/ in every notebook")
    return 1 if (drift and not write) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
