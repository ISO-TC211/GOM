from pathlib import Path
from rdflib import Graph

THIS_FILE = Path(__file__).resolve()
SEM_OBS_DIR = THIS_FILE.parent.parent

all_ttl_files = SEM_OBS_DIR.glob("**/*.ttl")

for f in sorted(all_ttl_files):
    g = Graph().parse(f)
    open(f, "w").write(g.serialize(format="longturtle"))

print("done")
