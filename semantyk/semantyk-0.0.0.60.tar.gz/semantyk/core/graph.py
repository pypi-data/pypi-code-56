'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Graph
Module | `graph.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''

# TODO
# collection() 
# de_skolemize()
# parse()
# query()
# resource()
# serialize()
# seq()
# triples()
# update()
# value()
# _get_namespace_manager()
# namespace_manager = property()

__all__ = ['Graph'] 

import random

from .identifier.bnode import BNode
from .identifier.uriref import URIRef
from .namespace import RDF, RDFS, SKOS
from .node import Node


class Graph(Node):
    def absolutize(self, uri, defrag=1):
        return self.namespace_manager.absolutize(uri, defrag)

    def add(self, triple):
        s, p, o = triple
        assert isinstance(s, Node), 'Subject %s must be a Node' % (s)
        assert isinstance(p, Node), 'Predicate %s must be a Node' % (p)
        assert isinstance(o, Node), 'Object %s must be a Node' % (o)
        self.__store.add((s, p, o), self, quoted=False)

    def addN(self, quads):
        self.__store.addN(
            (s, p, o, c)
            for s, p, o, c in quads
            if isinstance(c, Graph) 
            and c.identifier is self.identifier 
            and _assertnode(s, p, o)
        )

    def all_nodes(self):
        res = set(self.objects())
        res.update(self.subjects())
        return res

    def bind(self, prefix, namespace, override=True, replace=False):
        return self.namespace_manager.bind(prefix, namespace, override=override, replace=replace)

    def close(self, commit_pending_transaction=False):
        self.__store.close(commit_pending_transaction=commit_pending_transaction)

    def comment(self, subject, default=""):
        if subject is None:
            return default
        return self.value(subject, RDFS.comment, default=default, any=True)

    def commit(self):
        self.__store.commit()

    def compute_qname(self, uri, generate=True):
        return self.namespace_manager.compute_qname(uri, generate)

    def connected(self):
        all_nodes = list(self.all_nodes())
        discovered = []
        if not all_nodes:
            return False
        visiting = [all_nodes[random.randrange(len(all_nodes))]]
        while visiting:
            x = visiting.pop()
            if x not in discovered:
                discovered.append(x)
            for new_x in self.objects(subject=x):
                if new_x not in discovered and new_x not in visiting:
                    visiting.append(new_x)
            for new_x in self.subjects(object=x):
                if new_x not in discovered and new_x not in visiting:
                    visiting.append(new_x)
        if len(all_nodes) == len(discovered):
            return True
        else:
            return False

    def destroy(self, configuration):
        self.__store.destroy(configuration)

    def isomorphic(self, other):
        if len(self) != len(other):
            return False
        for s, p, o in self:
            if not isinstance(s, BNode) and not isinstance(o, BNode):
                if not (s, p, o) in other:
                    return False
        for s, p, o in other:
            if not isinstance(s, BNode) and not isinstance(o, BNode):
                if not (s, p, o) in self:
                    return False
        return True

    def items(self, list):
        chain = set([list])
        while list:
            item = self.value(list, RDF.first)
            if item is not None:
                yield item
            list = self.value(list, RDF.rest)
            if list in chain:
                raise ValueError("List contains a recursive rdf:rest reference")
            chain.add(list)

    def label(self, subject, default=""):
        if subject is None:
            return default
        return self.value(subject, RDFS.label, default=default, any=True)

    def load(self, source, publicID=None, format="xml"):
        self.parse(source, publicID, format)

    def namespaces(self):
        for prefix, namespace in self.namespace_manager.namespaces():
            yield prefix, namespace

    def n3(self):
        return '[%s]' % self.identifier.n3()

    def objects(self, subject=None, predicate=None):
        for s, p, o in self.triples((subject, predicate, None)):
            yield o

    def open(self, configuration, create=False):
        return self.__store.open(configuration, create)

    def predicates(self, subject=None, object=None):
        for s, p, o in self.triples((subject, None, object)):
            yield p

    def predicate_objects(self, subject=None):
        for s, p, o in self.triples((subject, None, None)):
            yield p, o

    def preferredLabel(self, subject, lang=None, default=None, labelProperties=(SKOS.prefLabel, RDFS.label)):
        if default is None:
            default = []
        if lang is not None:
            if lang == "":
                def langfilter(l):
                    return l.language is None
            else:
                def langfilter(l):
                    return l.language == lang
        else:
            def langfilter(l):
                return True
        for labelProp in labelProperties:
            labels = list(filter(langfilter, self.objects(subject, labelProp)))
            if len(labels) == 0:
                continue
            else:
                return [(labelProp, l) for l in labels]
        return default

    def qname(self, uri):
        return self.namespace_manager.qname(uri)

    def remove(self, triple):
        self.__store.remove(triple, context=self)

    def rollback(self):
        self.__store.rollback()

    def set(self, triple):
        (subject, predicate, object_) = triple
        assert (subject is not None), "s can't be None in .set([s,p,o]), as it would remove (*, p, *)"
        assert (predicate is not None), "p can't be None in .set([s,p,o]), as it would remove (s, *, *)"
        self.remove((subject, predicate, None))
        self.add((subject, predicate, object_))

    def skolemize(self, new_graph=None, bnode=None, authority=None, basepath=None):
        def do_skolemize(bnode, t):
            (s, p, o) = t
            if s == bnode:
                s = s.skolemize(authority=authority, basepath=basepath)
            if o == bnode:
                o = o.skolemize(authority=authority, basepath=basepath)
            return s, p, o
        def do_skolemize2(t):
            (s, p, o) = t
            if isinstance(s, BNode):
                s = s.skolemize(authority=authority, basepath=basepath)
            if isinstance(o, BNode):
                o = o.skolemize(authority=authority, basepath=basepath)
            return s, p, o
        retval = Graph() if new_graph is None else new_graph
        if bnode is None:
            self._process_skolem_tuples(retval, do_skolemize2)
        elif isinstance(bnode, BNode):
            self._process_skolem_tuples(retval, lambda t: do_skolemize(bnode, t))
        return retval

    def subjects(self, predicate=None, object=None):
        for s, p, o in self.triples((None, predicate, object)):
            yield s

    def subject_objects(self, predicate=None):
        for s, p, o in self.triples((None, predicate, None)):
            yield s, o

    def subject_predicates(self, object=None):
        for s, p, o in self.triples((None, None, object)):
            yield s, p

    def transitiveClosure(self, func, arg, seen=None):
        if seen is None:
            seen = {}
        elif arg in seen:
            return
        seen[arg] = 1
        for rt in func(arg, self):
            yield rt
            for rt_2 in self.transitiveClosure(func, rt, seen):
                yield rt_2

    def transitive_objects(self, subject, property, remember=None):
        if remember is None:
            remember = {}
        if subject in remember:
            return
        remember[subject] = 1
        yield subject
        for object in self.objects(subject, property):
            for o in self.transitive_objects(object, property, remember):
                yield o

    def transitive_subjects(self, predicate, object, remember=None):
        if remember is None:
            remember = {}
        if object in remember:
            return
        remember[object] = 1
        yield object
        for subject in self.subjects(predicate, object):
            for s in self.transitive_subjects(predicate, subject, remember):
                yield s

    def toPython(self):
        return self

    def triples_choices(self, triple, context=None):
        subject, predicate, object_ = triple
        for (s, p, o), cg in self.store.triples_choices((subject, predicate, object_), context=self):
            yield s, p, o

    @staticmethod
    def _assertnode(*terms):
        for t in terms:
            assert isinstance(t, Node), "Term %s must be an rdflib term" % (t)
        return True

    def _get_identifier(self):
        return self.__identifier
    identifier = property(_get_identifier)

    def _set_namespace_manager(self, namespace_manager):
        self.__namespace_manager = namespace_manager

    def _get_store(self):
        return self.__store
    store = property(_get_store)

    def _process_skolem_tuples(self, target, func):
        for t in self.triples((None, None, None)):
            target.add(func(t))

    def __add__(self, other):
        retval = Graph()
        for (prefix, uri) in set(list(self.namespaces()) + list(other.namespaces())):
            retval.bind(prefix, uri)
        for x in self:
            retval.add(x)
        for y in other:
            retval.add(y)
        return retval

    def __cmp__(self, other):
        if other is None:
            return -1
        elif isinstance(other, Graph):
            return (self.identifier > other.identifier) - (self.identifier < other.identifier)
        else:
            return 1

    def __contains__(self, triple):
        for triple in self.triples(triple):
            return True
        return False

    def __eq__(self, other):
        return isinstance(other, Graph) and self.identifier == other.identifier

    def __ge__(self, other):
        return self > other or self == other

    def __getitem__(self, item):
        pass

    def __gt__(self, other):
        return (isinstance(other, Graph) and self.identifier > other.identifier) or (other is not None)

    def __hash__(self):
        return hash(self.identifier)

    def __iadd__(self, other):
        self.addN((s, p, o, self) for s, p, o in other)
        return self

    def __init__(self, store='default', identifier=None, namespace_manager=None, base=None):
        pass

    def __isub__(self, other):
        for triple in other:
            self.remove(triple)
        return self

    def __iter__(self):
        return self.triples((None, None, None))

    def __le__(self, other):
        return self < other or self == other

    def __len__(self):
        return self.__store.__len__(context=self)

    def __lt__(self, other):
        return (other is None) or (isinstance(other, Graph) and self.identifier < other.identifier)

    def __mul__(self, other):
        retval = Graph()
        for x in other:
            if x in self:
                retval.add(x)
        return retval

    def __reduce__(self):
        return (Graph, (self.store, self.identifier))
        
    def __repr__(self):
        return '<Graph identifier=%s (%s)>' % (self.identifier, type(self))

    def __str__(self):
        if isinstance(self.identifier, URIRef):
            return ('%s a rdfg:Graph;rdflib:storage ' + "[a rdflib:Store;rdfs:label '%s'].") % (self.identifier.n3(), self.store.__class__.__name__)
        else:
            return ('[a rdfg:Graph;rdflib:storage ' + "[a rdflib:Store;rdfs:label '%s']].") % self.store.__class__.__name__

    def __sub__(self, other):
        retval = Graph()
        for x in self:
            if x not in other:
                retval.add(x)
        return retval

    def __xor__(self, other):
        return (self - other) + (other - self)

    __and__ = __mul__
    __or__ = __add__
