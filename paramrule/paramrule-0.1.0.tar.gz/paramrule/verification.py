from string import Template

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
        # Keep compatible string configuration
        for key in self._configs:
            if isinstance(self._configs[key], str):
                cfg = []
                for expr in self._configs[key].split(";"):
                    cfg.append({"rule": expr})
                self._configs[key] = cfg

    def check(self):
        """
        Verify parameters
        :return: Verification result
        """
        for config in self._configs.items():
            name = config[0]
            # Split expression
            exprs = config[1]

            # Rule matching flag bit
            for expr in exprs:
                flag = False
                for rule in self._rules:
                    if not rule.know(expr["rule"]):
                        continue
                    flag = True
                    b = rule.check(expr["rule"], self._dict_parameter, name)
                    if not b:
                        if "message" in expr:
                            return False, Template(expr["message"])\
                                .substitute(rule=expr["rule"], name=name)
                        return False, Template("Parameter failed validation [rule=${rule}, name=${name}]")\
                            .substitute(rule=expr["rule"], name=name)
                    break
                if not flag:
                    tmp = "Unknown expression, please check validation rule [rule=${rule}, name=${name}]"
                    return False, Template(tmp).substitute(rule=expr["rule"], name=name)
        return True, "success"
