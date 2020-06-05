import copy
import itertools
import collections
import os
import sys
import re
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

import six
import astroid
from astroid import decorators
from astroid import modutils
from pylint.interfaces import IAstroidChecker, INFERENCE, INFERENCE_FAILURE, HIGH
from pylint.utils import get_global_option
from pylint.checkers import BaseChecker
from pylint.checkers import utils
from pylint.checkers.variables import VariablesChecker

a = VariablesChecker()



MSGS = {
    'E0601': ('Using variable %r before assignment',
              'used-before-assignment',
              'Used when a local variable is accessed before it\'s \
              assignment.'),
    'E0602': ('Undefined variable %r',
              'undefined-variable',
              'Used when an undefined variable is accessed.'),
    'E0603': ('Undefined variable name %r in __all__',
              'undefined-all-variable',
              'Used when an undefined variable name is referenced in __all__.'),
    'E0604': ('Invalid object %r in __all__, must contain only strings',
              'invalid-all-object',
              'Used when an invalid (non-string) object occurs in __all__.'),
    'E0611': ('No name %r in module %r',
              'no-name-in-module',
              'Used when a name cannot be found in a module.'),

    'W0601': ('Global variable %r undefined at the module level',
              'global-variable-undefined',
              'Used when a variable is defined through the "global" statement \
              but the variable is not defined in the module scope.'),
    'W0602': ('Using global for %r but no assignment is done',
              'global-variable-not-assigned',
              'Used when a variable is defined through the "global" statement \
              but no assignment to this variable is done.'),
    'W0603': ('Using the global statement', # W0121
              'global-statement',
              'Used when you use the "global" statement to update a global \
              variable. Pylint just try to discourage this \
              usage. That doesn\'t mean you cannot use it !'),
    'W0604': ('Using the global statement at the module level', # W0103
              'global-at-module-level',
              'Used when you use the "global" statement at the module level \
              since it has no effect'),
    'W0611': ('Unused %s',
              'unused-import',
              'Used when an imported module or variable is not used.'),
    'W0612': ('Unused variable %r',
              'unused-variable',
              'Used when a variable is defined but not used.'),
    'W0613': ('Unused argument %r',
              'unused-argument',
              'Used when a function or method argument is not used.'),
    'W0614': ('Unused import %s from wildcard import',
              'unused-wildcard-import',
              'Used when an imported module or variable is not used from a \
              `\'from X import *\'` style import.'),

    'W0621': ('Redefining name %r from outer scope (line %s)',
              'redefined-outer-name',
              'Used when a variable\'s name hides a name defined in the outer \
              scope.'),
    'W0622': ('Redefining built-in %r',
              'redefined-builtin',
              'Used when a variable or function override a built-in.'),
    'W0623': ('Redefining name %r from %s in exception handler',
              'redefine-in-handler',
              'Used when an exception handler assigns the exception \
               to an existing name'),

    'W0631': ('Using possibly undefined loop variable %r',
              'undefined-loop-variable',
              'Used when an loop variable (i.e. defined by a for loop or \
              a list comprehension or a generator expression) is used outside \
              the loop.'),

    'E0632': ('Possible unbalanced tuple unpacking with '
              'sequence%s: '
              'left side has %d label(s), right side has %d value(s)',
              'unbalanced-tuple-unpacking',
              'Used when there is an unbalanced tuple unpacking in assignment',
              {'old_names': [('W0632', 'unbalanced-tuple-unpacking')]}),

    'E0633': ('Attempting to unpack a non-sequence%s',
              'unpacking-non-sequence',
              'Used when something which is not '
              'a sequence is used in an unpack assignment',
              {'old_names': [('W0633', 'unpacking-non-sequence')]}),

    'W0640': ('Cell variable %s defined in loop',
              'cell-var-from-loop',
              'A variable used in a closure is defined in a loop. '
              'This will result in all closures using the same value for '
              'the closed-over variable.'),

    }



class VariablesChecker2(BaseChecker):
    """checks for
    * unused variables / imports
    * undefined variables
    * redefinition of variable from builtins or from an outer scope
    * use of variable before assignment
    * __all__ consistency
    """

    __implements__ = IAstroidChecker

    name = 'variables'
    msgs = MSGS
    priority = -1

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self._to_consume = []  # list of tuples: (to_consume:dict, consumed:dict, scope_type:str)
        self._checking_mod_attr = None
        self._loop_variables = []

    @utils.check_messages('redefined-outer-name')
    def visit_for(self, node):
        assigned_to = [var.name for var in node.target.nodes_of_class(astroid.AssignName)]


    def _ignore_class_scope(self,node):
        return a._ignore_class_scope(node)
    
    def _has_homonym_in_upper_function_scope(self, node, index):
        return a._has_homonym_in_upper_function_scope(node,index)

    def _check_late_binding_closure(self,node, assignment_node):
        return a._check_late_binding_closure(node, assignment_node)


    def _loopvar_name(self,node, name):
        return a._loopvar_name(node, name)

    @staticmethod
    def _is_variable_violation(node, name, defnode, stmt, defstmt,
                               frame, defframe, base_scope_type,
                               recursive_klass):
        return a._is_variable_violation(node, name, defnode, stmt, defstmt,
                               frame, defframe, base_scope_type,
                               recursive_klass)



    @utils.check_messages(*(MSGS.keys()))
    def visit_name(self, node):
        try:
            """check that a name is defined if the current scope and doesn't
            redefine a built-in
            """
            stmt = node.statement()
            if stmt.fromlineno is None:
                # name node from a astroid built from live code, skip
                assert not stmt.root().file.endswith('.py')
                return

            name = node.name
            frame = stmt.scope()
            # if the name node is used as a function default argument's value or as
            # a decorator, then start from the parent frame of the function instead
            # of the function frame - and thus open an inner class scope
            if ((utils.is_func_default(node) and not utils.in_comprehension(node)) or
                    utils.is_func_decorator(node) or utils.is_ancestor_name(frame, node)):
                # Do not use the highest scope to look for variable name consumption in this case
                # If the name is used in the function default, or as a decorator, then it
                # cannot be defined there
                # (except for list comprehensions in function defaults)
                start_index = len(self._to_consume) - 2
            else:
                start_index = len(self._to_consume) - 1
            # iterates through parent scopes, from the inner to the outer
            base_scope_type = self._to_consume[start_index].scope_type
            # pylint: disable=too-many-nested-blocks; refactoring this block is a pain.
            for i in range(start_index, -1, -1):
                current_consumer = self._to_consume[i]
                # if the current scope is a class scope but it's not the inner
                # scope, ignore it. This prevents to access this scope instead of
                # the globals one in function members when there are some common
                # names. The only exception is when the starting scope is a
                # comprehension and its direct outer scope is a class
                if current_consumer.scope_type == 'class' and i != start_index and not (
                        base_scope_type == 'comprehension' and i == start_index-1):
                    if self._ignore_class_scope(node):
                        continue

                # the name has already been consumed, only check it's not a loop
                # variable used outside the loop
                # avoid the case where there are homonyms inside function scope and
                if name in current_consumer.consumed and not (
                        current_consumer.scope_type == 'comprehension'
                        and self._has_homonym_in_upper_function_scope(node, i)):
                    defnode = utils.assign_parent(current_consumer.consumed[name][0])
                    self._check_late_binding_closure(node, defnode)
                    self._loopvar_name(node, name)
                    break

                found_node = current_consumer.get_next_to_consume(node)
                if found_node is None:
                    continue

                # checks for use before assignment
                defnode = utils.assign_parent(current_consumer.to_consume[name][0])
                if defnode is not None:
                    self._check_late_binding_closure(node, defnode)
                    defstmt = defnode.statement()
                    defframe = defstmt.frame()
                    # The class reuses itself in the class scope.
                    recursive_klass = (frame is defframe and
                                        defframe.parent_of(node) and
                                        isinstance(defframe, astroid.ClassDef) and
                                        node.name == defframe.name)

                    maybee0601, annotation_return, use_outer_definition = self._is_variable_violation(
                        node, name, defnode, stmt, defstmt,
                        frame, defframe,
                        base_scope_type, recursive_klass)

                    if use_outer_definition:
                        continue

                    if (maybee0601
                            and not utils.is_defined_before(node)
                            and not astroid.are_exclusive(stmt, defstmt, ('NameError',))):

                        # Used and defined in the same place, e.g `x += 1` and `del x`
                        defined_by_stmt = (
                            defstmt is stmt
                            and isinstance(node, (astroid.DelName, astroid.AssignName))
                        )
                        if (recursive_klass
                                or defined_by_stmt
                                or annotation_return
                                or isinstance(defstmt, astroid.Delete)):
                            if not utils.node_ignores_exception(node, NameError):
                                self.add_message('undefined-variable', args=name,
                                                    node=node)
                        elif base_scope_type != 'lambda':
                            # E0601 may *not* occurs in lambda scope.
                            self.add_message('used-before-assignment', args=name, node=node)
                        elif base_scope_type == 'lambda':
                            # E0601 can occur in class-level scope in lambdas, as in
                            # the following example:
                            #   class A:
                            #      x = lambda attr: f + attr
                            #      f = 42
                            if isinstance(frame, astroid.ClassDef) and name in frame.locals:
                                if isinstance(node.parent, astroid.Arguments):
                                    if stmt.fromlineno <= defstmt.fromlineno:
                                        # Doing the following is fine:
                                        #   class A:
                                        #      x = 42
                                        #      y = lambda attr=x: attr
                                        self.add_message('used-before-assignment',
                                                            args=name, node=node)
                                else:
                                    self.add_message('undefined-variable',
                                                        args=name, node=node)
                            elif current_consumer.scope_type == 'lambda':
                                self.add_message('undefined-variable',
                                                    node=node, args=name)

                current_consumer.mark_as_consumed(name, found_node)
                # check it's not a loop variable used outside the loop
                self._loopvar_name(node, name)
                break
            else:
                # we have not found the name, if it isn't a builtin, that's an
                # undefined name !
                if not (name in astroid.Module.scope_attrs or utils.is_builtin(name)
                        or name in self.config.additional_builtins):
                    if not utils.node_ignores_exception(node, NameError):
                        self.add_message('undefined-variable', args=name, node=node)
        except Exception as e:
            print(e)