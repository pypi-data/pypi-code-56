from src.reading.interaction.prompt.Prompt import Prompt


class InterpChainPrompt(Prompt):
    """A Prompt in which View output is processed by propagating through
    sequential interpreters."""

    def __init__(self, prompt_data, interpreters):
        """Initializes an InterpChainPrompt.

        Args:
            prompt_data: the data used by the View to prompt the reader.
            interpreters: a list of zero or more interpreters, in which the
                input type of the first is the View-agnostic View output, the
                output of the first is the input of the second, and so on.
        """

        self.prompt_data = prompt_data
        self.interpreters = interpreters

    def get_prompt_data(self):
        return self.prompt_data

    def process_view_output(self, view_output):
        """Processes view output by applying Interpreters sequentially.

        Args:
            view_output: View-agnostic unprocessed reader response.

        Returns:
            The result of the View's output being shoved through the
            Interpreter chain.
        """

        processed_output = view_output
        for interpreter in self.interpreters:
            processed_output = interpreter.interpret(processed_output)
        return processed_output
