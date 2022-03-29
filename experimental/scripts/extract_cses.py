from pathlib import Path
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SDO, SKOS, XSD
import re

REG = Namespace("http://purl.org/linked-data/registry#")
STATUS = Namespace("http://def.isotc211.org/iso19135/-1/2015/CoreModel/code/RE_ItemStatus/")


def pretty_title(title: str):
    t = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", title)
    t = re.sub(r"_", " ", t)
    t = re.sub(r"(?<=[A-Z]{1:})", " ", t)

    return t


def main():
    tc_graph = Graph()

    tc = URIRef("http://def.isotc211.org/org/tc211")
    tc_graph.add((tc, RDF.type, SDO.Organization))
    tc_graph.add((tc, SDO.name, Literal("ISO's Technical Committee 211")))
    tc_graph.add((tc, SDO.description, Literal("The International Organization for Standardization's Technical Committee on \"Geographic information/Geomatics\", charged with standardization in the field of digital geographic information", lang="en")))
    tc_graph.add((tc, SDO.url, Literal("https://www.iso.org/committee/54904.html", datatype=XSD.anyURI)))

    ont_dir = Path(__file__).parent.parent.parent / "isotc211_GOM_harmonizedOntology" / "iso19115" / "-1" / "2018"
    voc_dir = Path(__file__).parent.parent.parent / "experimental" / "codelist-vocabularies" / "iso19115" / "-1" / "2018"
    voc_dir.mkdir(parents=True, exist_ok=True)

    rdf_files = ont_dir.glob("*.rdf")

    g = Graph()
    for f in rdf_files:
        print(f"parsing {f}")
        g.parse(f)
        print(len(g))

    for cs in g.subjects(RDF.type, SKOS.ConceptScheme):
        g2 = Graph()
        g2.bind("reg", REG)
        g2.bind("status", STATUS)
        g2.bind("cs", cs)
        g2.bind("", Namespace(str(cs) + "/"))
        for s, p, o in g.triples((cs, None, None)):
            if p == RDFS.isDefinedBy:
                g2.add((cs, DCTERMS.source, Literal(str(o), datatype=XSD.anyURI)))
                g2.remove((cs, RDFS.isDefinedBy, o))
            elif p == SKOS.prefLabel:
                g2.add((cs, p, Literal(pretty_title(str(o).replace(" - ConceptScheme", "")), lang="en")))
            else:
                g2.add((s, p, o))
        g2.add((cs, SKOS.definition, Literal("An ISO standard's ConceptScheme", lang="en")))

        # CS metadata
        g2.add((cs, DCTERMS.creator, tc))
        g2.add((cs, DCTERMS.created, Literal("2000-01-01", datatype=XSD.date)))
        g2.add((cs, DCTERMS.publisher, tc))
        g2.add((cs, DCTERMS.modified, Literal("2000-01-01", datatype=XSD.date)))
        g2.add((cs, DCTERMS.issued, Literal("2000-01-01", datatype=XSD.date)))
        g2.add((cs, DCTERMS.provenance, Literal("Derived from TC211-produced RDF versions of the standard's UML", lang="en")))
        g2.add((cs, DCTERMS.identifier, Literal(str(cs).split("/")[-1], datatype=XSD.token)))

        g2 += tc_graph

        for c in g.subjects(SKOS.inScheme, cs):
            for s2, p2, o2 in g.triples((c, None, None)):
                if p2 == RDF.type and o2 != SKOS.Concept:
                    pass
                else:
                    if p2 == RDFS.isDefinedBy:
                        g2.add((s2, p2, cs))
                    elif p2 == SKOS.prefLabel:
                        g2.add((s2, p2, Literal(pretty_title(str(o2)).lower(), lang="en")))
                    else:
                        g2.add((s2, p2, o2))
            g2.add((c, DCTERMS.provenance, Literal("Presented in the original standard's codelist", lang="en")))
            g2.add((c, SKOS.topConceptOf, cs))
            g2.add((c, DCTERMS.identifier, Literal(str(c).split("/")[-1], datatype=XSD.token)))
            g2.add((c, REG.status, STATUS.stable))

            g2.add((cs, SKOS.hasTopConcept, c))

            if (c, SKOS.definition, None) not in g2:
                g2.add((c, SKOS.definition, Literal("Missing", lang="en")))

        g2.serialize(destination=Path(voc_dir) / f"{str(cs).split('/')[-1]}.ttl", format="longturtle")


if __name__ == "__main__":
    # strs = [
    #     "CamelCase",
    #     "camelCase camelCase",
    #     "CamelCamelCCCase",
    #     "CI_TelephoneTypeCode",
    #     "DCPList",
    #     "MD_SpatialRepresentationTypeCode"
    # ]
    # for s in strs:
    #     print(pretty_title(s))
    main()
