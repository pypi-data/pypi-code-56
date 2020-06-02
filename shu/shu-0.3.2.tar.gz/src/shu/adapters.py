from airflow.models import DagModel, DagRun


def _escape(pattern):
    return pattern.replace("_", r"\_")


class RepoTransaction:
    def __init__(self, session):
        self._session = session

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()
        return False  # Do not surpress the exception


class DagRunRepository:
    def __init__(self, session):
        self._session = session

    def transaction(self):
        return RepoTransaction(self._session)

    def store(self, run):
        self._session.add(run)

    def find(self, dag_id, filters):
        query = self._session.query(DagRun).filter(DagRun.dag_id == dag_id)
        if "prefix" in filters:
            pattern = _escape("{}%".format(filters["prefix"]))
            query = query.filter(DagRun.run_id.like(pattern))
            del filters["prefix"]
        return query.filter_by(**filters).all()

    def get(self, dag_id, run_id):
        query = self._session.query(DagRun).filter(
            DagRun.dag_id == dag_id, DagRun.run_id == run_id
        )
        return query.one_or_none()


class DagRepository:
    def __init__(self, session):
        self._session = session

    def transaction(self):
        return RepoTransaction(self._session)

    def find(self, filters):
        query = self._session.query(DagModel)
        if "prefix" in filters:
            pattern = _escape("{}%".format(filters["prefix"]))
            query = query.filter(DagModel.dag_id.like(pattern))
            del filters["prefix"]
        return query.filter_by(**filters).all()

    def get(self, dag_id):
        query = self._session.query(DagModel).filter(DagModel.dag_id == dag_id)
        return query.one_or_none()


def create_adapters(session):
    return {
        "dag_run_repo": DagRunRepository(session),
        "dag_repo": DagRepository(session),
    }
