import abc

class TaskListener(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def onTaskUpdate(self, task):
        raise NotImplementedError()

class Task():
    def __init__(self, listener, task_name, task_run_id):
        self.listener = listener

        self.task_name = task_name
        self.task_run_id = task_run_id

        self.task_status = None
        self.task_input = None
        self.task_output = None
        self.task_metadata = None

    def update(self, task_status=None, task_input=None, task_output=None, task_metadata=None):
        if task_status is not None:
            self.task_status = task_status
        if task_input is not None:
            self.task_input = task_input
        if task_output is not None:
            self.task_output = task_output
        if task_metadata is not None:
            self.task_metadata = task_metadata

        self.listener.onTaskUpdate(self)

        return self
