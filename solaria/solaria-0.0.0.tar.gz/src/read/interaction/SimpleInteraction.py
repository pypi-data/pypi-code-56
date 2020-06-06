from src.reading.interaction.Interaction import Interaction
from src.reading.interaction.prompt.Prompt import Prompt
from src.reading.view.View import View


class SimpleInteraction(Interaction):
    """Displays one displayable and then presents one Prompt. Returns
    the string result of that Prompt."""

    def __init__(self, displayable, prompt: Prompt):
        self.displayable = displayable
        self.prompt = prompt

    def interact(self, view: View):
        view.display(self.displayable)
        return view.prompt(self.prompt)
