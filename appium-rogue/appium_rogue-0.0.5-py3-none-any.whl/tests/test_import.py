import unittest


class BaseTestCase(unittest.TestCase):

    ...


class TestImport(BaseTestCase):

    def test_import(self):
        import appium_rogue
