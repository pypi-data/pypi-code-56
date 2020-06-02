from airflow.models import DAG, DagRun
from shu.wrappers import DagRunWrapper, DagWrapper, Collection


class InteractionError(Exception):
    pass


class NotFound(InteractionError):
    def __init__(self, cls, key):
        super().__init__("No {} with key {}".format(cls.__name__, key))
        self.cls = cls
        self.key = key

    def to_dict(self):
        return {"object": self.cls.__name__, "key": self.key, "message": str(self)}


class AlreadyExists(InteractionError):
    def __init__(self, cls, key):
        super().__init__("Key {} for {} already exists".format(key, cls.__name__))
        self.cls = cls
        self.key = key

    def to_dict(self):
        return {"object": self.cls.__name__, "key": self.key, "message": str(self)}


class Interactions:
    def __init__(self, adapters):
        self._dag_run_repo = adapters["dag_run_repo"]
        self._dag_repo = adapters["dag_repo"]

    def find_dags(self, filters):
        cleaned = {k: v for (k, v) in filters.items() if v is not None}
        dags = self._dag_repo.find(cleaned)
        return Collection([DagWrapper(dag) for dag in dags])

    def create_dag_run(self, dag_id, data):
        dag = self._dag_repo.get(dag_id)
        if not dag:
            raise NotFound(DAG, dag_id)
        data["dag_id"] = dag_id

        wrapper = DagRunWrapper.from_dict(data)
        existing = self._dag_run_repo.get(dag_id, wrapper.dag_run.run_id)
        if existing is not None:
            raise AlreadyExists(DagRun, wrapper.dag_run.run_id)
        with self._dag_run_repo.transaction():
            self._dag_run_repo.store(wrapper.dag_run)
        return wrapper

    def find_dag_run(self, dag_id, filters):
        cleaned = {k: v for (k, v) in filters.items() if v is not None}
        dag = self._dag_repo.get(dag_id)
        if not dag:
            raise NotFound(DAG, dag_id)
        dag_runs = self._dag_run_repo.find(dag_id, cleaned)
        return Collection([DagRunWrapper(dag_run) for dag_run in dag_runs])
