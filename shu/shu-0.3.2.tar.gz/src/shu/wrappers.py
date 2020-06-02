import datetime as dt
from abc import ABC, abstractclassmethod, abstractmethod

import spectacular as spec
from airflow.models import DagRun


class Wrapper(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @abstractclassmethod
    def from_dict(cls, data):
        pass


class Collection:
    def __init__(self, xs):
        self.xs = xs

    def to_dict(self):
        return [x.to_dict() for x in self.xs]


def from_schedule_interval(schedule_interval):
    if schedule_interval is None:
        return None
    if isinstance(schedule_interval, dt.timedelta):
        return {"type": "seconds", "value": schedule_interval.total_seconds()}
    if isinstance(schedule_interval, str):
        return {"type": "cron", "value": schedule_interval}
    raise ValueError("Expected string or timedelta, got {}".format(schedule_interval))


def from_state(state):
    return state


class DagWrapper(Wrapper):
    def __init__(self, dag_model):
        self.dag_model = dag_model

    def to_dict(self):
        return {
            "dag_id": self.dag_model.dag_id,
            "is_paused": self.dag_model.is_paused,
            "is_active": self.dag_model.is_active,
            "schedule_interval": from_schedule_interval(
                self.dag_model.schedule_interval
            ),
        }

    def from_dict(self, data):
        raise NotImplementedError()


class DagRunWrapper(Wrapper):
    def __init__(self, dag_run):
        self.dag_run = dag_run

    @staticmethod
    def schema(context=spec.Context.CREATE, ignored=None):
        conf_spec = spec.any_value()
        conf_spec["example"] = {}
        schema = spec.obj(conf=conf_spec, run_id=spec.string(), dag_id=spec.string())
        return spec.select(schema, context, ignored=ignored or [])

    @classmethod
    def from_dict(cls, data):
        spec.validate(cls.schema(), data)
        # pylint: disable=unexpected-keyword-arg
        dag_run = DagRun(
            dag_id=data["dag_id"],
            run_id=data["run_id"],
            conf=data["conf"],
            external_trigger=True,
        )
        return cls(dag_run)

    def to_dict(self):
        return {
            "dag_id": self.dag_run.dag_id,
            "run_id": self.dag_run.run_id,
            "conf": self.dag_run.conf,
            # pylint: disable=protected-access; HACK
            "state": from_state(self.dag_run._state),
        }
