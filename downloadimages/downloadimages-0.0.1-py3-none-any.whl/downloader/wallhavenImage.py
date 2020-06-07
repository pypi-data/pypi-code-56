from bs4 import BeautifulSoup

from ..crawler import Crawler
from .generic import ImageGetter
from .customExceptions import DownloaderInvaildParam


class WallhavenImage(ImageGetter):

    def __init__(self, search=None, limit=None, category="toplist", nsfw=True, ratios=None):
        """[Init for wallhaven.cc iterator image]

        Get image url from wallhaven.cc

        Keyword Arguments:
            search {str} -- key work search (default: {None})
            limit {[int]} -- [limit image urls get] (default: {None} -- unlimit)
            category {str} -- [wallhaven.cc category] (default: {"toplist"}) -- vaild value: toplist, random, latest
            nsfw {[bool]} -- nsfw flag (defautl: {True})
            ratios {[str]} -- ratio image (defautl: {None}) -- valid value: [None, "16x9", "16x10", "21x9", "32x9", "48x9"]
        """
        # self._validate_kwargs()
        if search == category == None:
            raise DownloaderInvaildParam("Required search or category is not None")
        if category not in ["toplist", "random", "latest"]:
            raise DownloaderInvaildParam('category vaild value: ["toplist", "random", "latest"]')

        self.search = search
        self.limit = limit
        self.category = category
        self.nsfw = bool(nsfw)
        self.ratios = ratios

    def __iter__(self):
        # self._validate_kwargs()

        self.crawler = Crawler()
        self.current_page = 0
        self.number_image = 0

        self.pre_load_urls = []
        self._generate_url = self._generator_url()

        return self

    def _validate_kwargs(self, **kwargs):
        pass

    def _generator_url(self):
        if self.search:
            url = f"https://wallhaven.cc/search?q={self.search}"
        else:
            url = f"https://wallhaven.cc/{self.category}"
        if self.ratios:
            params = f"categories=111&purity=10{self.nsfw:d}&topRange=1M&ratios={self.ratios}&sorting=toplist&order=desc"
        else:
            params = f"categories=111&purity=10{self.nsfw:d}&topRange=1M&sorting=toplist&order=desc"
        while True:
            self.current_page += 1
            yield f"{url}?{params}&page={self.current_page}"

    def _parse_image_url(self, html):
        soup = BeautifulSoup(html, "lxml")
        figure_elems = soup.select("ul > li > figure")
        for figure_elem in figure_elems:
            link_split = figure_elem.select_one("a.preview")["href"].split("/")
            is_png = figure_elem.select_one("div.thumb-info > span.png")
            if is_png:
                image_ext = "png"
            else:
                image_ext = "jpg"
            url = f"https://w.wallhaven.cc/full/{link_split[-1][:2]}/wallhaven-{link_split[-1]}.{image_ext}"
            yield url

    def get_urls(self):
        res = []
        self.current_page = 0
        self.crawler = Crawler()
        number_image_credit = self.limit
        for page_url in self._generate_url():
            html = self.crawler.get_text(page_url)
            urls = list(self._parse_image_url(html))
            res.extend(urls[:number_image_credit])
            number_image_credit -= len(urls)
            if number_image_credit > 0:
                continue
            return res
        return res

    def __next__(self):
        if len(self.pre_load_urls) == 0:
            page_url = next(self._generate_url)
            html = self.crawler.get_text(page_url)
            self.pre_load_urls = list(self._parse_image_url(html))

        image_url = self.pre_load_urls.pop(0)
        self.number_image += 1
        if self.limit and self.number_image > self.limit:
            raise StopIteration
        return image_url
