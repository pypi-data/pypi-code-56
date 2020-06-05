import importhook


@importhook.on_import("requests.sessions")
def on_import_requests_session(requests_sessions):
    from .injector import inject
    inject(requests_sessions)
