from typing import Optional


class TaskDataProcessor:
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, limit_length: Optional[int] = None):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, limit_length: Optional[int] = None):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()
