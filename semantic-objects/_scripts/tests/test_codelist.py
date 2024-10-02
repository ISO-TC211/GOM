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


testdata_19157 = [
    CODELISTS_DIR / "19157" / "-1" / "2023" / "EvaluationMethodTypeCode.ttl",
    CODELISTS_DIR / "19157" / "-1" / "2023" / "ValueStructure.ttl",
]

@pytest.mark.parametrize("vocab", testdata_19157)
def test_19157(vocab):
    data_graph = Graph().parse(vocab) + agents_graph
    valid, results_graph, results_text = validate(data_graph, shacl_graph=validator_graph, allow_warnings=True)
    if not valid:
        print(f"{vocab} is not valid: {results_text}")

    assert valid


testdata_19135 = [
    CODELISTS_DIR / "19135" / "-1" / "2015" / "RE_AmendmentType.ttl",
    CODELISTS_DIR / "19135" / "-1" / "2015" / "RE_DecisionStatus.ttl",
    CODELISTS_DIR / "19135" / "-1" / "2015" / "RE_Disposition.ttl",
    CODELISTS_DIR / "19135" / "-1" / "2015" / "RE_ItemStatus.ttl",
    CODELISTS_DIR / "19135" / "-1" / "2015" / "RE_SimilarityToSource.ttl",
]

@pytest.mark.parametrize("vocab", testdata_19135)
def test_19135(vocab):
    data_graph = Graph().parse(vocab) + agents_graph
    valid, results_graph, results_text = validate(data_graph, shacl_graph=validator_graph, allow_warnings=True)
    if not valid:
        print(f"{vocab} is not valid: {results_text}")

    assert valid


testdata_19115 = [
    CODELISTS_DIR / "19115" / "-1" / "2018" / "CI_DateTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "CI_OnLineFunctionCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "CI_PresentationFormCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "CI_RoleCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "CI_TelephoneTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "CountryCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "DCPList.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "DS_AssociationTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "DS_InitiativeTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "KeywordTypeCode-Bio.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "LanguageCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_CellGeometryCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_CharacterSetCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_ClassificationCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_CoverageContentTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_DatatypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_DimensionNameTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_GeometricObjectTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_ImagingConditionCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_KeywordTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_MaintenanceFrequencyCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_MediumFormatCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_ProgressCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_ReferenceSystemTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_RestrictionCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_ScopeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_SpatialRepresentationTypeCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "MD_TopologyLevelCode.ttl",
    CODELISTS_DIR / "19115" / "-1" / "2018" / "SV_CouplingType.ttl",
]

@pytest.mark.parametrize("vocab", testdata_19115)
def test_19115(vocab):
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