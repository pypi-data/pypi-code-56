from abc import ABC, abstractmethod

class Predicate(ABC):

    @abstractmethod
    def toQuery(self):
        pass

class SimplePredicate(Predicate):

    def __init__(self, exp):
        self._exp = exp

    def toQuery(self):
        return self._exp

class LogicalPredicate(object):

    def __new__(cls, clauses=None, *args, **kwargs):
        if cls is LogicalPredicate:
            raise TypeError("LogicalPredicate class may not be instantiated")
        else:
            return object.__new__(cls, *args, *kwargs)

    def __init__(self, clauses):
        if clauses:
            self._predicates = clauses
        else:
            self._predicates = []

    def addClause(self, predicate):
        self._predicates.append(predicate)

    def toQuery(self):
        if not self._predicates:
            raise ValueError
        return "(" + self._logical_operator.join([item.toQuery() for item in self._predicates]) + ")"

class AndPredicate(LogicalPredicate, Predicate):
    
    def __init__(self, clauses=None):
        LogicalPredicate.__init__(self, clauses)
        self._logical_operator = " AND " # Keep spaces to be able to use in join strings

class OrPredicate(LogicalPredicate, Predicate):

    def __init__(self, clauses=None):
        LogicalPredicate.__init__(self, clauses)
        self._logical_operator = " OR " # Keep spaces to be able to use in join strings
