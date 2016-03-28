import unittest

import weakparser
from weakparser import exceptions

class TestScript(unittest.TestCase):
    def setUp(self):
        template_string = """
            <!DOCTYPE html>
            <body>
              <tag1>a</tag1>
              <tag2>b</tag2>
            </body>
            </html>
            """

        self.parser = weakparser.WeakParser(template_string)


    def test_first(self):
        content = """
            <!DOCTYPE html>
            <body>
              <script>random script</script>
              <tag1>a</tag1>
              <tag2>b</tag2>
            </body>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {})


    def test_middle(self):
        content = """
            <!DOCTYPE html>
            <body>
              <tag1>a</tag1>
              <script>random script</script>
              <tag2>b</tag2>
            </body>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {})


    def test_end(self):
        content = """
            <!DOCTYPE html>
            <body>
              <tag1>a</tag1>
              <tag2>b</tag2>
              <script>random script</script>
            </body>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {})
