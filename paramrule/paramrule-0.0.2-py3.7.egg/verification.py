from paramrule.rule import *


class Helper:
    """
    Format verification help class
    """

    # Parameter dictionary
    _dict_parameter = None
    # Check configuration
    _configs = None
    # Built in verification rules
    _rules = [Required(), Ban(), Length(), Range(), DateTime(), Regexp()]

    def __init__(self, dict_parameter, configs):
        """
        Initialize verification help tool class
        :param dict_parameter: Parameter dictionary
        :param configs: Rule dictionary
        """
        self._dict_parameter = dict_parameter
        self._configs = configs

    def check(self):
        """
        Verify parameters
        :return: Verification result
        """
        for config in self._configs.items():
            name = config[0]
            # Split expression
            exprs = config[1].split(";")

            # Rule matching flag bit
            flag = False
            for expr in exprs:
                for rule in self._rules:
                    if not rule.know(expr):
                        continue
                    flag = True
                    b, message = rule.check(expr, self._dict_parameter, name)
                    if not b:
                        return b, message
                    break
            if not flag:
                return False, "Validation rule does not exist"
        return True, "success"
