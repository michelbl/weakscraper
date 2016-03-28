import unittest

import weakparser
from weakparser import exceptions

class TestWPOptional(unittest.TestCase):
    def setUp(self):
        template_string = """
            <!DOCTYPE html>
            <body>
              <tag1 wp-optional>
                some text
              </tag1>
              <tag2 wp-name="tag2" wp-optional/>
            </body>
            </html>
            """

        self.parser = weakparser.WeakParser(template_string)


    def test_empty(self):
        content = """
            <!DOCTYPE html>
            <body>
            </body>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {})


    def test_first(self):
        content = """
            <!DOCTYPE html>
            <body>
              <tag1>
                some text
              </tag1>
            </body>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {})


    def test_second(self):
        content = """
            <!DOCTYPE html>
            <body>
              <tag2>some text
              </tag2>
            </body>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {'tag2': 'some text'})
