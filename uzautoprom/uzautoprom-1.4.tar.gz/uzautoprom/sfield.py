"""
MIT License

Copyright (c) 2020 LidaRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Dict

from .abc import Field


class StrictlessField(Field):
    """StrictlessField is built-in realization of Field abc,
       which match criteria is that contract field should
       contain FullMatchField _value attribute data.

    """

    __slots__ = ["_name", "_value"]

    def __init__(self, name: str, value: str):
        self._name = str(name)
        self._value = str(value)

    def is_match(self, contract: Dict[str, str]) -> bool:
        if self._name in contract:
            return self._value in contract[self._name]
        return False


__all__ = ["StrictlessField"]
