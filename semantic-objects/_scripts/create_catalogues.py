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

header = f'''
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
        schema:description """This catalogue contains SKOS ConceptScheme vocabularies for many of, and eventually all of, the codelists and enumerations presented in the ISO's 19* series of geographic information/geomantic standards.
        
These codelist versions are encoded using the human- and machine-readable [Resource Description Framework](https://www.w3.org/RDF/) conforming to the [Simple Knowledge Organization System (SKOS)]https://www.w3.org/TR/skos-reference/ data model for taxonomies. This allows for simple enough human reading - RDF files are text files - but also automated validating, automated absorption into databases, multi-codelist indexing, searching and so on.

TC-211 standards of the ISO 19* series are about "Geographic information/Geomatics". Many of those standards contain codelists of terms that are used within the standards' data models. For example, the standard [ISO 19115-1:2014
Geographic information — Metadata — Part 1: Fundamentals (ISO19115-1)](https://www.iso.org/standard/53798.html) contains the codelist _Association Type Codes_ (`DS_AssociationTypeCode`) which gives values for the _associationType_ property defined as identifying the "type of relation between the resources" (Table B.3.6 — Association information).

Many of the codelist vocabularies were initially produced in [Web Ontology Language (OWL)](https://www.w3.org/OWL/) data automatically generated from UML models of the TC-211 19* series of standards by GOM. Those OWL objects are available in this content's repository in the directory [isotc211_GOM_harmonizedOntology](https://github.com/ISO-TC211/GOM/tree/master/isotc211_GOM_harmonizedOntology/).

The _Association Type Codes_ codelist above has previously been delivered online several times as a non-ISO-sponsored publication in Semantic Web form. One such form was delivered by CSIRO, Australia's national scientific research agency, that is now offline but a catalogue entry for is still exists at https://vocabs.ardc.edu.au/viewById/272. Note that the CSIRO copy indicates that its source was this GOM repository's `isotc211_GOM_harmonizedOntology` directory contents.

Such unauthorised republications of ISO content are not allowed by ISO licensing. We encourage people wanting more ISO material delivered as machine-readable objects to contact the Group on Ontology maintenance, see this catalogue's publisher details for contact information.""" ;
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
        schema:codeRepository "https://github.com/ISO-TC211/GOM" ;
    .
    '''

g = Graph().parse(data=header, format="turtle")
for iri in vocab_iris:
        g.add((catalogue_iri, SDO.hasPart, URIRef(iri)))

g.serialize(destination=CODELISTS_DIR / "codelists-catalogue.ttl", format="longturtle")
print("done")
