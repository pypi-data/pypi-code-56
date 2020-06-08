from typing import List

from trompace.mutations import definedterm


def create_defined_terms(creator: str, name: str, terms: List[str]):
    definedtermsettype = "https://vocab.trompamusic.eu/vocab#TagCollection"
    definedtermtype = "https://vocab.trompamusic.eu/vocab#TagCollectionElement"

    dtsmutation = definedterm.create_defined_term_set(creator, name, definedtermsettype)
    dtsidentifier = None

    for term in terms:
        dtmutation = definedterm.create_defined_term(creator, term, definedtermtype)
        dtidentifier = None
        definedterm.add_defined_term_to_defined_term_set(dtsidentifier, dtidentifier)


def create_annotation_text():
    pass


def create_annotation_tag():
    pass


def create_annotation_term():
    pass


def create_annotation_rating():
    pass
