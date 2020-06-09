from logging import getLogger
from typing import Callable, Optional

from aiohttp.abc import Request

logger = getLogger(__name__)


class BaseResolver:
    endpoint: str
    _endpoint: Optional[Callable] = None

    def get_endpoint(self, request: Request) -> Optional[Callable]:
        if self._endpoint is not None:
            return self._endpoint
        if not self.endpoint:
            return
        try:
            client, service, endpoint = self.endpoint.split('.')
            if not (client and service and endpoint):
                raise ValueError
        except ValueError as e:
            raise RuntimeError(f'error with parse endpoint name {self.endpoint}. '
                               f'use client.service.endpoint format. {e}')

        client = getattr(request.app, client, None)
        service = client.get(service)
        endpoint = getattr(service, endpoint, None)

        if not endpoint:
            raise RuntimeError(f'Cant get source method or endpoint for {self.endpoint}')

        self._endpoint = endpoint
        return endpoint

    async def load(self, parent, args, ctx, info):
        raise NotImplementedError
