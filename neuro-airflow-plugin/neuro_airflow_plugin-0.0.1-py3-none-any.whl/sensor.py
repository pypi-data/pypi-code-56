import logging
from typing import Any, Callable, Dict, NoReturn, Optional, Sequence

from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from neuromation.api import JobDescription, JobStatus

from .hook import NeuroHook


log = logging.getLogger(__name__)


class NeuroJobSensor(BaseSensorOperator):

    ui_color = "#f7e1f9"
    ui_fgcolor = "#3c013f"

    template_fields = ("job_id", "neuro_conn_id")

    @apply_defaults
    def __init__(
        self,
        *,
        job_id: str,
        neuro_conn_id: str = "neuro_default",
        job_status_cb: Callable[[JobDescription], bool],
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.neuro_conn_id = neuro_conn_id
        self.job_status_cb = job_status_cb
        self.job_id = job_id.strip()

        self._neuro_hook: Optional[NeuroHook] = None

    def execute(self, context: Dict[str, Any]) -> NoReturn:
        try:
            super_exec: Callable[..., NoReturn] = super().execute
            super_exec(context)
        finally:
            if self._neuro_hook is not None:
                self._neuro_hook.close()

    def poke(self, context: Dict[str, Any]) -> bool:
        job_id = self.job_id

        neuro_hook = self._neuro_hook
        if neuro_hook is None:
            neuro_hook = NeuroHook(self.neuro_conn_id)
            neuro_hook.login()
            self._neuro_hook = neuro_hook

        log.info(f"Checking status for job_id={job_id}")
        client = neuro_hook.client
        job = neuro_hook.run(client.jobs.status(job_id))
        return self.job_status_cb(job)


class NeuroJobStatusSensor(NeuroJobSensor):

    ui_color = "#f7e1f9"
    ui_fgcolor = "#3c013f"

    template_fields = ("job_id", "neuro_conn_id")

    @apply_defaults
    def __init__(
        self,
        *,
        job_id: str,
        job_statuses: Sequence[JobStatus] = (JobStatus.SUCCEEDED, JobStatus.FAILED),
        neuro_conn_id: str = "neuro_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            job_id=job_id,
            neuro_conn_id=neuro_conn_id,
            job_status_cb=self._job_status_cb,
            **kwargs,
        )
        self._waiting_statuses = set(job_statuses)

    def _job_status_cb(self, job: JobDescription) -> bool:
        log.info(f"Status for job_id={job.id} is {job.status}")
        return job.status in self._waiting_statuses
