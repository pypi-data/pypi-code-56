class Exists(Exception):
    pass


class LoadError(Exception):
    pass


class CommitError(Exception):
    pass


class RollbackError(Exception):
    pass