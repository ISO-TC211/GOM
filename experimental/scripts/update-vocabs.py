from pathlib import Path
from rdflib import Graph, BNode, URIRef
from rdflib.namespace import PROV, RDF, RDFS, SKOS

for filepath in Path("../codelist-vocabularies").rglob("*.ttl"):
    if "_reference-ontologies" not in str(filepath):
        print(filepath.absolute())

        g = Graph().parse(filepath.absolute())
        cs = None
        for s in g.subjects(RDF.type, SKOS.ConceptScheme):
            cs = s
        qd = BNode()
        dmode = URIRef("http://linked.data.gov.au/def/vocab-derivation-modes/none")
        g.add((cs, PROV.qualifiedDerivation, qd))
        g.add((qd, PROV.hadRole, dmode))
        Path(filepath.rename(filepath.with_suffix(".old.ttl")))
        g.serialize(destination=filepath, format="longturtle")
