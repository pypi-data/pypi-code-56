from typing import Optional, Callable

from gql_ext.dataloaders import BaseDataLoader
from .base import BaseResolver


class BaseQueryResolver(BaseResolver):
    batch: bool = False
    _dataloader: Optional[Callable]

    async def load(self, parent, args, ctx, info):
        endpoint = self.get_endpoint(ctx['request'])
        dataloader = self.get_dataloader(ctx['request'], endpoint)
        return await dataloader(**args)

    def get_dataloader(self, request, endpoint) -> BaseDataLoader:
        dataloader = getattr(request, self.endpoint, None)
        if dataloader is None:
            dataloader = BaseDataLoader(endpoint=endpoint, request=request, batch=self.batch)
            setattr(request, self.endpoint, dataloader)
        return dataloader
