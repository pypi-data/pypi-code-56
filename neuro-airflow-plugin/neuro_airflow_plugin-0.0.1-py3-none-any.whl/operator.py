import asyncio
import logging
import textwrap
import time
from dataclasses import replace
from datetime import datetime
from types import MappingProxyType
from typing import (
    Any,
    AsyncIterator,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

from airflow.models import BaseOperator, BaseOperatorLink, TaskInstance
from airflow.utils.decorators import apply_defaults
from neuromation.api import (
    Client,
    Container,
    HTTPPort,
    JobDescription,
    JobStatus,
    RemoteImage,
    Resources,
    Volume,
)
from typing_extensions import TypedDict

from .hook import NeuroHook


log = logging.getLogger(__name__)


JOB_POLL_INTERVAL = 0.2
JOB_REPORT_INTERVAL = 10
EX_PLATFORMERROR = 125  # neuro platform misfunctioning
MAX_LOG_BUFFER = 16 * 1025  # max line size to wait for


class JobExtraKw(TypedDict, total=False):
    # TODO: Remove after cleanup, backward compatibility
    tags: Sequence[str]
    description: str
    life_span: Optional[float]
    environ: Mapping[str, str]
    entrypoint: str
    http_port: Optional[int]
    http_auth: bool
    tty: bool


def _to_xcom_value(job: JobDescription, exit_code: Optional[int]) -> Dict[str, Any]:
    return {
        "id": job.id,
        "exit_code": exit_code,
        "status": job.status.value,
        "http_url": str(job.http_url),
    }


class JobFailed(RuntimeError):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message, exit_code)
        self.exit_code = exit_code


class NeuroRunOperator(BaseOperator):

    ui_color = "#fafafa"
    ui_fgcolor = "#3c013f"

    template_fields = (
        "job_command",
        "job_image",
        "job_volumes",
        "job_name",
        "job_resources_preset",
        "job_tags",
        "job_environ",
        "job_entrypoint",
        "job_description",
        "job_http_port",
        "neuro_conn_id",
    )

    @apply_defaults
    def __init__(
        self,
        job_command: str,
        job_image: Union[str, RemoteImage],
        *,
        job_volumes: Sequence[Union[str, Volume]] = (),
        job_name: Optional[str] = None,
        job_resources_preset: Optional[str] = None,
        job_resources: Optional[Resources] = None,
        job_is_preemptible: Optional[bool] = None,
        job_extshm: Optional[bool] = None,
        job_tags: Optional[Sequence[str]] = None,
        job_description: Optional[str] = None,
        job_lifespan: Optional[float] = None,
        job_environ: Optional[Mapping[str, str]] = None,
        job_entrypoint: Optional[str] = None,
        job_http_port: Optional[str] = None,
        job_http_auth: Optional[bool] = None,
        job_tty: Optional[bool] = None,
        job_detach: bool = True,
        neuro_conn_id: str = "neuro_default",
        kill_on_error: bool = False,
        raise_on_errno: bool = True,
        # TODO: remove
        job_kw: JobExtraKw = cast(JobExtraKw, MappingProxyType({})),
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.neuro_conn_id = neuro_conn_id

        if job_resources_preset is not None and job_resources is not None:
            raise ValueError(
                "You need to specify `job_resources_preset` or `job_resources`, "
                "not both."
            )

        # Technically a string is a Sequence[str], but lets block such input right away
        if isinstance(job_volumes, str):
            raise ValueError(
                f"job_volumes should be a Sequence[str] or Sequence[Volume]"
                f", not {type(job_volumes)}"
            )

        if job_kw is None:
            if "tags" in job_kw and job_tags is None:
                job_tags = job_kw["tags"]
            if "description" in job_kw and job_description is None:
                job_description = job_kw["description"]
            if "life_span" in job_kw and job_lifespan is None:
                job_lifespan = job_kw["life_span"]
            if "environ" in job_kw and job_environ is None:
                job_environ = job_kw["environ"]
            if "entrypoint" in job_kw and job_entrypoint is None:
                job_entrypoint = job_kw["entrypoint"]
            if "http_port" in job_kw and job_http_port is None:
                job_http_port = job_kw["http_port"]
            if "http_auth" in job_kw and job_http_auth is None:
                job_http_auth = job_kw["http_auth"]
            if "http_tty" in job_kw and job_tty is None:
                job_tty = job_kw["http_tty"]

        self.job_command = job_command
        self.job_image = job_image
        self.job_volumes = job_volumes
        self.job_name = job_name
        self.job_resources_preset = job_resources_preset
        self.job_resources = job_resources
        self.job_is_preemptible = job_is_preemptible
        self.job_extshm = job_extshm
        self.job_tags = job_tags
        self.job_description = job_description
        self.job_lifespan = job_lifespan
        self.job_environ = job_environ
        self.job_entrypoint = job_entrypoint
        self.job_http_port = job_http_port
        self.job_http_auth = job_http_auth
        self.job_tty = job_tty
        self.job_detach = job_detach

        self._job_id: Optional[str] = None
        self._kill_on_error = kill_on_error
        self._raise_on_errno = raise_on_errno

        self._neuro_hook: Optional[NeuroHook] = None

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # NOTE: Context is the same dictionary used as when rendering jinja templates.

        # We create neuro hook on execute to allow templating of `neuro_conn_id`
        self._neuro_hook = neuro_hook = NeuroHook(self.neuro_conn_id)
        with neuro_hook:
            try:
                log.info("Successfully logged in to Neuro platform")
                return neuro_hook.run(self._execute(context, neuro_hook))
            except (Exception, KeyboardInterrupt) as err:
                neuro_hook.run(self._maybe_kill_job(err))
                raise

    def _prepare_volumes(self, client: Client) -> List[Volume]:
        volumes = []
        for volume_spec in self.job_volumes:
            if isinstance(volume_spec, Volume):
                volumes.append(volume_spec)
            else:
                volumes.append(client.parse.volume(volume_spec))
        return volumes

    def _prepare_resources(self, client: Client) -> Tuple[Resources, bool]:
        if self.job_resources_preset is not None:
            job_preset = client.config.presets[self.job_resources_preset]
            resources = Resources(
                memory_mb=job_preset.memory_mb,
                cpu=job_preset.cpu,
                gpu=job_preset.gpu,
                gpu_model=job_preset.gpu_model,
                tpu_type=job_preset.tpu_type,
                tpu_software_version=job_preset.tpu_software_version,
            )
            is_preemptible = job_preset.is_preemptible
            if self.job_extshm is not None:
                resources = replace(resources, shm=self.job_extshm)
        else:
            assert self.job_resources
            resources = self.job_resources
            if self.job_is_preemptible is None:
                # Default to not preemptible
                is_preemptible = False
            else:
                is_preemptible = self.job_is_preemptible
        return resources, is_preemptible

    def _prepare_image(self, client: Client) -> RemoteImage:
        if isinstance(self.job_image, RemoteImage):
            image = self.job_image
        else:
            image = client.parse.remote_image(self.job_image)
        return image

    async def _execute(
        self, context: Dict[str, Any], neuro_hook: NeuroHook
    ) -> Dict[str, Any]:
        client = neuro_hook.client
        volumes = self._prepare_volumes(client)
        resources, is_preemptible = self._prepare_resources(client)
        image = self._prepare_image(client)

        http = None
        if self.job_http_port is not None:
            http_port = int(self.job_http_port)
            http_auth = self.job_http_auth if self.job_http_auth is not None else True
            http = HTTPPort(int(http_port), http_auth)
        tty = self.job_tty if self.job_tty is not None else True

        container = Container(
            image=image,
            entrypoint=self.job_entrypoint,
            command=self.job_command,
            http=http,
            resources=resources,
            env=self.job_environ or {},
            volumes=list(volumes),
            tty=tty,
        )

        log.info(
            f"Starting job `{self.job_command}` "
            f"{self.job_image} with name={self.job_name}"
        )
        log.info(
            textwrap.dedent(
                f"""\
                Job details:
                is_preemptible: {is_preemptible}
                tags: {self.job_tags}
                description: {self.job_description}
                lifespan: {self.job_lifespan}
                container: {container}"""
            )
        )

        job = await client.jobs.run(
            container,
            is_preemptible=is_preemptible,
            name=self.job_name,
            tags=self.job_tags or (),
            description=self.job_description,
            life_span=self.job_lifespan,
        )

        log.info("Job assigned. Job id %s", job.id)
        self._job_id = job.id

        self.xcom_push(context, "assigned_job", _to_xcom_value(job, None))

        last_report = time.time()
        while job.status == JobStatus.PENDING:
            await asyncio.sleep(JOB_POLL_INTERVAL)
            job = await client.jobs.status(job.id)

            now = time.time()
            if now - last_report > JOB_REPORT_INTERVAL:
                log.info("Still starting...")
                last_report = now

        exit_code = None
        if not self.job_detach:
            log.info("Job successfully started. Starting log streaming from now on.")
            async for line in self._yield_log_lines(client, job.id):
                log.info(line)
            job = await client.jobs.status(job.id)
            while job.status in (JobStatus.PENDING, JobStatus.RUNNING):
                await asyncio.sleep(JOB_POLL_INTERVAL)
                job = await client.jobs.status(job.id)
            exit_code = job.history.exit_code
        else:
            log.info("Job successfully started. Continuing in detached mode.")
            # Even if we detached, but the job has failed to start
            # (most common reason - no resources), the command fails
            if job.status == JobStatus.FAILED:
                exit_code = EX_PLATFORMERROR

        if exit_code and self._raise_on_errno:
            raise JobFailed(
                f"Job returned a non-zero exit code: {exit_code}", exit_code
            )

        return _to_xcom_value(job, exit_code)

    async def _yield_log_lines(self, client: Client, job_id: str) -> AsyncIterator[str]:
        buffer = ""
        async for chunk in client.jobs.monitor(job_id):
            buffer += chunk.decode(errors="ignore")
            *lines, buffer = buffer.split("\n")
            for line in lines:
                yield line

            # To avoid large buffer in memory we will dump large lines right away
            if len(buffer) > MAX_LOG_BUFFER:
                yield buffer
                buffer = ""
        # If no new line was at the end of job output
        if buffer:
            yield buffer

    async def _maybe_kill_job(self, err: BaseException) -> None:
        if (
            self._neuro_hook is not None
            and self._kill_on_error
            and self._job_id is not None
        ):
            log.info(
                f"Error during job execution: {err!r}. Job configured to be "
                "killed on error. Killing..."
            )
            job_id = self._job_id
            self._job_id = None
            await self._neuro_hook.client.jobs.kill(job_id)

    def on_kill(self) -> None:
        log.error("NeuroJobRun task killed, performing cleanup...")
        if self._neuro_hook is not None:
            self._neuro_hook.close()


class BrowseLink(BaseOperatorLink):
    name = "Browse"
    operators = [NeuroRunOperator]

    def get_link(self, operator: "NeuroRunOperator", dttm: datetime) -> str:
        ti = TaskInstance(task=operator, execution_date=dttm)
        job: Dict[str, Any] = ti.xcom_pull(
            task_ids=operator.task_id, key="assigned_job"
        )
        if job is None:
            raise ValueError("Job not started yet")
        if not job["http_url"]:
            raise ValueError("Job not configured with an http port exposed")
        return str(job["http_url"])
