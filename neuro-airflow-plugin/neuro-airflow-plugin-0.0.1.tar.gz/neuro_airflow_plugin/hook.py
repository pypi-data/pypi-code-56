import logging
import tempfile
from pathlib import Path
from types import TracebackType
from typing import AsyncIterator, Awaitable, Generator, Optional, Tuple, Type, TypeVar

import yarl
from airflow.hooks.base_hook import BaseHook
from neuromation.api import (
    DEFAULT_API_URL,
    Client,
    Config,
    Parser,
    get as neuro_get,
    login_with_token,
)

from .asyncio_tools import AsyncioRunner


T = TypeVar("T")

log = logging.getLogger(__name__)


def obfuscate(token: str, max_print_len: int = 10) -> str:
    if not token:
        return ""
    return "..." + token[-max_print_len:]


class NeuroHook(BaseHook):
    def __init__(
        self, connection_id: str = "neuro_default", *, debug: bool = False,
    ) -> None:
        self._connection_id = connection_id
        self._tmp_dir: Optional[tempfile.TemporaryDirectory[str]] = None
        self._client: Optional[Client] = None
        self._aio_runner = AsyncioRunner()
        super().__init__(debug)

    def run(self, coro: Awaitable[T]) -> T:
        return self._aio_runner.run(coro)

    def run_iter(self, aiter: AsyncIterator[T]) -> Generator[T, Optional[bool], bool]:
        return self._aio_runner.run_iter(aiter)

    def __enter__(self) -> None:
        try:
            self.login()
        except Exception:
            self.close()
            raise

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        self.close()

    def _connect(self) -> Tuple[str, yarl.URL, Optional[str]]:
        # Get neuro connection information from Airflow DB. Synchronous call...
        conn = self.get_connection(self._connection_id)
        extra = conn.extra_dejson

        if "api_url" in extra:
            api_url = yarl.URL(extra["api_url"])
        else:
            api_url = DEFAULT_API_URL

        cluster = None
        if "cluster" in extra:
            cluster = extra["cluster"]
        return extra["token"], api_url, cluster

    @property
    def config_path(self) -> Path:
        if self._tmp_dir is None:
            self._tmp_dir = tempfile.TemporaryDirectory(prefix="neuro")
        return Path(self._tmp_dir.name)

    def login(self) -> None:
        token, api_url, cluster = self._connect()
        log.info(
            f"Login to Neuro using token: {obfuscate(token)!r} "
            f"api_url: {str(api_url)!r}"
        )
        self._client = self.run(
            self._login(token=token, api_url=api_url, cluster=cluster)
        )

    async def _login(
        self, token: str, api_url: yarl.URL, cluster: Optional[str]
    ) -> Client:
        await login_with_token(token, path=self.config_path, url=api_url)
        client = await neuro_get(path=self.config_path)
        if cluster is not None:
            await client.config.switch_cluster(cluster)
        return client

    def close(self) -> None:
        if self._client is not None:
            self.run(self._client.close())
            self._client = None
        if self._tmp_dir is not None:
            self._tmp_dir.cleanup()
            self._tmp_dir = None
        # Cleanup asyncio loop
        self._aio_runner.close()

    def ensure_client(self) -> Client:
        if self._client is None:
            raise RuntimeError("You have to `login()` before calling any methods")
        return self._client

    @property
    def parse(self) -> Parser:
        client = self.ensure_client()
        return client.parse

    @property
    def config(self) -> Config:
        client = self.ensure_client()
        return client.config

    @property
    def client(self) -> Client:
        return self.ensure_client()
