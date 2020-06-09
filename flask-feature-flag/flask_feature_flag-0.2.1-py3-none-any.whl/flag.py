import functools
from .use_cases import GetFeature
from .utils import (
    response_command,
    response_not_found,
    response_use_case
)


class Flag:

    def __init__(self, app=None, cache=None, **kwargs):
        if app is not None:
            self.init_app(app, cache, **kwargs)

    def init_app(self, app, cache=None, **kwargs):
        self._config = app.config
        self._cache = cache

    def route_enabled(self, feature: str):
        """Decorator to enable or disable a route.

        Example:
        ::
            @flag.route_enabled('MY_FEATURE'):
                def my_funtion():
                    pass

        Args:
            feature: Environment variable name.

        Returns:
            response: Decorated function or response_not_found.
        """
        def _decorator(func):
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                use_case = GetFeature(self._config, self._cache)
                feature_name = use_case.handle(feature)
                if feature_name:
                    return func(*args, **kwargs)
                return response_not_found()
            return _wrapper
        return _decorator

    def is_enabled(self, response, feature):
        """Decorator to enable or disable a feature.

        Example:
        ::
            @flag.is_enabled(lambda: {}, 'MY_FEATURE'):
                def my_funtion():
                    pass

        Args:
            response: Function that returns object to return.
            feature: Environment variable name.

        Returns:
            response: Decorated function or function error.
        """
        def _decorator(func):
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                use_case = GetFeature(self._config, self._cache)
                feature_name = use_case.handle(feature)
                if feature_name:
                    return func(*args, **kwargs)
                return response()
            return _wrapper
        return _decorator

    def command_enabled(self, feature: str):
        """Decorator to enable or disable a command.

        Example:
        ::
            @flag.command_enabled('MY_FEATURE'):
                def my_funtion():
                    pass

        Args:
            feature: Environment variable name.

        Returns:
            response: Decorated function or response_command.
        """
        def _decorator(func):
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                use_case = GetFeature(self._config, self._cache)
                feature_name = use_case.handle(feature)
                if feature_name:
                    return func(*args, **kwargs)
                return response_command()
            return _wrapper
        return _decorator

    def use_case_enabled(self, feature: str):
        """Decorator to enable or disable a use case.

        Example:
        ::
            @flag.use_case_enabled('MY_FEATURE'):
                def my_funtion():
                    pass

        Args:
            feature: Environment variable name.

        Returns:
            response: Decorated function or response_use_case.
        """
        def _decorator(func):
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                use_case = GetFeature(self._config, self._cache)
                feature_name = use_case.handle(feature)
                if feature_name:
                    return func(*args, **kwargs)
                return response_use_case()
            return _wrapper
        return _decorator

    def on(self, feature: str):
        """Enable or disable a feature.

        Example:
        ::
            if flag.on('MY_FEATURE'):
                pass

        Args:
            feature (str):

        Returns:
            bool:
        """
        use_case = GetFeature(self._config, self._cache)
        return use_case.handle(feature)
