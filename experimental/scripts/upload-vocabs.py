from typing import List, Union
import json
import os
import time
import argparse
from pathlib import Path
import httpx
from rdflib import Graph
from rdflib.namespace import RDF, SKOS
from pyshacl import validate


def validate_vocab(vocab: Union[Path, Graph]):
    val = Graph().parse(Path(__file__).parent / "vocpub.ttl")
    if type(vocab) == Path:
        vocab = Graph().parse(vocab)
    return validate(vocab, shacl_graph=val, allow_warnings=True)


def validate_all_vocabs():
    for vocab in sorted(list_all_vocabs()):
        conforms, results_graph, results_text = validate_vocab(vocab)
        if not conforms:
            print(f"{vocab.name} is invalid")
            # print(results_text)


def upload_vocab(p: Path):
    g = Graph().parse(p)
    v = validate_vocab(g)
    if v[0]:
        print(f"Uploading {p.name}")
        iri = None
        for cs in g.subjects(RDF.type, SKOS.ConceptScheme):
            iri = str(cs)

        r = httpx.post(
            DB_ENDPOINT + "/data",
            params={"graph": iri},
            headers={"Content-Type": "text/turtle"},
            content=p.read_bytes(),
            auth=(DB_USERNAME, DB_PASSWORD),
        )

        assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)

        r = httpx.post(
            DB_ENDPOINT,
            data={"update": f"ADD <{iri}> TO DEFAULT"},
            auth=(DB_USERNAME, DB_PASSWORD),
        )

        assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)
    else:
        print(f"Skipping {p.name}, invalid")


def upload_vocab_via_sparql_insert(p: Path):
    g = Graph().parse(p)
    iri = g.value(predicate=RDF.type, object=SKOS.ConceptScheme)
    print(f"Uploading file {p.name} to graph <{iri}>")

    nt = g.serialize(format="ntriples")
    sparql = f"INSERT DATA {{ GRAPH <{iri}> {{ {nt} }} }}"

    r = httpx.post(
        DB_ENDPOINT,
        data={"update": sparql},
        auth=(DB_USERNAME, DB_PASSWORD),
    )

    assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)

    r = httpx.post(
        DB_ENDPOINT,
        data={"update": f"ADD <{iri}> TO DEFAULT"},
        auth=(DB_USERNAME, DB_PASSWORD),
    )

    assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)


def upload_all_vocabs():
    for vocab in list_all_vocabs():
        upload_vocab_via_sparql_insert(vocab)


def drop_all_vocabs():
    r = httpx.post(DB_ENDPOINT, data={"update": "DROP ALL"}, auth=(DB_USERNAME, DB_PASSWORD))

    assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)
    print("All dropped")


def list_all_vocabs():
    vs = []
    for v in Path(Path(__file__).parent.parent / "codelist-vocabularies").rglob("*.ttl"):
        if "_reference-ontologie" not in str(v):
            vs.append(v)
    return vs


if __name__ == "__main__":
    # validate_all_vocabs()
    DB_ENDPOINT = os.environ.get("DB_ENDPOINT", None)
    DB_USERNAME = os.environ.get("DB_USERNAME", None)
    DB_PASSWORD = os.environ.get("DB_PASSWORD", None)

    # drop_all_vocabs()
    upload_all_vocabs()
