class Environ:

    class Context:

        def __init__(self, Environ):

            self.Environ = Environ
            self.username = self.Environ.EnvironRunnerName
            self.commandusage = self.Environ.CommandUsage

        def currscope(self): return self.Environ.CurrScope

        def currpath(self): return self.Environ.CurrPath

        def runinscope(self, Scope: str, Function: classmethod): return self.Environ.RunInScope(Scope, Function)

        def send(self, String: str): self.Environ.Send(String)

        def say(self, String: str): self.Environ.Say(String)

        def fixstring(self, String: str): return self.Environ.FixString(String)

        def scopevariables(self):

            Variables = []

            for Variable in self.__Environ.EnvironVariables:

                Variable = Variable()

                Variable.Validate()

                VariableInfo = Variable.Info()

                Variables.append(f'(NAME: {VariableInfo[0]}, SCOPE: {VariableInfo[1]}, VALUE: {str(VariableInfo[2](self))})')

            return ', '.join(Variables)

    def __init__(
            self,
            EnvironName: str = 'QEnv',
            EnvironScopeName: str = 'global',
            EnvironCommands: list = [],
            EnvironVariables: list = [],
                 ):

        import os, sys

        self.__InEnvironment = False
        self.CommandUsage = 0

        self.EnvironName = EnvironName
        self.EnvironScopeName = EnvironScopeName
        self.CurrScope = self.EnvironScopeName

        self.EnvironRunnerName = os.getlogin()

        self.EnvironCommands = EnvironCommands
        self.EnvironVariables = EnvironVariables

        from QEnv.Commands import Package as CP
        from QEnv.Variables import Package as VP

        [self.EnvironCommands.append(P) for P in CP()]
        [self.EnvironVariables.append(P) for P in VP()]

        self.CurrPath = os.get_exec_path()[0]

        self.Send = self.Send
        self.Say = self.Say
        self.Run = self.Run

        self.Context = self.Context(self)

    def Run(self):

        while True:

            self.__InEnvironment = True

            self.CommandUsage += 1

            Raw = input(f'{self.EnvironName}:{self.CurrScope} @ {self.CurrPath} >> ')
            self.Context.arguments = Raw.split(' ')

            RawArgs = Raw.split(' ')
            CookedArgs = self.FixString(Raw)
            Command = RawArgs[0]
            Args = RawArgs[1:]

            #Check commands
            for CommandClass in self.EnvironCommands:

                TheCommand = CommandClass()

                TheCommand.Validate()

                TheCommandInfo = TheCommand.Info()

                if TheCommandInfo[0].lower() == Command.lower():

                    self.UpdateContext(TheCommandInfo[1](self.Context))
                    break

                else: pass

        self.__InEnvironment = False

    def FixString(self, String: str):

        for VariableClass in self.EnvironVariables:

            TheVariable = VariableClass()

            TheVariable.Validate()

            TheVariableInfo = TheVariable.Info()

            if TheVariableInfo[0] in String and TheVariableInfo[1] in (self.EnvironScopeName, self.CurrScope):

                String = String.replace(TheVariableInfo[0], TheVariableInfo[3](self.Context))

        return String

    def Send(self, String: str): print(f'{self.EnvironName} ~ {self.CurrScope} >> {String}')

    def Say(self, String: str): print(String)

    def RunInScope(self, Scope: str, Func: classmethod):

        self.CurrScope = Scope
        F = Func(self.Context)
        self.CurrScope = self.EnvironScopeName
        return F


    def Command(self, Command: classmethod): self.EnvironCommands.append(Command)
    def Variable(self, Variable: classmethod): self.EnvironVariables.append(Variable)

    def SetCurrPath(self, Path: str):

        self.CurrPath = Path

    def UpdateContext(self, Context):

        if Context:

            self.__dict__ == Context.Environ.__dict__


        else: pass