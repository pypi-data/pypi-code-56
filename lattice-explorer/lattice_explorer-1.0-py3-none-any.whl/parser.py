# Lattice Explorer
# Copyright (C) 2020  Dominik Vilsmeier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import functools
import re


# Each command must be on its own line.
COMMAND_TEMPLATE = (
    '''
    ^
    [ \t]*
    (?:
       (?P<label>[a-z][a-z0-9_.]*)
       [ \t]*
       :
       [ \t]*
    )?
    (?P<keyword>{keyword})
    [ \t]*
    ,
    [ \t]*
    (?P<arguments>.+?)
    ;
    $
    '''
)


def _compile_pattern(pattern):
    return re.compile(pattern, flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE)


COMMAND_PATTERN = _compile_pattern(COMMAND_TEMPLATE.format(keyword='[a-z0-9]+'))


find_all_csp = functools.partial(re.findall, re.compile('(?:{.*?}|".*?"|[^,])+'))
find_all_csp.__doc__ = 'Find all comma separated parts, skipping commas which are part of strings "" or arrays {}.'


def find_all_commands(text, *, keyword=None):
    pattern = (
        COMMAND_PATTERN
        if keyword is None
        else _compile_pattern(COMMAND_TEMPLATE.format(keyword=keyword))
    )
    for match in re.finditer(pattern, text):
        arg_pairs = (x.split('=', 1) for x in find_all_csp(match.groupdict()['arguments']))
        arg_pairs = (x if len(x) > 1 else (*x, 'true') for x in arg_pairs)
        arg_pairs = ((x.strip().lower(), y.strip()) for x, y in arg_pairs)
        yield {
            'label': match.groupdict()['label'],
            'keyword': match.groupdict()['keyword'],
            'arguments': dict(arg_pairs),
        }
