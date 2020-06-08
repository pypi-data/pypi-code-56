from .base import BaseResolver


class BaseMutationResolver(BaseResolver):

    async def load(self, parent, args, ctx, info):
        endpoint = self.get_endpoint(ctx['request'])
        return await endpoint(**args, headers=ctx['request'].headers)
