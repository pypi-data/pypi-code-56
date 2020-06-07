# Create your tests here.
import unittest
from .bbcode import bbcode2html
from precise_bbcode.bbcode import get_parser

"""
    BBCode tests
"""


class TestBBCodes(unittest.TestCase):
    tests = {
        "email": {
            "source_text": "blabla[email]toto@domain.name[/email]blabla",
            "target_text": "blabla<a href=\"mailto:toto@domain.name\">toto@domain.name</a>blabla",
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
        "mp3": {
            "source_text": "blabla[mp3]http://test.com/mp.mp3[/mp3]blabla",
            "target_text": 'blabla<audio controls src="http://test.com/mp.mp3">Your browser does not support the '
                           '<code>audio</code> element.</audio>blabla'
        },
        "br": {
            "source_text": "blabla[br]blabla",
            "target_text": 'blabla<br />blabla'
        },
        "hr": {
            "source_text": "blabla[hr]blabla",
            "target_text": 'blabla<hr />blabla'
        },
    }

    def test_email(self):
        """ test BBCode email """
        bbcode_name = "email"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_invisible(self):
        """ test BBCode invisible """
        bbcode_name = "invisible"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_right(self):
        """ test BBCode right """
        bbcode_name = "right"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_justifier(self):
        """ test BBCode justifier """
        bbcode_name = "justifier"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_preformatted(self):
        """ test BBCode preformatted """
        bbcode_name = "preformatted"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_mp3(self):
        """ test BBCode mp3 """
        bbcode_name = "mp3"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_br(self):
        """ test BBCode br """
        bbcode_name = "br"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )

    def test_hr(self):
        """ test BBCode hr """
        bbcode_name = "hr"
        re = self.tests.get(bbcode_name)
        result = bbcode2html(re.get("source_text"))
        self.assertEqual(
            first=result,
            second=re.get("target_text"),
            msg=f"Error on rendering tag '{bbcode_name}'"
        )


if __name__ == '__main__':
    unittest.main()
