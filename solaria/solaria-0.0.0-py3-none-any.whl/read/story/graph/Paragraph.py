

class Paragraph:
    """A Paragraph is a "position" in a GraphStory that a Reader can be
    in.

    Paragraphs display prompts upon reader entry depending upon the
    Reader state. A Paragraph has zero or more directed edges, called
    Phrases, that direct to a destination Paragraph. This new Paragraph
    can be the origin Paragraph. A Paragraph also has zero or more
    Phrases that feed into it.

    The Paragraph has a field called conditional_prompts which is a list
    of maps from determiners to prompts. prompt_conditionally returns
    the corresponding prompt, or a default prompt.

    The inhabiting of a Paragraph never deviates from this prescription:
      - The Paragraph accepts the Reader, and prints out a prompt
        depending on the Reader's state.
      - The reader (lowercase R) produces an input.
      - The Paragraph sends that input off to the interpreter, along
        with some information about itself. TODO clarify this and below
      - Based on the response from the interpreter, the Paragraph either
        prints out some kind of error-style message or sends a user down
        a Phrase.

    A Paragraph also has the additional layer property. Layers are a
    field in a Paragraph that allows a Reader to inhabit multiple
    Paragraphs at once. This is accomplished by two or more Phrases
    pointing away from the same Paragraph having the same name, all
    pointing to Paragraphs from different layers. It is illegal to have
    two Phrases of the same name and source paragraph directed towards
    Paragraphs on the same layer.
    """

    def __init__(self):
        """Initializes this Paragraph with an empty conditional_print dict."""
        self.__init__([])
        self.conditional_prompts = None  # NOTE do this REALLY need inclusion?

    def __init__(self, conditional_prompts):
        """Initializes this Paragraph with a Reader property to response
        dict"""
        assert type(conditional_prompts, list)  # NOTE this good?
        self.conditional_prompts = conditional_prompts

    # NOTE see above docs
    def accept_reader(self, reader):
        assert type(reader, dict)
        self.prompt_conditionally(reader)

    def prompt_conditionally(self, reader):
        """Returns the correct prompt for this paragraph depending on the
        Reader's stats
        """
        for condition in self.conditional_prompts:
            pass  # print conditional_prompt if reader passes condition
            # TODO require condition has default prompt, or code that in?
        return ""

    # TODO function for determining if Reader satisfies condition

    # TODO maybe add some stuff with IDs and whatever
