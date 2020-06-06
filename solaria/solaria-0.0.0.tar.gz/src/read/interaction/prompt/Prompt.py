

class Prompt(object):
    """TEMPLATE CLASS for Prompts.

    A Prompt is data to be displayed and a format to return a reader
    response in. The prompt data must be supported by the View. The View
    output accepted by this Prompt may undergo processing by zero or
    more Interpreters before returning.

    Examples include: [prompt data, view return data]
        - An array of strings, one of those strings
        - A filepath to a picture of a body, a string indicating a
          clicked body part
        - A typed string and an array of option strings, a string
          indicating which option string the typed string is most
          semantically similar to

    The Interpreters that are used to transform the View output into the
    Prompt's return data type can be any functions, as long as the data
    types chain together correctly. Note that those may themselves
    invoke Interactions.
    """

    def get_prompt_data(self):
        """
        Returns:
            The prompt data to be displayed by the View.
        """

        pass

    def process_view_output(self, view_output):
        """Accept reader output that has been processed a View, the form of
        which should not depend on the View. Shoves this view output through
        any interpreters it may have.

        Returns:
            Fully processed reader input to a read session.
        """

        pass
