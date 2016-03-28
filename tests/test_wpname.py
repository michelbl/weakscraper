import unittest

import weakparser
from weakparser import exceptions

class TestWPName(unittest.TestCase):
    def setUp(self):
        template_string = """
            <!DOCTYPE html>
            <head wp-name="head">
              <title wp-name="title"/>
            </head>
            </html>
            """

        self.parser = weakparser.WeakParser(template_string)


    def test_match(self):
        content = """
            <!DOCTYPE html>
            <head>
              <title>Title</title>
            </head>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {'head': {'title': 'Title'}})
