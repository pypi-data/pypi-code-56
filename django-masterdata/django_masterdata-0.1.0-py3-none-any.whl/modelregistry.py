from django.db.models import  SmallIntegerField, Case, When, Value, Q, Sum
from functools import reduce
import operator
from .issuetuple import IssueTuple
from .issuecount import IssueCount


class ModelRegistry:
    def __init__(self, model):
        '''Creates a registry for configuring and running checks against the provided model'''
        self.model = model
        self._checks = []

    def checks(self, *checks):
        '''Sets the checks for the registered model'''
        self._checks = checks

    def gen_issues(self):
        '''IssueTuple generator for (obj, check) pairs for all
        triggered checks'''
        objs = self._issues_queryset()
        return (
            IssueTuple(
                obj=obj,
                check=check,
            )
            for alias, check in self.get_aliased_checks()
            for obj in objs
            if getattr(obj, f'{alias}_triggered')
        )

    def gen_aliased_issue_counts(self):
        '''IssueCount generator for all triggered checks'''
        counts = self._issues_queryset().aggregate(**{
            alias: Sum(f'{alias}_triggered')
            for alias, check in self.get_aliased_checks()
        })

        return (
            (alias, IssueCount(check, counts[alias]))
            for alias, check in self.get_aliased_checks()
            if counts[alias]
        )

    def _issues_queryset(self):
        '''Selects shallow objects (ids only) that trigger any of the configured checks'''
        if not self._checks:
            return self.model.objects.none()
        else:
            return self.model.objects.only('pk').annotate(
                **{
                    alias: check.expression
                    for alias, check
                    in self.get_aliased_checks()
                }
            ).annotate(
                **{
                    f'{alias}_triggered' : Case(
                        When(check.condition(alias), then=1),
                        default=0,
                        output_field=SmallIntegerField()
                    )
                    for alias, check
                    in self.get_aliased_checks()
                }
            ).filter(
                reduce(operator.or_, (
                    Q(**{f'{alias}_triggered': 1})
                    for alias, check in self.get_aliased_checks()
                ))
            )

    def get_aliased_checks(self):
        '''Get a stable field name for alias referencing the check throughout internal querying
        along with the actual Check'''
        return ((f'check_{i}', check) for i, check in enumerate(self._checks))
