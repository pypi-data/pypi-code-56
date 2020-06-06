class EnvironCommand:

    def __init__(self):

        self.__Trigger = None
        self.__DoCommand = None

    def Info(self, CommandTriggerWord: str = None, CommandFunc: classmethod = None):

        if CommandTriggerWord == None and CommandFunc == None: return self.__Trigger, self.__DoCommand

        else:

            self.__Trigger = CommandTriggerWord
            self.__DoCommand = CommandFunc

    def Validate(self):

        if not self.__Trigger: raise TypeError('The trigger value for the command must not be a nonetype object (Must be set to a value) this value must be a string')

        if not self.__Trigger: raise TypeError('The docommand value for the command must not be a nonetype object (Must be set to a value) this value must be a classmethod')

class LsCommand(EnvironCommand):

    def __init__(self): self.Info('ls', self.MyCommand)

    def MyCommand(self, ctx):

        from os import listdir

        ctx.send(', '.join(listdir(ctx.currpath())))

class CdCommand(EnvironCommand):

    def __init__(self): self.Info('cd', self.MyCommand)

    def MyCommand(self, ctx):

        from os.path import exists

        while len(ctx.arguments) < 4: ctx.arguments.append(None)

        try:

            if ctx.arguments[1] in ('/', '\\'): ctx.Environ.CurrPath = '\\'.join(ctx.currpath().split('\\')[:-1])

            elif exists(ctx.arguments[1]): ctx.Environ.CurrPath = ctx.arguments[1]

            else: ctx.send('That path does not exist')

        except:

            print('Invalid usage/syntax of/for command')

        return ctx

class ReadCommand(EnvironCommand):

    def __init__(self): self.Info('read', self.MyCommand)

    def MyCommand(self, ctx):

        filepath = ctx.arguments[0]

        with open(filepath, 'r') as file: ctx.say(file.read())

class DoCommand(EnvironCommand):

    def __init__(self): self.Info('do', self.MyCommand)

    def MyCommand(self, ctx): return ctx.runinscope('local-do', self.DoCommands)

    def DoCommands(self, ctx):

        while True:

            Command = input(f'DO ~ {ctx.currscope()} >> ')
            Commands = Command.split(' ')

            if Commands[0] == 'EXIT': break

            elif Commands[0] == 'LISTVARS': ctx.say(f'<< DO >> {"".join(ctx.scopevariables())}')

            elif Commands[0] == 'PRINT': ctx.say(f'<< DO >> ' + ctx.fixstring(' '.join(Commands[1:])))

            elif Commands[0] == 'PRINTRAW': ctx.say('<< DO >> ' + ' '.join(Commands[1:]))

            elif Commands[0] == 'SEARCHCTX':

                if Commands[1] in ctx.__dict__: ctx.say('<< DO >> ' + ctx.__dict__[Commands[1]])

                else: ctx.say(f'<< DO >> Nothing found in ctx for \'{Commands[1]}\'')

            else: ctx.say('<< DO >> You entered an unrecognised command')

        return ctx

def Package():

    return [LsCommand, CdCommand, ReadCommand, DoCommand]