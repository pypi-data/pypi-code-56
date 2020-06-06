from src.writing.draft.Draft import Draft
from src.writing.editor.Editor import Editor


class Environment(object):
    """TEMPLATE CLASS for Environments.

    An Environment must be able to put Drafts and their Editors
    together to form Draft-Editor complexes. It must then allow a writer
    to use the Editor to alter the Draft.
    """

    def add_draft_editor(self, draft: Draft, editor: Editor):
        """Wire up Editor to Draft and add the complex to the Environment.
        Depending on the Environment, this can kick out the previous
        Draft-Editor or add it to a list.

        Args:
            draft: a draft to be edited
            editor: an editor capable of editing and displaying the draft
        """

        pass
