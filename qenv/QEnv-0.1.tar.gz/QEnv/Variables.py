class EnvironVariable:

    def __init__(self):

        self.__Name = None
        self.__Scope = None
        self.__Value = None
        self.__Type = None

    def Info(self, VariableName: str = None, VariableDataType: str = None, VariableScope: str = None, VariableReturnValue: classmethod = None):

        if VariableName == None or VariableScope == None or VariableReturnValue == None or VariableDataType == None: return self.__Name, self.__Scope, self.__Value, self.__Type

        else:

            self.__Name = '<' + VariableName + '>::'
            self.__Scope = VariableScope
            self.__Value = VariableReturnValue
            self.__Type = VariableDataType

    def Validate(self):

        if not self.__Name: raise TypeError('The name value for the variable must not be a nonetype object (Must be set to a value) this value must be a string')

        if not self.__Scope: raise TypeError('The scope value for the variable must not be a nonetype object (Must be set to a value) this value must be a string')

        if not self.__Value: raise TypeError('The value value for the variable must not be a nonetype object (Must be set to a value) this value must be a classmethod')

        if not self.__Type: raise TypeError('The datatype value for the variable must not be a nonetype object (Must be set to a value) this value must be a string')

class MyPathVariable(EnvironVariable):

    def __init__(self): self.Info('MyPath', 'string','global', self.DoVariable)

    def DoVariable(self, ctx): return ctx.currpath()

class MyNameVariable(EnvironVariable):

    def __init__(self): self.Info('MyName', 'string', 'global', self.DoVariable)

    def DoVariable(self, ctx): return ctx.username

class MyCommandUsageVariable(EnvironVariable):

    def __init__(self): self.Info('MyCommandUsage','string', 'global', self.DoVariable)

    def DoVariable(self, ctx): return ctx.CommandUsage

class MyScopeVariable(EnvironVariable):

    def __init__(self): self.Info('MyScope', 'string', 'global', self.DoVariable)

    def DoVariable(self, ctx): return ctx.currscope()

def Package():

    return [MyPathVariable, MyNameVariable, MyScopeVariable, MyCommandUsageVariable]