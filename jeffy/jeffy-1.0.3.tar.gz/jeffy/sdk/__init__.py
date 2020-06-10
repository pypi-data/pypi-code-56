from jeffy import framework


class SdkBase():
    """Jeffy SDK base class."""

    def __init__(self) -> None:
        self.app = framework.get_app()
