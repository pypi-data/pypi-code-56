from functools import partial

from .context_factory import default_context_factory
from .subscription_ws_handler import AIOHTTPSubscriptionHandler


def set_ws_handlers(app, engine, endpoint_url: str = '/ws'):
    executor_context = {"app": app}
    context_factory = partial(default_context_factory, executor_context)

    app.router.add_route("GET", endpoint_url, AIOHTTPSubscriptionHandler(app, engine, context_factory))
