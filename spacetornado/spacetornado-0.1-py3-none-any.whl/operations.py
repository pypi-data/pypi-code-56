import spacy

nlp = spacy.load('en_core_web_sm')


def __token(token):
    return {
        'text': str(token.text),
        'lemma': str(token.lemma_),
        'pos': str(token.pos_),
        'tag': str(token.tag_),
        'prettytag': str(spacy.explain(token.tag_)),
        'dep': str(token.dep_),
        'shape': str(token.shape_),
        'alpha': str(token.is_alpha),
        'stop': str(token.is_stop)
    }


def __noun_chunk(chunk):
    return {
        'text': str(chunk.text),
        'roottext': str(chunk.root.text),
        'rootdep': str(chunk.root.dep_),
        'rootheadtext': str(chunk.root.head.text)
    }


def __entity(entity):
    return {
        'text': str(entity.text),
        'start': str(entity.start_char),
        'end': str(entity.end_char),
        'label': str(entity.label_)
    }


def __similarity(left, right):
    return {
        'similarity': left.similarity(right)
    }


def tokens(text):
    return [__token(token) for token in nlp(text)]


def noun_chunks(text):
    return [__noun_chunk(chunk) for chunk in nlp(text).noun_chunks]


def entities(text):
    return [__entity(entity) for entity in nlp(text).ents]


def similarity(left, right):
    return __similarity(nlp(left), nlp(right))
