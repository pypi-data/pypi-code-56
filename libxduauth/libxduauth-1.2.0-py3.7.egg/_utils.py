import os

from bs4 import BeautifulSoup
from pytesseract import pytesseract


def parse_form_hidden_inputs(html):
    soup = BeautifulSoup(html, "lxml")
    return {
        item.get('name'): item.get('value', '')
        for item in soup.findAll('input', type='hidden')
    }


def try_get_vcode(img):
    try:
        from importlib import resources
        with resources.path(__package__, 'ar.traineddata') as pkg_path:
            img = img.convert('L')
            vcode = pytesseract.image_to_string(
                img, lang='ar',
                config="--psm 7 --tessdata-dir " +
                       os.path.dirname(pkg_path)
            )
    except:
        vcode = pytesseract.image_to_string(
            img, lang='eng', config="--psm 7")
    return vcode
