"""run_notebook_cells.py - run each notebook's code cells in order (no Jupyter needed) and compare what every cell
prints with the stream output stored in the notebook.

  python tools/run_notebook_cells.py [NOTEBOOK ...]     default: every notebooks/*/*.ipynb

Runs with matplotlib's Agg backend in the notebook's own folder. IPython magics and shell lines (% and !) are skipped.
Exit 0 only if every cell runs and every stored stdout equals the fresh stdout. Images and rich outputs are not compared.
"""
import contextlib
import glob
import io
import json
import os
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def stored_stdout(cell):
    return "".join("".join(o.get("text", [])) for o in cell.get("outputs", []) if o.get("output_type") == "stream" and o.get("name") == "stdout")


def run(nb_path):
    import matplotlib
    matplotlib.use("Agg")
    nb = json.load(open(nb_path, encoding="utf-8"))
    here = os.getcwd()
    os.chdir(os.path.dirname(nb_path))
    g = {"__name__": "__main__"}
    problems, n = [], 0
    try:
        for ci, cell in enumerate(nb.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
            n += 1
            src = "\n".join(l for l in "".join(cell.get("source", [])).splitlines() if not l.lstrip().startswith(("%", "!")))
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(compile(src, "<cell %d>" % ci, "exec"), g)
            except SystemExit:
                pass
            except Exception as e:
                problems.append("cell %d raised %s: %s" % (ci, type(e).__name__, str(e)[:200]))
                traceback.print_exc()
                break
            want = stored_stdout(cell)
            if want and buf.getvalue() != want:
                a, b = buf.getvalue().splitlines(), want.splitlines()
                k = next((i for i in range(max(len(a), len(b))) if (a[i] if i < len(a) else None) != (b[i] if i < len(b) else None)), 0)
                problems.append("cell %d stdout differs at line %d: stored %r / fresh %r" % (ci, k + 1, b[k] if k < len(b) else None, a[k] if k < len(a) else None))
    finally:
        os.chdir(here)
    return n, problems


def main(argv):
    nbs = argv or sorted(glob.glob(os.path.join(ROOT, "notebooks", "*", "*.ipynb")))
    if not nbs:                                    # an empty run is never a pass (same rule as notebook_code_sync C-1)
        print("FAIL: no notebooks found")
        return 1
    bad = 0
    for nb in nbs:
        n, problems = run(os.path.abspath(nb))
        print("%-60s %d code cells  %s" % (os.path.relpath(nb, ROOT), n, "OK" if not problems else "PROBLEMS"))
        for p in problems:
            print("   " + p)
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
