import datetime
import re


class Rule:
    """
    Validation rule abstract class
    """

    def know(self, expr):
        """
        Identification verification rules
        :param expr: Rule expression
        :return: Boer
        """
        pass

    def check(self, expr, dic, name):
        """
        Verify expression and corresponding value
        :param expr: Rule expression
        :param dic: Original dictionary
        :param name: Parameter name
        :return: Verification results
        """
        pass


# Non empty calibration
class Required(Rule):
    def know(self, expr):
        return "required" == expr

    def check(self, expr, dic, name):
        b = name in dic
        if not b:
            return False, name + " Field cannot be empty"
        return True, "success"


# Empty calibration
class Ban(Rule):
    def know(self, expr):
        return "ban" == expr

    def check(self, expr, dic, name):
        b = name in dic
        if b:
            return False, name + " Parameter is disabled"
        return True, "success"


# String length verification
class Length(Rule):
    expr = "length"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, expr, dic, name):
        if name not in dic:
            return True, "success"
        value = dic[name]
        b = isinstance(value, str)
        if not b:
            return False, name + " error in type"
        length = len(value)
        minmax = expr[len(self.expr) + 1:len(expr) - 1].split("-")
        if length < int(minmax[0]) or length > int(minmax[1]):
            return False, name + " Illegal field length"
        return True, "success"


# Digital range verification
class Range(Rule):
    expr = "range"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, expr, dic, name):
        if name not in dic:
            return True, "success"
        value = dic[name]
        try:
            value = int(value)
            dic[name] = value
        except Exception as e:
            print(e)
            return False, name + " error in type"
        minmax = expr[len(self.expr) + 1:len(expr) - 1].split("-")
        if value < int(minmax[0]) or value > int(minmax[1]):
            return False, name + " Illegal field range"
        return True, "success"


# Time check
class DateTime(Rule):
    expr = "datetime"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, expr, dic, name):
        if name not in dic:
            return True, "success"
        value = dic[name]
        pattern = expr[len(self.expr) + 1:len(expr) - 1]
        try:
            value = datetime.datetime.strptime(value, pattern)
            dic[name] = value
        except Exception as e:
            print(e)
            return False, name + " error in type"
        return True, "success"


# Regular match check
class Regexp(Rule):
    expr = "regexp"

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, expr, dic, name):
        if name not in dic:
            return True, "success"
        value = dic[name]
        pattern = expr[len(self.expr) + 1:len(expr) - 1]
        search = re.search(pattern, value)
        if search is None:
            return False, name + " Illegal field format"
        start_end = search.span()
        if (start_end[1] - start_end[0]) != len(value):
            return False, name + " Illegal field format"
        return True, "success"
