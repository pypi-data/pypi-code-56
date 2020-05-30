from flask import Blueprint


class NestableBlueprint(Blueprint):
    """
        Hacking in support for nesting blueprints, until hopefully
        https://github.com/mitsuhiko/flask/issues/593 will be resolved
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or "") + (options.get("url_prefix", blueprint.url_prefix) or "")
            if "url_prefix" in options:
                del options["url_prefix"]
            blueprint.name = f"{state.blueprint.name}.{blueprint.name}"
            blueprint.import_name = f"{state.blueprint.import_name}.{blueprint.import_name}"
            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)

        self.record(deferred)

    def register_method_view(self, *args, **kwargs):
        def wrapper(method_view_class):
            name = method_view_class.__name__
            self.add_url_rule(*args, view_func=method_view_class.as_view(name), **kwargs)
            return method_view_class

        return wrapper
