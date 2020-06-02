"""
leocli - a console translation script for https://dict.leo.org/ .

Copyright (c) 2012 Christian Schick

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import subprocess
import sys
from typing import Iterable, List, Tuple, Optional

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from . import __version__

try:
    import argcomplete
except ImportError:
    pass

API = "https://dict.leo.org/dictQuery/m-vocab/{lang1}{lang2}/query.xml"
DEFAULTPARAMS = {
    "tolerMode": "nof",
    "rmWords": "off",
    "rmSearch": "on",
    "searchLoc": "0",
    "resultOrder": "basic",
    "multiwordShowSingle": "on",
    "lang": "de",
}
LANGUAGES = {
    "de": "German",
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "ch": "",
    "ru": "Russian",
    "pt": "",
    "pl": "",
}
PAGER = "less"


def parse_args() -> argparse.Namespace:
    """
    Parse cli arguments.

    Return the parsed arguments
    """
    valid_langs = [lang for lang in LANGUAGES.keys() if lang != "de"]
    valid_langs_str = ", ".join(valid_langs)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "words",
        action="store",
        nargs="+",
        metavar="word",
        type=str,
        help="the words you want to translate",
    )
    parser.add_argument(
        "-l",
        "--lang",
        action="store",
        dest="language",
        metavar="lang",
        type=str,
        default="en",
        choices=valid_langs,
        help=f"the languagecode to translate to or from {valid_langs_str}",
    )
    parser.add_argument(
        "--pager",
        action="store",
        dest="pager",
        metavar="pagercmd",
        type=str,
        default=PAGER,
        help=f"The pager command to use. Default: {PAGER}. Use `--pager=` to disable the pager.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}",
    )

    if "argcomplete" in globals():
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    return args


def get(search: Iterable[str], language1: str = "en", language2: str = "de",) -> str:
    """Querie the API and returns a lists of result string pairs."""
    params = {"search": "+".join(search), "lp": f"{language1}{language2}"}
    params.update(DEFAULTPARAMS)
    try:
        res = requests.get(API.format(lang1=language1, lang2=language2), params=params,)
        res.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err:
        print("[!]", str(err), file=sys.stderr)
        sys.exit(1)

    return res.text


def parse_api(
    api_res: str, language1: str = "en", language2: str = "de",
) -> List[List[Tuple[str, str]]]:
    """Parse the API response and return the results list."""
    content = BeautifulSoup(api_res, "xml")
    results = []

    for section in content.sectionlist.findAll("section"):
        if int(section["sctCount"]) > 0:
            result = []

            for entry in section.findAll("entry"):
                res0 = entry.find("side", attrs={"lang": language1})
                res1 = entry.find("side", attrs={"lang": language2})

                if res0 and res1:
                    res0_str: str = res0.repr.getText()
                    res1_str: str = res1.repr.getText()
                    result.append((res0_str, res1_str))

            if result:
                results.append(result)

    return results


def print_result(
    results: List[List[Tuple[str, str]]],
    language1: str = "en",
    language2: str = "de",
    pager: Optional[str] = PAGER,
) -> None:
    """Print the result to stdout."""
    output = "\n\n".join(
        tabulate(
            result,
            headers=(LANGUAGES[language1], LANGUAGES[language2]),
            tablefmt="presto",
        )
        for result in results
    )

    if not pager:
        print(output)
    else:
        subprocess.run(
            pager.split(), input=output, check=True, encoding=sys.stdout.encoding,
        )


def main() -> None:
    """The main function."""
    args = parse_args()
    # The second language must be 'de'
    language2 = "de"
    api_res = get(args.words, args.language, language2)
    words = parse_api(api_res, args.language, language2)

    if words:
        print_result(words, args.language, language2, pager=args.pager)
    else:
        print(
            "[!] No matches found for '{}'".format("', '".join(args.words)),
            file=sys.stderr,
        )
        sys.exit(1)
