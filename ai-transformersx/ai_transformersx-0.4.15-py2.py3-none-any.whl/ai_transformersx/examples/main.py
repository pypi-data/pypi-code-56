import sys
from .tasks import *

from .examples_management import ExampleManagement

manager = ExampleManagement()
manager.register_tasks([
    ('news', NewsSegmentTask),
    ('sentiment', SentimentTask)
])

if __name__ == "__main__":
    manager.start_example_task()
