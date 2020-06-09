"""Implements worker classes.

Classes:
Worker
"""

import json

from .utils import echo


class Worker:
    """Basic worker class.

    Example Usage:
        task = AdderTask()
        worker = Worker(task=task)
        worker.start()
    """

    def __init__(self, task):
        self.task = task
        self.waiting = False

    def start(self):
        """Begin working on the assigned type of task."""
        while True:
            try:
                # Read database.
                dequeued_item = self.task.dequeue()
                if not dequeued_item:
                    if not self.waiting:
                        echo(f"Waiting for next task... (Ctrl + C to quit)\n")
                        self.waiting = True
                    continue
                self.waiting = False
                self.task.set_status('dequeued')
                task_id, _, _, _, task_args, task_kwargs = dequeued_item
                task_args = json.loads(task_args)
                task_kwargs = json.loads(task_kwargs)
                # Run.
                echo(f'Running task: {task_id}')
                self.task.set_status('running')
                self.task.run(*task_args, **task_kwargs)
                echo(f'Finished task: {task_id}\n')
                self.task.set_status('complete')
            except KeyboardInterrupt:
                self.quit()
                break

    def quit(self):
        """Stop working."""
        echo('Quitting')
