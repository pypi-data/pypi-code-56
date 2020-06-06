from src.reading.interaction.Interaction import Interaction
from src.reading.interaction.SimpleInteraction import SimpleInteraction
from src.reading.interaction.prompt.InterpChainPrompt import InterpChainPrompt
from src.reading.story.Story import Story


class StringBuilderStory(Story):
    """A Story that concatenates and displays everything the reader has
    typed in. Expects a string as a result of the interaction."""

    def __init__(self):
        self.type_history = ""

    def turn_page(self, interaction_result) -> Interaction:
        self.type_history += str(interaction_result)
        return SimpleInteraction(
            self.type_history,
            InterpChainPrompt([], []))
