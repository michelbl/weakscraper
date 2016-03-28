import unittest

import weakparser
from weakparser import exceptions

class TestWPFunction(unittest.TestCase):
    def setUp(self):
        template_string = """
            <!DOCTYPE html>
            <head wp-function="sum">
              <number wp-name="a" wp-function="int"/>
              <number wp-name="b" wp-function="int"/>
            </head>
            </html>
            """

        functions = {
            'int': int,
            'sum': (lambda dic: dic['a'] + dic['b'])
        }

        self.parser = weakparser.WeakParser(template_string, functions)


    def test_sum(self):
        content = """
            <!DOCTYPE html>
            <head>
              <number>
                12
              </number>
              <number>
                -5
              </number>
            </head>
            </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {'sum': 7})
