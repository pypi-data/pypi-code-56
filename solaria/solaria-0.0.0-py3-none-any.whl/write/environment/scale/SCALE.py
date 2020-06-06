from src.writing.environment.Environment import Environment


class SCALE(Environment):
    """SCALE: Solaria CommAnd Line Environment

    An Environment that stores a list of editors and TODO does file stuff
    """

    def __init__(self):
        """Initializes this SCALE with an empty list of editors, """
        self.editors = []

    def build(self):
        """See base class."""

        pass

    def add_draft_editor(self, draft, editor):
        """See base class."""

        pass
