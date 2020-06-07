# Create your tests here.
import unittest

from precise_bbcode.bbcode import get_parser

"""
    BBCode tests
"""


class TestBBCodes(unittest.TestCase):
    tests = {
        "email": {
            "source_text": "blabla[email]{EMAIL}[/email]blabla",
            "target_text": "blabla<a href=\"mailto:{EMAIL}\">Lien courriel : {EMAIL}</a>blabla",
        },
        "invisible": {
            "source_text": "blabla[invisible]blabla[/invisible]blabla",
            "target_text": "blabla<span style:\"display:none\">blabla</span>blabla",
        },
        "justifier": {
            "source_text": "blabla[justifier]blabla[/justifier]blabla",
            "target_text": "blabla<p style=\"text-align:justify\">blabla</p>blabla",
        },
        "preformatted": {
            "source_text": "blabla[preformatted]blabla[/preformatted]blabla",
            "target_text": "blabla<pre>blabla</pre>blabla",
        },
        "right": {
            "source_text": "blabla[right]blabla[/right]blabla",
            "target_text": "blabla<div align=\"right\">blabla</div>blabla",
        },
    }

    parser = get_parser()

    def test_email(self):
        """ test BBCode email """
        bbcode_name = "email"
        re = self.tests.get(bbcode_name)
        self.assertEqual(
            first=self.parser.render(re.get("source_text")),
            second=re.get("source_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_invisible(self):
        """ test BBCode invisible """
        bbcode_name = "invisible"
        re = self.tests.get(bbcode_name)
        self.assertEqual(
            first=self.parser.render(re.get("source_text")),
            second=re.get("source_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_right(self):
        """ test BBCode right """
        bbcode_name = "right"
        re = self.tests.get(bbcode_name)
        self.assertEqual(
            first=self.parser.render(re.get("source_text")),
            second=re.get("source_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_justifier(self):
        """ test BBCode justifier """
        bbcode_name = "justifier"
        re = self.tests.get(bbcode_name)
        self.assertEqual(
            first=self.parser.render(re.get("source_text")),
            second=re.get("source_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_preformatted(self):
        """ test BBCode preformatted """
        bbcode_name = "preformatted"
        re = self.tests.get(bbcode_name)
        self.assertEqual(
            first=self.parser.render(re.get("source_text")),
            second=re.get("source_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )


if __name__ == '__main__':
    unittest.main()
