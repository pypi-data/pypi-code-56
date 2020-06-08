import sys

import requests
from parsel import Selector


IMAGE_URL_CSS_SELECTOR = "[itemprop=image]::attr(content)"


def get_bilibili_image(video_url, filepath=None):
    video_req = requests.get(video_url)
    selector = Selector(text=video_req.text)
    image_url = selector.css(IMAGE_URL_CSS_SELECTOR).get()
    image_req = requests.get(image_url)
    if filepath is None:
        filepath = image_url.split('/')[-1]
    with open(filepath, 'wb') as f:
        f.write(image_req.content)


def main():
    try:
        get_bilibili_image(*sys.argv[1:])
    except TypeError:
        print("输入错误, 请检查命令是否正确")
        print("bilibili-image video_url filepath")


if __name__ == "__main__":
    main()