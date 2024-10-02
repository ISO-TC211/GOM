from pathlib import Path
from pyshacl import validate

THIS_FILE = Path(__file__).resolve()
CODELISTS_DIR = THIS_FILE.parent.parent / "codelists"

vocab_files = CODELISTS_DIR.glob("**/*.ttl")

for v in sorted(vocab_files):
    if "19160" in str(v):
        r = v.name + ":"
        valid, results_graph, results_text = validate(str(v), shacl_graph=str(THIS_FILE.parent / "vocpub-4.10.ttl"), allow_warnings=True)
        if valid:
            r += " OK"
        else:
            r += " not OK " + results_text
        print(r)