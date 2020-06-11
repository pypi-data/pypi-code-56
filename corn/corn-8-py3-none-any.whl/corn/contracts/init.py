import inspect


def sig(hub):
    pass


def call(hub, ctx):
    """
    Top level contract for corn collection
    """
    # TODO this needs to apply recursivly to all grain functions

    argspec = inspect.getfullargspec(ctx.func)
    kwargs = argspec.kwonlyargs
    if kwargs:
        raise ValueError(
            f"Corn collection functions do not take arguments: {', '.join(kwargs)}"
        )
    args = argspec.args[1:]
    if args:
        raise ValueError(
            f"Corn collection functions do not take arguments: {', '.join(args)}"
        )

    return ctx.func(*ctx.args, **ctx.kwargs)


# These come from corn/init.py and the top level call shouldn't affect them
def release(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def release_all(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_wait_for(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_cli(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_standalone(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_collect(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_run_sub(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_process_subs(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_clean_value(hub, ctx) -> str or None:
    return ctx.func(*ctx.args, **ctx.kwargs)
