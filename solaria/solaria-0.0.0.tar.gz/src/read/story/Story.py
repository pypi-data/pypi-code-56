from src.reading.interaction.Interaction import Interaction


class Story(object):
    """TEMPLATE CLASS for Stories.

    A Story is something that produces Interactions and then uses the
    result of that Interaction to produce the next one.
    """

    def turn_page(self, interaction_result) -> Interaction:
        """Accepts the result of a previous Interaction and produces the next
        one. An input of None should always return the same thing, typically a
        desired initial state.

        Args:
            interaction_result: the result of the previous interaction, or None
                if this is the first call to turn_page.

        Returns:
            The next Interaction.
        """

        pass
