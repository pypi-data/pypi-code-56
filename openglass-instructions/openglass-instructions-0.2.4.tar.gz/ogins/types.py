class ArgumentType:
    def __init__(self, name, length):
        self.name = name
        self.length = length


PTR = ArgumentType('ptr', 4)
BYTE = ArgumentType('byte', 1)
INT = ArgumentType('int', 2)
LONG = ArgumentType('long', 4)


class Argument:
    def __init__(self, name, type):
        self.type = type
        self.name = name


class Instruction:
    def __init__(self, name, opcode, args):
        self.name = name
        self.opcode = opcode
        self.args = args

