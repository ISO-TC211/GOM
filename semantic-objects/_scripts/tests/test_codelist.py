from pathlib import Path
from pyshacl import validate
from rdflib import Graph
from rdflib.namespace import RDF, SH
import pytest

THIS_FILE = Path(__file__).resolve()
CODELISTS_DIR = THIS_FILE.parent.parent.resolve().parent / "codelists"

vocab_files = CODELISTS_DIR.glob("**/*.ttl")

validator_graph = Graph().parse(THIS_FILE.parent.parent / "vocpub-4.10.ttl")
agents_graph = Graph().parse(CODELISTS_DIR / "agents.ttl")

testdata_19160 = [
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressAliasType.ttl",
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressClass.ttl", # No Concepts
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressComponentType.ttl",
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressComponentValueType.ttl",
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressLifecycleStage.ttl",
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressPositionType.ttl", # No Concepts
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressStatus.ttl",
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressTypology.ttl",
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressableObjectLifecycleStage.ttl",
    CODELISTS_DIR / "19160" / "-1" / "2015" / "AddressableObjectType.ttl", # No Concepts
    CODELISTS_DIR / "19160" / "-1" / "2015" / "ReferenceObjectType.ttl", # No Concepts
]

@pytest.mark.parametrize("vocab", testdata_19160)
def test_19160(vocab):
    data_graph = Graph().parse(vocab) + agents_graph
    valid, results_graph, results_text = validate(data_graph, shacl_graph=validator_graph, allow_warnings=True)
    # allow vocabs to have no Concepts
    if not valid:
        results_graph: Graph
        for s in results_graph.subjects(predicate=RDF.type, object=SH.ValidationReport):
            for o in results_graph.objects(subject=s, predicate=SH.result):
                for o2 in results_graph.objects(subject=o, predicate=SH.resultMessage):
                    assert "Requirement 2.1.9 " in str(o2), f"Vocab {vocab} is invalid: {o2}"
    else:
        assert valid