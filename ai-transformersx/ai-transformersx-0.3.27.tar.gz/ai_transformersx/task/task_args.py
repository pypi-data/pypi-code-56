from ai_transformersx.model.model_args import ModelArguments
from ai_transformersx.data.data_args import DataArguments
from ai_transformersx.train.training_args import TrainingArguments
from ..transformersx_base import *


@configclass
class TaskArguments:
    model_args: ModelArguments = ModelArguments()
    data_args: DataArguments = DataArguments()
    training_args: TrainingArguments = TrainingArguments()


def parse_tasks_args(extensionArgs=None) -> (TaskArguments,):
    task_args = TaskArguments()
    if extensionArgs is not None:
        if type(extensionArgs) == type:
            task_args.extension = extensionArgs()
        else:
            task_args.extension = extensionArgs
    return Arguments(TaskArguments()).parse(), task_args.extension
