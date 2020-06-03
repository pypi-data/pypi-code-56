import sys
import asyncio

import httpx



from ._auth import Auth, AsyncAuth
from ._digi import Digi, AsyncDigi
from ._tools import Tools, AsyncTools
from ._snmp import SNMP, AsyncSNMP
from ._mac import Mac, AsyncMac
from ._cpe import CPE, AsyncCPE


class Client:

    def __init__(self, netauto_url: str, api_version: int, username: str, password: str, cert_path: str = ""):
        self._base_url = f"{netauto_url}/api/v{api_version}/"
        if cert_path:
            self._session = httpx.Client(verify=cert_path, base_url=self._base_url)
        else:
            self._session = httpx.Client(verify=False, base_url=self._base_url)

        self.auth = Auth(session=self._session, username=username, password=password)
        self.tools = Tools(session=self._session)
        self.digi = Digi(session=self._session)
        self.snmp = SNMP(session=self._session)
        self.mac = Mac(session=self._session)
        self.cpe = CPE(session=self._session)

    def __enter__(self):
        self.auth.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def close_session(self):
        self._session.close()


class AsyncClient:

    def __init__(self, netauto_url: str, api_version: int, username: str, password: str, cert_path: str = ""):
        self._base_url = f"{netauto_url}/api/v{api_version}/"
        pool_limits = httpx.PoolLimits(max_keepalive=10, max_connections=50)
        timeout = httpx.Timeout(connect_timeout=5, write_timeout=5, read_timeout=60, pool_timeout=60)
        settings = dict(base_url=self._base_url, pool_limits=pool_limits, timeout=timeout)

        if cert_path:
            self._session = httpx.AsyncClient(verify=cert_path, **settings)
        else:
            self._session = httpx.AsyncClient(verify=False, **settings)

        self.auth = AsyncAuth(session=self._session, username=username, password=password)
        self.tools = AsyncTools(session=self._session)
        self.digi = AsyncDigi(session=self._session)
        self.snmp = AsyncSNMP(session=self._session)
        self.mac = AsyncMac(session=self._session)
        self.cpe = AsyncCPE(session=self._session)

    async def __aenter__(self):
        await self.auth.login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.aclose()

    async def close_session(self):
        await self._session.aclose()
