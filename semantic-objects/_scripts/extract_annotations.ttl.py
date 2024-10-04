from rdflib import Graph

g = Graph().parse("../codelists/19135/-1/2015/RE_ItemStatus.ttl")

q = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <https://schema.org/>
 
    CONSTRUCT {
        ?c 
            rdfs:label ?pl_nolang ;
            schema:description ?d_nolang ;
        . 
    }
    WHERE {
        ?c a skos:Concept ;
            skos:prefLabel ?pl ;
            skos:definition ?d ;
        .
        
        BIND(STR(?pl) AS ?pl_nolang)    
        BIND(STR(?d) AS ?d_nolang)    
    }
    """

r = g.query(q)

r.serialize(format="longturtle", destination="../_background/iso-statuses-annotations.ttl")
