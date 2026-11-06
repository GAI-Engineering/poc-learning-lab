"""Tests for tools/notebook_code_sync.py. Run: python tools/test_notebook_code_sync.py (exit 0 = all pass).

1. The real repository passes --check and reports a non-zero comparison count.
2. C-1: a tree with no notebooks fails (an empty comparison is never a pass).
3. A tree whose notebook shares no definition with kit/ fails.
4. A notebook with a drifted definition fails, and --write makes it pass.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "notebook_code_sync.py")


def run(root, mode="--check"):
    p = subprocess.run([sys.executable, os.path.join(root, "tools", "notebook_code_sync.py"), mode], capture_output=True, text=True)
    return p.returncode, p.stdout


def tree(files):
    root = tempfile.mkdtemp(prefix="nbsync-")
    os.makedirs(os.path.join(root, "tools"))
    shutil.copy(TOOL, os.path.join(root, "tools"))
    for rel, text in files.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    return root


def nb(code):
    return json.dumps({"cells": [{"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": code.splitlines(keepends=True)}],
                       "metadata": {}, "nbformat": 4, "nbformat_minor": 5}, indent=1)


def main():
    fails = 0

    def T(name, ok):
        nonlocal fails
        print(("  PASS  " if ok else "  FAIL  ") + name)
        fails += 0 if ok else 1

    code, out = subprocess.run([sys.executable, TOOL, "--check"], capture_output=True, text=True).returncode, ""
    out = subprocess.run([sys.executable, TOOL, "--check"], capture_output=True, text=True).stdout
    T("1 real repository passes and compares something", code == 0 and "compared 0 notebooks" not in out and ", 0 inlined" not in out)

    code, out = run(tree({"kit/k.py": "def f():\n    return 1\n"}))
    T("2 C-1: no notebooks -> exit 1", code == 1 and "nothing was compared" in out)

    code, out = run(tree({"kit/k.py": "def f():\n    return 1\n", "notebooks/x/x.ipynb": nb("def other():\n    return 2\n")}))
    T("3 C-1: no shared definition -> exit 1", code == 1 and "nothing was compared" in out)

    root = tree({"kit/k.py": "def f():\n    return 1\n", "notebooks/x/x.ipynb": nb("def f():\n    return 99\n")})
    code, out = run(root)
    T("4a drifted definition -> exit 1 and named", code == 1 and "DRIFT" in out and ": f differs" in out)
    run(root, "--write")
    code, out = run(root)
    T("4b after --write the same tree passes", code == 0 and "matches" in out)

    print("ALL PASS" if not fails else "FAILED %d" % fails)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
