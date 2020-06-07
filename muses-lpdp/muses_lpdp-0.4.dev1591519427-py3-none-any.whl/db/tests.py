# Create your tests here.
import unittest

from precise_bbcode.bbcode import get_parser

from db.models import Member


class TestThemesList(unittest.TestCase):
    themes = {
        "THEME_DEFAULT": "muses_default",
        "THEME_CLASSIC": "muses_classic",
        "THEME_ROSE": "muses_rose",
        "THEME_BLUE": "muses_blue",
        "THEME_GREEN": "muses_green",
        "THEME_ORANGE": "muses_orange",
    }

    def test_themes_in_choices(self):
        m = Member()
        for k in self.themes:
            self.assertEqual(self.themes[k], getattr(m, k), msg=f"Member not contains {self.themes[k]}")


"""
    BBCode tests
"""


class TestBBCodes(unittest.TestCase):

        tests = {
            "invisible":{
                "source_text": "blabla[invisible]blabla[/invisible]blabla",
                "target_text": "blabla<span style:\"display:none\">blabla</span>blabla",
            },
            "justifier":{
                "source_text": "blabla[justifier]blabla[/justifier]blabla",
                "target_text": "blabla<p style=\"text-align:justify\">blabla</p>blabla",
            },
            "preformatted": {
                "source_text": "blabla[preformatted]blabla[/preformatted]blabla",
                "target_text": "blabla<pre>blabla</pre>blabla",
            }
        }

        parser = get_parser()

        def test_invisible(self):
            """ test BBCode invisible """
            bbcode_name = "invisible"
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
