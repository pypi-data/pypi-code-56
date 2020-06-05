import csv
import json
import os
import time
import urllib


class BaseEngine:
    """
    Базовый класс обработки результатов поиска
    """
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


class DuckDuckGoEngine(BaseEngine):
    """
    Класс для DuckDuckGo
    """
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

    def search(self, soup):
        a_classes = soup.find_all("a", attrs={"class": "result__a"}, href=True)
        for a_class in a_classes:
            if self.tries == self.count:
                break
            self.results.append((a_class.text, a_class["href"]))
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
                self.vqd_value,
            )
        else:
            return f"{self.url_query}{self.page_text}{self.page_number}"


class GoogleEngine(BaseEngine):
    """
    Класс для Google
    """
    def __init__(self, query: str, count: int):
        self.original_query = query
        self.count = count
        self.base_url = "https://www.google.com/search?q="
        self.page_text = "&start="
        self.page_number = 0

    def next_page(self):
        self.page_number += 10

    def search(self, soup):
        for g_class in soup.find_all(class_="g"):
            if self.tries == self.count:
                break
            for a_class in g_class.find_all("a"):
                if a_class.get("href") and a_class.find("h3"):
                    self.results.append(
                        (a_class.find("h3").text, a_class.get("href"))
                    )
                    self.tries += 1
                    break


def write_console(search):
    """
    Вывод результатов на экран
    """
    for item in search.results:
        print(f"{item[0]}: {item[1]}")


def write_csv(search):
    """
    Запись результатов в csv файл
    """
    pwd = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(pwd, f"{search.original_query.replace(' ', '_')}.csv")
    with open(path, "w") as outfile:
        outfile_writer = csv.writer(outfile, delimiter=";", quotechar='"')
        outfile_writer.writerow(["Text", "URL"])
        for row in search.results:
            outfile_writer.writerow(row)
    print(f"File path: {path}")


def write_json(search):
    """
    Запись результатов в json файл
    """
    pwd = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(pwd, f"{search.original_query.replace(' ', '_')}.json")
    with open(path, "w") as outfile:
        results = [{"text": x[0], "url": x[1]} for x in search.results]
        json.dump(results, outfile, indent=2, ensure_ascii=False)
    print(f"File path: {path}")
