"""Progress report printers."""


class ReportBase(object):
    COLUMN_NAMES = NotImplemented
    COLUMN_WIDTHS = NotImplemented
    ITERATION_FORMATS = NotImplemented

    @classmethod
    def print_header(cls):
        fmt = ("|"
               + "|".join(["{{:^{}}}".format(x) for x in cls.COLUMN_WIDTHS])
               + "|")
        separators = ['-' * x for x in cls.COLUMN_WIDTHS]
        print(fmt.format(*cls.COLUMN_NAMES))
        print(fmt.format(*separators))

    @classmethod
    def print_iteration(cls, *args):
        # args[3] is obj func. It should really be a float. However,
        # trust-constr typically provides a length 1 array. We have to coerce
        # it to a float, otherwise the string format doesn't work.
        args = list(args)
        args[3] = float(args[3])

        iteration_format = ["{{:{}}}".format(x) for x in cls.ITERATION_FORMATS]
        fmt = "|" + "|".join(iteration_format) + "|"
        print(fmt.format(*args))

    @classmethod
    def print_footer(cls):
        print()


class BasicReport(ReportBase):
    COLUMN_NAMES = ["niter", "f evals", "CG iter", "obj func", "tr radius",
                    "opt", "c viol"]
    COLUMN_WIDTHS = [7, 7, 7, 13, 10, 10, 10]
    ITERATION_FORMATS = ["^7", "^7", "^7", "^+13.4e",
                         "^10.2e", "^10.2e", "^10.2e"]


class SQPReport(ReportBase):
    COLUMN_NAMES = ["niter", "f evals", "CG iter", "obj func", "tr radius",
                    "opt", "c viol", "penalty", "CG stop"]
    COLUMN_WIDTHS = [7, 7, 7, 13, 10, 10, 10, 10, 7]
    ITERATION_FORMATS = ["^7", "^7", "^7", "^+13.4e", "^10.2e", "^10.2e",
                         "^10.2e", "^10.2e", "^7"]


class IPReport(ReportBase):
    COLUMN_NAMES = ["niter", "f evals", "CG iter", "obj func", "tr radius",
                    "opt", "c viol", "penalty", "barrier param", "CG stop"]
    COLUMN_WIDTHS = [7, 7, 7, 13, 10, 10, 10, 10, 13, 7]
    ITERATION_FORMATS = ["^7", "^7", "^7", "^+13.4e", "^10.2e", "^10.2e",
                         "^10.2e", "^10.2e", "^13.2e", "^7"]
