from src.reading.storyteller.Storyteller import Storyteller
from src.reading.story.Story import Story
from src.reading.view.View import View


class SimpleStoryteller(Storyteller):
    """Runs the simplest storytelling session."""

    def __init__(self, story: Story, view: View):
        self.story = story
        self.view = view

    def read(self):
        interaction_result = None
        while True:
            interaction_result \
                = self.story.turn_page(interaction_result)\
                .interact(self.view)
