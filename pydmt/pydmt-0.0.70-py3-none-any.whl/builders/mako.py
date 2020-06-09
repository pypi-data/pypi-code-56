import sys
from typing import List, Dict, Union

import mako
import mako.exceptions
import mako.lookup
import mako.template
import os

from pydmt.api.builder import Builder
from pydmt.utils.filesystem import makedirs_for_file
from pydmt.utils.digest import sha1_files


class Mako(Builder):
    def get_sources(self) -> List[str]:
        return [self.source]

    def __init__(self,
                 source: str,
                 target: str,
                 data: Union[Dict[str, object], None],
                 config_files: List[str],
                 snipplet_files: List[str],
                 ):
        super().__init__()
        self.source: str = source
        self.target: str = target
        self.data = data
        self.config_files: List[str] = config_files
        self.snipplet_files: List[str] = snipplet_files

    def get_signature(self) -> str:
        # TODO: currentl we work at the file level and so we sha1
        # the source file + all config files + all snipplet files
        # it would be much better to work at the variable level
        # and sha1 only the variables and the values which are actually
        # used in the source file.
        # and only add snipplet files which we actually use.
        return sha1_files(self.config_files + self.snipplet_files + [self.source])

    def build(self):
        try:
            lookup = mako.lookup.TemplateLookup(
                directories=['.'],
                input_encoding='utf-8',
                output_encoding='utf-8',
            )
            template = mako.template.Template(
                filename=self.source,
                lookup=lookup,
            )
            makedirs_for_file(self.target)
            if self.data is None:
                output = template.render()
            else:
                output = template.render(**self.data)
            with open(self.target, 'w') as file_handle:
                file_handle.write(output)
        except Exception as e:
            if os.path.isfile(self.target):
                os.unlink(self.target)
            raise e

    def get_targets(self) -> List[str]:
        return [self.target]


def print_full_exception():
    print('printing full exception')
    traceback = mako.exceptions.RichTraceback()
    for (filename, line_number, function_name, line) in traceback.traceback:
        print('File {0}, line {1}, in {2}'.format(filename, line_number, function_name))
        print(line)
    print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))


def print_exception(e, input_file):
    found = False
    traceback = mako.exceptions.RichTraceback()
    for (filename, line_number, function_name, line) in traceback.traceback:
        if filename == input_file:
            print('{0}: error {1} in {2}, line {3}'.format(sys.argv[0], str(e), filename, line_number, function_name))
            print('{0}'.format(line))
            found = True
    if not found:
        for (filename, line_number, function_name, line) in traceback.traceback:
            print('File {0}, line {1}, in {2}'.format(filename, line_number, function_name))
            print(line)
        print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))
