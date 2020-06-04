import argparse
import csv
import json
import os
import requests
import time
import urllib

from bs4 import BeautifulSoup


class BaseEngine:

    tries = 0
    results = list()

    def __init__(self, query: str, count: int):
        self.original_query = query
        self.count = count
        self.base_url = ""
        self.page_text = ""
        self.page_number = 0

    @property
    def query(self):
        return urllib.parse.quote_plus(self.original_query)

    @property
    def url_query(self):
        return f"{self.base_url}{self.query}"

    @property
    def url(self):
        return f"{self.url_query}{self.page_text}{self.page_number}"


class GoogleEngine(BaseEngine):

    def __init__(self, query: str, count: int):
        self.original_query = query
        self.count = count
        self.base_url = "https://www.google.com/search?q="
        self.page_text = "&start="
        self.page_number = 0

    def next_page(self):
        self.page_number += 10

    def search(self, soup: BeautifulSoup):
        for g_class in soup.find_all(class_="g"):
            if self.tries == self.count:
                break
            for a_class in g_class.find_all("a"):
                if a_class.get("href") and a_class.find("h3"):
                    self.results.append(
                        (a_class.find('h3').text, a_class.get('href'))
                    )
                    self.tries += 1
                    break


class DuckDuckGoEngine(BaseEngine):

    def __init__(self, query: str, count: int):
        self.original_query = query
        self.count = count
        self.base_url = "https://duckduckgo.com/html/?q="
        self.page_text = "&s="
        self.page_number = 30
        self.extra = "&nextParams=&v=l&o=json&api=d.js"
        self.dc = "&dc="
        self.vqd = "&vqd="
        self.dc_value = ""
        self.vqd_value = ""

    def next_page(self):
        self.page_number += 50

    def search(self, soup: BeautifulSoup):
        for a_class in soup.find_all("a", attrs={'class':'result__a'}, href=True):
            if self.tries == self.count:
                break
            self.results.append(
                (a_class.text, a_class['href'])
            )
            self.tries += 1
        for input in soup.findAll("input", type="hidden"):
            if input["name"] == "dc":
                self.dc_value = input["value"]
            elif input["name"] == "vqd":
                self.vqd_value = input["value"]
        time.sleep(2)

    @property
    def url(self):
        if self.dc_value or self.vqd_value:
            return "{}{}{}{}{}{}{}{}".format(
                self.url_query,
                self.page_text,
                self.page_number,
                self.extra,
                self.dc,
                self.dc_value,
                self.vqd,
                self.vqd_value
            )
        else:
            return f"{self.url_query}{self.page_text}{self.page_number}"


def write_json(search):
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0], f"{search.original_query}.json")
    with open(path, 'w') as outfile:
        results = [{'text': x[0], 'url': x[1]} for x in search.results]
        json.dump(results, outfile, indent=2)
    print(f"File path: {path}")


def write_csv(search):
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0], f"{search.original_query}.csv")
    with open(path, 'w') as outfile:
        outfile_writer = csv.writer(outfile, delimiter=',', quotechar='"')
        outfile_writer.writerow(['Text', 'URL'])
        for row in search.results:
            outfile_writer.writerow(row)
    print(f"File path: {path}")


def write_console(search):
    for item in search.results:
        print(f"{item[0]}: {item[1]}")


def positive_integer(i: str) -> int:
    try:
        v = int(i)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected integeter, got {i}")
    if v <= 0:
        raise argparse.ArgumentTypeError(
            f"expected positive integeter, got {i}"
        )
    return v


def process_args() -> argparse.Namespace:
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
        "-r",
        "--recursive",
        action="store_true",
        help="Add this to make recursive searching.",
    )
    parser.add_argument(
        "-l",
        "--logging",
        choices=("console", "json", "csv"),
        default="console",
        help="Print information on the screen",
    )
    return parser.parse_args()


def start():
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
