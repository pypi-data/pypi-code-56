from .base import BaseResolver


class BaseSubscriptionResolver(BaseResolver):

    async def load(self, parent, args, ctx, info):
        endpoint = self.get_endpoint(ctx['request'])
        async for message in endpoint(**args, headers=ctx['request'].headers):
            yield message
