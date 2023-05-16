from pathlib import Path
from rdflib import Graph, BNode, URIRef, Namespace
from rdflib.namespace import DCTERMS, PROV, RDF, RDFS, SKOS

REG = Namespace("http://purl.org/linked-data/registry#")
STATUS = Namespace("http://def.isotc211.org/iso19135/-1/2015/CoreModel/code/RE_ItemStatus/")

for filepath in Path("../codelist-vocabularies").rglob("*.ttl"):
    if "_reference-ontologies" not in str(filepath):
        print(filepath.absolute())

        g = Graph().parse(filepath.absolute())
        g.bind("reg", REG)
        g.bind("status", STATUS)

        cs = None
        for s in g.subjects(RDF.type, SKOS.ConceptScheme):
            cs = s
        # qd = BNode()
        # g.add((cs, PROV.qualifiedDerivation, qd))
        # g.add((qd, PROV.hadRole, URIRef("https://linked.data.gov.au/def/vocab-derivation-modes/none")))
        # g.add((qd, PROV.entity, URIRef("http://example.com/none")))
        # Path(filepath.rename(filepath.with_suffix(".old.ttl")))
        # g.serialize(destination=filepath, format="longturtle")

        g.remove((cs, DCTERMS.description, None))

        g.serialize(destination=filepath, format="longturtle")
