

class Interaction(object):
    """TEMPLATE CLASS for Interactions.

    An Interaction is a sequence of displayables and prompts that
    display on a View in order. Interactions are created by Stories, but
    are not necessarily able to reference their creator. This class's
    single method returns instructions of some sort that tell the Story
    how to produce its next Interaction, or update its internal state if
    it has dynamic data.
    """

    def interact(self, view):
        """Interacts with the reader using a View.

        Uses reader responses to zero or more of this Interaction's prompts to
        construct an instruction set informing a Storyteller how to update its
        state.

        Returns:
            Instructions for the Story to use to produce its next Interaction
            and update its internal state if it has dynamic data.
        """

        pass
