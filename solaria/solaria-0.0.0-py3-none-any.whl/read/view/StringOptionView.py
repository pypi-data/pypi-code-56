from src.reading.interaction.prompt.Prompt import Prompt
from src.reading.view.View import View


class StringOptionView(View):
    """The simplest usable implementation of a View. Accepts strings as
    displayables and lists of strings as prompt data."""

    def display(self, displayable: str):
        print(displayable)

    def prompt(self, prompt: Prompt):
        prompt_data = prompt.get_prompt_data()
        assert(type(prompt_data) is list)  # expect a list (of strings)
        for option in prompt_data:
            print(option)
        return prompt.process_view_output(input())
