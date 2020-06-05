
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import json
import jedi
import astroid
import re



class FunctionVariableChecker(BaseChecker):
    __implements__ = IAstroidChecker
    source = {}
    functiondefdict = {}
    classlist = {}
    linter_storage = None
    importedclasses = []
    stubsfile = ""
    setup = False
    name = 'FunctionVariable-notvalid'
    project = project = jedi.get_default_project()
    priority = -1
    msgs = {
        'E8104': (
            'No attribute "%s" found on class: "%s"',
            'function-variable-cant-be-found',
            'variable is not valid.'
            
        ),
        'E8105': (
            'No attribute "%s" found on class: "%s". Attribute could be "%s"?',
            'function-variable-is-incomplete',
            'variable is not valid.'
        ),
        'E8106': (
            'Boxwiseclass "%s" not found in imports, add "%s" to imports',
            'sphinx-docstring-class-not-found',
            'variable is not valid.'
        ),
    }

    def __init__(self, linter=None):
        super(FunctionVariableChecker, self).__init__(linter)

    def setup_after_pylintrc_read(self):
        try:
            try:
                self.stubsfile = self.linter_storage['sourcefile'] + "/stubs"
                self.project.added_sys_path = [self.stubsfile]
            except:
                print "jedi setup broke"

            try:
                with open(self.linter_storage['sourcefile']+ "/classlist.json") as json_file:
                    self.classlist = json.load(json_file)
                    
            except:
                print "classlist broke"
            self.setup = True
            print "setup variables works"
        except:
            print "setup variables broke"

    def visit_importfrom(self, node):
        try:
            for importclass in node.names:
                self.importedclasses.append(importclass[0])
        except:
            print "error occurred in visit_importfrom"
        return

    #do we need a variable dict on functiondef lvl(make dicts in dicts) or can we make a general one(current)
    def visit_functiondef(self, node):
        if not self.setup:
            self.setup_after_pylintrc_read()
        patt = r"\s*:type (\s*\S*): ([^[][\w]*)"
        if node.doc is None:
            print "node.doc is empty"
            return
        match = re.findall(patt,node.doc)
        try:
            for found in match:
                print(found[0])
                if found[0] in self.functiondefdict:
                    print("already exists")
                self.functiondefdict[found[0]] = found[1]
                if found[1] in self.classlist and found[1] not in self.importedclasses:
                    hint = "from " + self.classlist[found[1]] + " import " + found[1] 
                    self.add_message('sphinx-docstring-class-not-found', node=node,args=(found[1], hint))
                else:
                    print("not a boxwiseclass")
            print "funcclass"
        except:
            print "something in funcdef went wrong"



    def visit_attribute(self, node):
        try:
            inferred = list(node.expr.infer())
            if inferred[0] == astroid.Uninferable:
                print "in attribute"
                attribute = node.attrname
                code = "\n"
                linesofcode = 2
                if node.expr.name in self.functiondefdict:
                    namedclass = self.functiondefdict[node.expr.name]
                else:
                    print("name not found in dict")
                    return 
                print namedclass
                if namedclass in self.classlist:
                    code += "from " + self.classlist[namedclass] + " import " + namedclass + "\n"
                    linesofcode = 3
                else:
                    print "class: '" + namedclass +"' not found in classlist"
                comb = namedclass +"." + attribute
                code += comb
                print(code)
                script = jedi.Script(code, environment=jedi.api.environment.InterpreterEnvironment(),project = self.project)
                completions = script.complete(3, len(comb))
                if len(completions) == 0:
                    self.add_message('function-variable-cant-be-found', node=node, args=(attribute, namedclass))
                    return
                print completions[0].name != attribute
                if completions[0].name != attribute:
                    self.add_message('function-variable-is-incomplete', node=node,args=(attribute, namedclass,completions[0].name))
        except:
            print "function_variable_checker.visit_attribute broke"
            return
        return