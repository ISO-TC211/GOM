from pathlib import Path
from pyshacl import validate
from rdflib import Graph

THIS_FILE = Path(__file__).resolve()
CODELISTS_DIR = THIS_FILE.parent.parent / "codelists"

vocab_files = CODELISTS_DIR.glob("**/*.ttl")

validator_graph = Graph().parse(THIS_FILE.parent / "vocpub-4.10.ttl")
agents_graph = Graph().parse(CODELISTS_DIR / "agents.ttl")

for v in sorted(vocab_files):
    if "19160" in str(v):
        data_graph = Graph().parse(v) + agents_graph
        r = v.name + ":"
        valid, results_graph, results_text = validate(data_graph, shacl_graph=validator_graph, allow_warnings=True)
        if valid:
            r += " OK"
        else:
            r += " not OK "
        print(r)