"""The base module contains base classes for the Ivory system."""
import copy
import inspect
from typing import Callable, Dict

import ivory.core.collections
from ivory import utils
from ivory.core import default, instance


class Base(ivory.core.collections.Dict):
    """Base class for entities such as `client`, `experiment`, and `run`. """

    def __init__(self, params=None, **objects):
        super().__init__()
        self.params = params
        self.id = self.name = self.source_name = ""
        if "id" in objects:
            self.id = objects.pop("id")
        if "name" in objects:
            self.name = objects.pop("name")
        if "source_name" in objects:
            self.source_name = objects.pop("source_name")
        self.dict = objects

    def __repr__(self):
        args = []
        if self.id:
            args.append(f"id={self.id!r}")
        if self.name:
            args.append(f"name={self.name!r}")
        args.append(f"num_objects={len(self)}")
        args = ", ".join(args)
        return f"{self.__class__.__name__}({args})"


class Creator(Base):
    """Creator class to create `run` objects."""

    @property
    def experiment_id(self):
        return self.params["experiment"]["id"]

    @property
    def experiment_name(self):
        return self.params["experiment"]["name"]

    def create_params(self, args=None, name: str = "run", **kwargs):
        params = copy.deepcopy(self.params)
        if name not in params:
            params.update(default.get(name))
        update, args = utils.params.create_update(params[name], args, **kwargs)
        utils.params.update_dict(params[name], update)
        return params, args

    def create_run(self, args=None, name: str = "run", **kwargs):
        params, args = self.create_params(args, name, **kwargs)
        run = instance.create_base_instance(params, name, self.source_name)
        if self.tracker:
            from ivory.callbacks.pruning import Pruning

            run.set_tracker(self.tracker, name)
            run.tracking.log_params_artifact(run)
            args = {arg: utils.params.get_value(run.params[name], arg) for arg in args}
            run.tracking.log_params(run.id, args)
            run.set(pruning=Pruning())
        return run

    def create_instance(self, instance_name: str, args=None, name="run", **kwargs):
        params, _ = self.create_params(args, name, **kwargs)
        return instance.create_instance(params[name], instance_name)


class Callback:
    """Callback class for the Ivory callback system."""

    METHODS = [
        "on_init_begin",
        "on_init_end",
        "on_fit_begin",
        "on_epoch_begin",
        "on_train_begin",
        "on_train_end",
        "on_val_begin",
        "on_val_end",
        "on_epoch_end",
        "on_fit_end",
        "on_test_begin",
        "on_test_end",
    ]

    ARGUMENTS = ["run"]

    def __init__(self, caller: "CallbackCaller", methods: Dict[str, Callable]):
        self.caller = caller
        self.methods = methods

    def __repr__(self):
        class_name = self.__class__.__name__
        callbacks = list(self.methods.keys())
        return f"{class_name}({callbacks})"

    def __call__(self):
        caller = self.caller
        for method in self.methods.values():
            method(caller)


class CallbackCaller(Creator):
    """Callback caller class."""

    def create_callbacks(self):
        """Creates callback functions and store them in the dict-object."""
        for method in Callback.METHODS:
            methods = {}
            for key in self:
                if hasattr(self[key], method):
                    callback = getattr(self[key], method)
                    if callable(callback):
                        parameters = inspect.signature(callback).parameters
                        if list(parameters.keys()) == Callback.ARGUMENTS:
                            methods[key] = callback

            self[method] = Callback(self, methods)


class Experiment(Creator):
    def set_tracker(self, tracker):
        if not self.id:
            self.id = tracker.create_experiment(self.name)
            self.params["experiment"]["id"] = self.id
        self.set(tracker=tracker)

    def create_task(self):
        return self.create_run(name="task")

    def create_study(self, args=None, **suggests):
        study = self.create_run(name="study")
        if isinstance(args, str) and args in study.objective:
            study.objective.suggests = {args: study.objective.suggests[args]}
            return study
        if args or suggests:
            study.objective.update(args, **suggests)
        return study
