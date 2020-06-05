try:
    import importlib.metadata as ilmd  # Python 3.8
except ImportError:
    import importlib_metadata as ilmd  # Python < 3.8

from .logger import logger


def inject(requests_sessions):
    logger.debug("requests_adapter_injector::inject")

    entry_points = ilmd.entry_points()

    adapter_factories = {}
    for ep in entry_points["requests_adapter_injector.adapter"]:
        logger.debug("requests_adapter_injector::inject loading %s = %s", ep.name, ep.value)
        adapter_factories[ep.name] = ep.load()

    orig_session_init = requests_sessions.Session.__init__

    def session_init(self):
        orig_session_init(self)

        for prefix, factory in adapter_factories.items():
            logger.debug("requests_adapter_injector::inject mounting %s = %s", prefix, factory)
            self.mount(prefix, factory())

    requests_sessions.Session.__init__ = session_init
