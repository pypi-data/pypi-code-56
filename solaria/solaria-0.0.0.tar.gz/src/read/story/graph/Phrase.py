

class Phrase:
    """A Phrase is a directed edge between one Paragraph and a second
    Paragraph. These two Paragraphs can be the same.

    The Phrase also has the ability to display text, but this should
    typically be short, with longer description left to Paragraphs. To
    identify themselves, Phrases have names that are unique with respect
    to a given source Paragraph and destination Paragraph-layer combo, but
    not necessarily unique globally. To clarify, this means that a
    Paragraph can have two Phrases with the same name, but only if those
    two Phrases are directed to Paragraphs sitting on different layers.

    The traversal of a Phrase can alter a Reader's stats or can display
    text, but does not have to do either one.
    """

    def __init__(self):
        """Initialize this Phrase with an empty alteration function and
        prompt"""
        self.prompt = ""

    def accept_reader(self, reader):
        """Prints out this Phrase's prompt and alters the reader."""
        pass  # TODO how to represent alteration data?
