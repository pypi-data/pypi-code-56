

class Draft(object):
    """TEMPLATE CLASS for Drafts.

    A Draft can be thought of conceptually as a draft for a Story.
    While a Story is read-only, a Draft can be altered via an Editor,
    which provide different methods for viewing and altering the
    contents of a Draft.
    """

    def build(self):
        """Produce a Story from this Draft.

        Returns:
            A Story.
        """

        pass
