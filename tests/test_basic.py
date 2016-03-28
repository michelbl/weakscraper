import unittest

import weakparser
from weakparser import exceptions

class TestBasic(unittest.TestCase):
    def setUp(self):
        template_string = """
            <!DOCTYPE html>
            <head>
              <title>Title</title>
            </head>
            <body attr1="val1" attr2="val2">
              <div>Hi !</div>
            </body>
            </html>
            """

        self.parser = weakparser.WeakParser(template_string)


    def test_match(self):
        content = """
            <!DOCTYPE html>
            <head><title>Title
              </title>
            </head>


            <body attr2="val2" attr1="val1">
            <div>

                Hi !
              </div>
            </body>
              </html>
            """

        result_data = self.parser.parse(content)

        self.assertEqual(result_data, {})


    def test_datanomatch(self):
        content =  """
            <!DOCTYPE html>
            <head>
              <title>Title</title>
            </head>
            <body attr2="val2" attr1="val1">
              <div>
                Hello !
              </div>
            </body>
            </html>
            """

        try:
            result_data = self.parser.parse(content)
        except exceptions.TextError:
            return

        self.assertTrue(False)


    def test_tagnomatch(self):
        content = """
            <!DOCTYPE html>
            <head>
              <title>Title</title>
            </head>
            <body attr2="val2" attr1="val1">
              <q>
                Hi !
              </q>
            </body>
            </html>
            """

        try:
            result_data = self.parser.parse(content)
        except exceptions.TagError:
            return

        self.assertTrue(False)


    def test_attrnomatch(self):
        content = """
            <!DOCTYPE html>
            <head>
              <title>Title</title>
            </head>
            <body attr3="val1" attr2="val2">
              <div>Hi !</div>
            </body>
            </html>
            """

        try:
            result_data = self.parser.parse(content)
        except exceptions.AttrsError:
            return

        self.assertTrue(False)
