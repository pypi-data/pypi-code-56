from src.reading.interaction.interpreter.Interpreter import Interpreter


class OptionInterpreter(Interpreter):
    """Has a Prompt with list data and a View. Receives user input. If
    the input is not an element of the Prompt data, prompts the reader
    again.
    """

    def __init__(self, prompt, view):
        assert(isinstance(prompt.get_prompt_data(), list))
        self.prompt = prompt
        self.view = view
        self.invalid_option_string = "Invalid option. Choose again: "

    def interpret(self, interpretable):
        """Check if interpretable is in option list, if not, prompt."""

        if interpretable in self.prompt.get_prompt_data():
            return interpretable
        else:
            self.view.display(self.invalid_option_string)
            return self.view.prompt(self.prompt)
