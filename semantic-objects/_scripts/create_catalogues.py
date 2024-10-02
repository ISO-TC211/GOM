from pathlib import Path
import re
from rdflib import Graph, URIRef
from rdflib.namespace import SDO

THIS_FILE = Path(__file__).resolve()
CODELISTS_DIR = THIS_FILE.parent.parent.resolve() / "codelists"

vocab_files = CODELISTS_DIR.glob("**/*.ttl")

vocab_iris = []
for f in sorted(vocab_files):
    rdf = f.read_text()
    if "skos:ConceptScheme" in rdf:
        print(f)
        vocab_iris.append(re.findall(r'PREFIX cs: <(.*)>', rdf)[0])

catalogue_iri = URIRef("http://def.isotc211.org/codelists/")

header = f"""
    PREFIX cat: <{catalogue_iri}>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX status: <http://def.isotc211.org/19135/-1/2015/CoreModel/code/RE_ItemStatus/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    cat:
        a dcat:Catalog ;
        schema:name "ISO TC-211 Codelist Vocabularies" ;
        schema:description "This catalogue contains SKOS ConceptScheme vocabularies for many of, and eventually all of, the codelists and enumerations presented in the ISO's 19* series of geographic information/geomantic standards" ;
        skos:historyNote "This catalogue was assembled from all the vocabularies made available by TC-211's Group on Ontology Maintenance"@en ;
        schema:contributor <https://www.ogc.org> ;
        schema:creator <https://committee.iso.org/home/tc211> ;
        schema:dateCreated "2024-09-03"^^xsd:date ;
        schema:dateModified "2024-09-03"^^xsd:date ;
        schema:publisher <https://committee.iso.org/home/tc211> ;
        schema:keywords
            "International Organization for Standardization" ,
            "ISO" ,
            "codelist" ,
            "geographic information" ,
            "geomatics" ;
    .
    """

g = Graph().parse(data=header, format="turtle")
for iri in vocab_iris:
        g.add((catalogue_iri, SDO.hasPart, URIRef(iri)))

g.serialize(destination=CODELISTS_DIR / "codelists-catalogue.ttl", format="longturtle")
print("done")
