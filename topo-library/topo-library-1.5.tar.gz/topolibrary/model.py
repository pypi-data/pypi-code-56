"""Mongo data models."""


from mongoengine.fields import Document, StringField, DateTimeField, ListField, IntField, EmbeddedDocument


class RepoEvents(Document):
    """The repository events collection model.

    Attributes:
        event_type (StringField): The GitHub event type https://developer.github.com/v3/activity/event_types
        repo_name (StringField): The full name of the GitHub repo.
        timestamp (DateTimeField): The datetime timestamp of the event.
    """

    meta = {'allow_inheritance': True}

    # Static list of valid event types
    valid_event_types = ["ReleaseEvent", "PushEvent", "PullRequestEvent"]

    # Crawler fields
    event_type = StringField(required=True, regex=f"^({'|'.join(valid_event_types)})$")
    repo_name = StringField(required=True)
    timestamp = DateTimeField(required=True)


class LinterScanEvent(EmbeddedDocument):
    """A sub-document for static analysis events.

    Attributes:
        linter_name (StringField): The name of the linter that ran against the file.
        file_path (StringField): The full path of the file in the repo.
        errors_total (IntField): Total number of errors.
        warnings_total (IntField): Total number of warnings.
        linter_output (StringField): Full output from the linter.
    """
    linter_name = StringField()
    file_path = StringField()
    errors_total = IntField()
    warnings_total = IntField()
    linter_output = StringField()


class ReleaseEvent(RepoEvents):
    """The GitHub release events model."""

    def __init__(self):
        RepoEvents.__init__(self)
        self.event_type = "ReleaseEvent"


class PullRequestEvent(RepoEvents):
    """The GitHub pull requests events model."""

    def __init__(self):
        RepoEvents.__init__(self)
        self.event_type = "PullRequestEvent"


class PushEvent(RepoEvents):
    """The GitHub push events model.

    Attributes:
        sha (StringField): The SHA of the most recent commit on ref after the push.
        ref (StringField): The full git ref that was pushed. Example: refs/heads/master.
        content_flags (ListField, optional): Flags that matched the file content rules.
        filename_flags (ListField, optional): Flags that matched the filename rules.
        LinterScanEvents (Document): A sub-document for static analysis events.
    """

    def __init__(self):
        RepoEvents.__init__(self)
        self.event_type = "PushEvent"

    # Push fields
    sha = StringField(required=True)
    ref = StringField(required=True)

    # Crawler flags
    aspect_flags = ListField()
    filename_flags = ListField()

    # Linter fields
    linter_warnings_total = IntField()
    linter_errors_total = IntField()
    linter_events = ListField(field=LinterScanEvent)

    # Analysis fields
    investment_kpi = IntField()
    maturity_kpi = IntField()