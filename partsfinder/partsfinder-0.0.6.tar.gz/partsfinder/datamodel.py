#!/usr/bin/env python3

import pint
import math
import random

class Value(object):
    """
    Represent a single value of a single parameter like a package name, maximum operating voltage or working temperature range
    
    May contain an optional unit used for comparisons.
    """
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.ureg = kwargs['ureg']

        # This is the raw value text
        self.raw = kwargs['raw']
        self.unit = kwargs.get('unit', None)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        if unit is not None:            
            self._unit = unit
            self.value = self.ureg.parse_expression(self.raw)

            if self._unit.to_base_units().units != self.value.to_base_units().units:
                raise ValueError("Units in unit spec '{}' and value '{}' do not match".format(
                    self.unit, self.value
                ))
        else:
            self._unit = unit
            self.value = self.raw

    def __lt__(self, other):
        if self.unit:
            other = self.ureg.parse_expression(other)
        return self.value < other

    def __gt__(self, other):
        if self.unit:
            other = self.ureg.parse_expression(other)
        return self.value > other

    def __eq__(self, other):
        if self.unit:
            other = self.ureg.parse_expression(other)
        return self.value == other

    def __ne__(self, other):
        if self.unit:
            other = self.ureg.parse_expression(other)
        return self.value != other


class Parameter(object):
    """
    Represent a single parameter.
    
    A parameter has a backend-specific identifier, a human-readable name, an optional unit, and a list of possible values.

    A parameter becomes constrained after it's values are filtered in-place by the constrain() function. This is useful
    for the backend API as usually search queries require specifiying only those parameters which have explicit values selected
    (in other words are constrained).
    """
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.unit = kwargs.get('unit', None)
        self.values = kwargs.get('values', {})
        self.constrained = kwargs.get('constrained', False)

    @property
    def all_values(self):
        # Make a set to have unique values
        return set(map(lambda v: v.raw, self.values.values()))

    @property
    def example_values(self, k=None):
        if k is None:
            k = min(5, math.ceil(len(self.values)/20))

        return random.sample(list(self.all_values), k=k)

    def validate_value_text(self, s):
        if self.unit is None:
            return True
        
        try:
            qu = self.ureg.parse_expression(s)
        except:
            return False
        return qu.check(self.unit)

    def constrain(self, pred):
        nv = filter(lambda v: pred(v), self.values.values())
        self.values = dict(map(lambda v: (v.id, v), nv))
        self.constrained = True

    @property
    def queryp(self):
        value_ids = map(lambda v: v.id, self.values.values())
        return '{}:{}'.format(self.id, ','.join(value_ids))

class ParamSpace(dict):
    """Represent a parameter space"""
    def __init__(self, **kwargs):
        super(self.__class__, self)
        # This is needed for temperature units to work out of the box
        self.ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

    def find_param(self, _name):
        try:
            return next(filter(lambda p: p.name == _name, self.values()))
        except StopIteration:
            return None

    @property
    def constrained_params(self):
        return filter(lambda p: p.constrained, self.values())
