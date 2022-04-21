# Codelist Vocabularies

This directory of GOM's code repository contains [Semantic Web](https://www.w3.org/standards/semanticweb/) versions of codelists found in ISO's [TC211's](https://www.iso.org/committee/54904.html) standards.

## Purpose

Many non-ISO-sponsored versions of TC211's codelists have been available on the Internet over the past two decades due to a community wish for certain machine-readable forms of them. In 2022, the TC is experimenting here with ISO-sponsored publication of them to try and fullfill that wish.

The technical role of this directory is to act as the data point-of-truth for Semantic Web versions of the codelists which are automatically published from here in humman- and service-accessible form via a "vocabulary server". 

## Codelists in Semantic Web form

These codelist versions are encoded using the human- and machine-readable [Resource Description Framework](https://www.w3.org/RDF/) and according to the [Simple Knowledge Organization System (SKOS)](https://www.w3.org/TR/skos-reference/) data model for taxonomies. This allows for simple ehough human reading - RDF files are text files - but also automated validating, automated absorption into databases, multi-codelist indexing, searching and so on. 

This director is monitored by automated tools which provide validation reports of new codelists to the GOM managers of it. Codelists RDF files are also able to be automatically loaded into the vocabulary server which delivers published vocabularies at their namespace-based web page locations online.

The entry point for the vocabulary server is:

* *not ready yet!*

At that entry point, you can find a listing of all of these codelists as well as browse and search tools to use them. Clicking on the hyperlink indentifiers for elements within these Semantic Web codelists on the vocabulary server or elsewhere will lead to their vocabulary server-delivered form. Machines may also resolve codelist hyperlink indentifiers in ways that lead to machein-readable formats of the content.

The dual publication in human- and machine-readable form of these codelists by a vocabulary server is a core principle/requirement/aspect of the Semantic Web.

## Codelist source

The source data used to make the Semantic Web forms of the codelists here are the [Web Ontology Language (OWL)](https://www.w3.org/OWL/) forms of TC211's UML models delivered in this repository in the directory [isotc211_GOM_harmonizedOntology](https://github.com/ISO-TC211/GOM/tree/master/isotc211_GOM_harmonizedOntology/).

## Codelist Content

TC211 standards are the ISO 19* series of standards related to "Geographic information/Geomatics". Many of those standards contain codelists of terms that are used within the standards' data models. For example, the standard [ISO 19115-1:2014
Geographic information — Metadata — Part 1: Fundamentals (ISO19115-1)](https://www.iso.org/standard/53798.html) contains the codelist _Association Type Codes_ (`DS_AssociationTypeCode <<CodeList>>`) which gives values for the _associationType_ property defined as identifying the "type of relation between the resources" (Table B.3.6 — Association information). Terms in this codelist are presented in Table B.3.8 which is reproduced below:

![](iso19115/-1/2014/AssociationTypeCodes.png)

## Non-ISO publication

The _Association Type Codes_ codelist above has previously been delivered online several times as a non-ISO-sponsored publication in Semantic Web form. One such form was delivered by CSIRO, Australia's national scientific research agency, that is now offline but a catalogue entry for is still exists at https://vocabs.ardc.edu.au/viewById/272. Note that the CSIRO copy indicates that its source was this GOM repository's isotc211_GOM_harmonizedOntology directory contents.

## Current publication

Each codelist in this directory is presented in its own RDF text file in the [Turtle](https://www.w3.org/TR/turtle/) serialization. The _Association Type Codes_ codelist above is in the file `iso19115/-1/-2014/AssociationTypeCodes.ttl`.

For demonstration only, the _Association Type Codes_ codelist is also presented in alternate RDF serializations:

* `iso19115/-1/-2014/AssociationTypeCodes.rdf` - [RDF/XML](http://www.w3.org/TR/rdf-syntax-grammar/)
* `iso19115/-1/-2014/AssociationTypeCodes.json` - [JSON-LD](https://www.w3.org/TR/json-ld/)
* `iso19115/-1/-2014/AssociationTypeCodes.nt` - [N-Triples](https://www.w3.org/TR/n-triples/)

Other codelists will only be delivered here in the Turtle format. Many tools exist to convert from one format to another.


### Differences with original GOM OWL publication

The _Association Type Codes_ codelist's first interpretation into Semantic Web form is as a SKOS `ConceptScheme` and `Collection` with the [Identification Information](https://github.com/ISO-TC211/GOM/blob/master/isotc211_GOM_harmonizedOntology/iso19115/-1/2014/IdentificationInformation.rdf) module of ISO19115-1 in OWL form which is available here:

* https://github.com/ISO-TC211/GOM/blob/master/isotc211_GOM_harmonizedOntology/iso19115/-1/2014/IdentificationInformation.rdf#L1179

Differences between that original form and that presented here are:

1. These codelists use Turtle as the base RDF format
1. Here, codelists are presented in their own files, not embedded within stnadards' ontologies
1. Codelist terms here have descriptions provided, not just labels
1. The `rdfs:isDefinedBy` property is now used to indicate the original `skos:ConceptScheme` defining the resources, not a link to the original standard. That task is now performed by the `dcterms:source` property
1. `skos:Collection` instnaces are not given for all the `skos:Concept` instances in a `skos:ConceptScheme` as flat lists of `skos:Concept` instances can be made easily with queries 

Codelists presented here as `skos:ConceptScheme` instances conform to the [_VocPub Profile_ of SKOS](https://w3id.org/profile/vocpub) which defines the minimum set of properties that these Semantic Web codelist all have.


https://inspire.ec.europa.eu/codelist