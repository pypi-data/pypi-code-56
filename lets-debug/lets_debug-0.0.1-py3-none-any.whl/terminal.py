import os
from time import time
from typing import Any, Dict, List

## Ferramentas o terminal

class _Terminal(object):

    class __Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    __count_names: List[Dict] = []

    def __write(self, txt, color=None, bold=True):
        if color is None:
            color = self.__Colors.OKBLUE
        print(f"{self.__Colors.BOLD if bold else ''}{color}{txt}{self.__Colors.ENDC}")

    def log(self, *args):
        for arg in args:
            self.__write(arg)
        if len(args) == 0:
            self.__write('...')

    def warn(self, *args):
        for arg in args:
            self.__write(arg, self.__Colors.WARNING)

    def error(self, *args):
        for arg in args:
            self.__write(arg, self.__Colors.FAIL)

    def clear(self, operacional_system='unix'):
        if operacional_system == 'unix':
            os.system('clear')
        elif operacional_system == 'win':
            os.system('cls')

    def success(self, *args):
        for arg in args:
            self.__write(arg, self.__Colors.OKGREEN)
        if len(args) == 0:
            self.__write('OK', self.__Colors.OKGREEN)

    def count(self, name='contador') -> int:
        i = next((self.__count_names.index(item) for item in self.__count_names if item['name'] == name), None)
        if i is None:
            dictionary = { 'name': name, 'count': 1 }
            self.__count_names.append(dictionary)
        else:
            dictionary = self.__count_names[i]
            dictionary['count'] += 1
            self.__count_names[i] = dictionary
        self.log(f"{dictionary['name']}: {dictionary['count']}")
        return dictionary['count']

    # É semelhante ao comando nativo assert, mas não para o programa, apenas imprime o callback
    def check_bool(self, boolean: bool, callback: Any):
        if not type(boolean) is bool:
            self.error("Terminal.check_bool: o argumento deve ser do tipo bool!")
        elif not boolean is True:
            self.warn(f"Checagem falhou: {callback}")

    def table(self, dictionary_list: List[Dict]):
        if not type(dictionary_list) is list:
            return self.error("Terminal.table: o argumento deve ser uma list de dicionários!")

        keys = []
        for d in dictionary_list:
            if not type(d) is dict:
                continue
            dk = d.keys()
            for k in dk:
                if not k in keys:
                    keys.append(k)

        values = [[] for i in range(len(keys))]
        for d in dictionary_list:
            if not type(d) is dict:
                continue
            for key in keys:
                if key in d:
                    values[keys.index(key)].append(d[key])

        max_blank_space = 15

        def check_length(text) -> str:
            s = str(text)
            if len(s) > max_blank_space - 2:
                s = s[:max_blank_space - 4] + '...'
            return s

        lines, header = [], ''
        for i in range(len(keys)):
            s = check_length(str(keys[i]) + ':')
            r = ''
            for n in range(max_blank_space - len(s)):
                r += ' ' if not n == max_blank_space - len(s) - 1 else f"{self.__Colors.OKBLUE}|{self.__Colors.ENDC}"
            header += f"{self.__Colors.BOLD}{self.__Colors.UNDERLINE}{self.__Colors.OKBLUE}{s}{self.__Colors.ENDC}{r}"
        lines.append(header)

        i = 0
        l = 0 if len(values) == 0 else len(values[0])
        for i in range(l):
            line = ''
            for arr in values:
                s = check_length(arr[i]) if i < len(arr) else '-'
                r = s
                for n in range(max_blank_space - len(s)):
                    r += ' ' if not n == max_blank_space - len(s) - 1 else f"{self.__Colors.OKBLUE}|{self.__Colors.ENDC}"
                line += r
            lines.append(line)

        for line in lines:
            print(line)

terminal = _Terminal()