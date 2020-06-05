import argparse
import requests

from bs4 import BeautifulSoup

from search_this.utils import (
    DuckDuckGoEngine, GoogleEngine, write_console, write_csv, write_json
)


def positive_integer(i):
    """
    Проверка введено ли положительное число для количества запросов
    """
    try:
        v = int(i)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected integeter, got {i}")
    if v <= 0:
        raise argparse.ArgumentTypeError(
            f"expected positive integeter, got {i}"
        )
    return v


def process_args():
    """
    Функция обработки аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help="Query for searching. Words define in qoutes.",
    )
    parser.add_argument(
        "-e",
        "--engine",
        choices=("google", "duck"),
        default="google",
        help="Choose the search engine. Default: Google.",
    )
    parser.add_argument(
        "-c",
        "--count",
        default=1,
        type=positive_integer,
        help="Count of results. Default: 1.",
    )
    parser.add_argument(
        "-l",
        "--logging",
        choices=("console", "json", "csv"),
        default="console",
        help="Information ouput. Default: console.",
    )
    return parser.parse_args()


def start():
    """
    Главная функция
    """
    args = process_args()
    search_vars = {
        "google": GoogleEngine,
        "duck": DuckDuckGoEngine
    }
    output_function = {
        "console": write_console,
        "json": write_json,
        "csv": write_csv
    }
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0)"
        "Gecko/20100101 Firefox/65.0"
    )
    headers = {"user-agent": user_agent}
    search = search_vars[args.engine](args.query, args.count)
    while search.tries < args.count:
        response = requests.get(search.url, headers=headers)
        if response.status_code != 200:
            print(f"Error {response.status_code}")
            break
        soup = BeautifulSoup(response.text, "html.parser")
        search.search(soup)
        search.next_page()
    output_function[args.logging](search)


if __name__ == "__main__":
    start()
