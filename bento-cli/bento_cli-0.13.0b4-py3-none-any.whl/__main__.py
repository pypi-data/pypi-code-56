#!/usr/bin/env python3
from bento.cli import make_cli
from bento.decorators import echo_exception


@echo_exception
def main() -> None:
    make_cli("bento")(auto_envvar_prefix="BENTO")


@echo_exception
def headless() -> None:
    make_cli("bentoh", headless=True)(
        default_map={"headless": True}, auto_envvar_prefix="BENTO"
    )


if __name__ == "__main__":
    main()
