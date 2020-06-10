'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Namespace
Module | `namespace.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''

__all__ = [
    'CSVW',
    'DC',
    'DCAT',
    'DCTERMS',
    'DOAP',
    'FOAF',
    'Namespace',
    'ODRL2',
    'ORG',
    'OWL',
    'PROF',
    'PROV',
    'QB',
    'RDF',
    'RDFS',
    'SDO',
    'SH',
    'SKOS',
    'SMTK',
    'SOSA',
    'SSN',
    'TIME',
    'XMLNS',
    'XSD',
    'VOID'
]

from .identifier.uriref import URIRef


class Namespace(str):
    __slots__ = ()

    def term(self, name):
        return URIRef(self + (name if isinstance(name, str) else ''))

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError
        return self.term(name)

    def __getitem__(self, key):
        return self.term(key)

    def __new__(cls, value):
        try:
            namespace = str.__new__(cls, value)
        except UnicodeDecodeError:
            namespace = str.__new__(cls, value, "utf-8")
        return namespace

    def __repr__(self):
        return "Namespace('%s')" % self

CSVW = Namespace('http://www.w3.org/ns/csvw#')
DC = Namespace('http://purl.org/dc/elements/1.1/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')
DCTERMS = Namespace('http://purl.org/dc/terms/')
DOAP = Namespace('http://usefulinc.com/ns/doap#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
ODRL2 = Namespace('http://www.w3.org/ns/odrl/2/')
ORG = Namespace('http://www.w3.org/ns/org#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
PROF = Namespace('http://www.w3.org/ns/dx/prof/')
PROV = Namespace('http://www.w3.org/ns/prov#')
QB = Namespace('http://purl.org/linked-data/cube#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
SDO = Namespace('https://schema.org/')
SH = Namespace('http://www.w3.org/ns/shacl#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SMTK = Namespace('https://raw.githubusercontent.com/semantyk/Semantyk/master/Archive/archive.ttl/')
SOSA = Namespace('http://www.w3.org/ns/sosa/')
SSN = Namespace('http://www.w3.org/ns/ssn/')
TIME = Namespace('http://www.w3.org/2006/time#')
XMLNS = Namespace('http://www.w3.org/XML/1998/namespace')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
VOID = Namespace('http://rdfs.org/ns/void#')
