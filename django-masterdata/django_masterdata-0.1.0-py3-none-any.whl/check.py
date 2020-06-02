from django.db.models import Q
from django.db.models.expressions import BaseExpression
import re
from typing import Any, NamedTuple


re_whitespace = re.compile(r'\s+')


class NoTarget:
    pass


class Check(NamedTuple):
    name: str = None
    expression: BaseExpression = None
    operator: str = None
    target: Any = NoTarget
    positive_trigger: bool = True

    def as_expression(self, expression):
        return self.updated(expression=expression)

    def being(self, **kwargs):
        negated = kwargs.pop('negated', False)
        assert len(kwargs) == 1, 'Only a single clause is supported'
        (operator, target) = kwargs.popitem()
        return self.updated(operator=operator, target=target, positive_trigger=not negated)

    def not_being(self, **kwargs):
        return self.being(negated=True, **kwargs)

    def updated(self, **kwargs):
        return Check(**{
            **self._asdict(),
            **kwargs,
        })

    def filter(self, queryset):
        '''Filters a queryset selecting only triggered objects'''
        return queryset.annotate(check=self.expression).filter(self.condition('check'))

    def condition(self, alias):
        '''Return a Q() object evaluating this check's clause on the given alias'''
        cond = Q(**{f'{alias}__{self.operator}': self.target})
        return cond if self.positive_trigger else ~cond

    def get_signature(self):
        return '!'.join(map(
            lambda x: re_whitespace.sub('', str(x).lower()),
            (self.expression, self.operator, self.target)
        ))

    def debug(self):
        print('expression', self.expression)
        print('operator', self.operator)
        print('target', self.target)
        print('name', self.name)
        print(self.get_signature())
        return self
