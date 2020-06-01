import json
from .colors import (
    INFO,
    REST,
    FAIL,
    PASS
)


def empty_lines(n: int = 0) -> None:
    print("\n" * n)


def info(message: str, title: str = "INFO") -> None:
    print(f"{INFO} {title} {REST}  {message}")


def ok(message: str, title: str = "PASS") -> None:
    print(f"{PASS} {title} {REST}  {message}")


def fail(message: str, title: str = "FAIL") -> None:
    print(f"{FAIL} {title} {REST}  {message}")


def json_pretty_print(obj: dict or list, title: str = "JSON") -> None:
    pretty_string = json.dumps(obj, indent=4, sort_keys=True)
    pretty_string = pretty_string.split("\n")
    for line in pretty_string:
        print(f"{INFO} {title} {REST}  {line}")
