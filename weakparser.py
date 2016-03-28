import template
import htmlparser
import templateparser

class WeakParser():
    def __init__(self, template_string, functions=None):
        template_parser = templateparser.TemplateParser()
        template_parser.feed(template_string)
        raw_template = template_parser.get_result()

        self.template = template.Template(raw_template, functions)

    def parse(self, html):
        html_parser = htmlparser.HtmlParser()
        html_parser.feed(html)
        html_tree = html_parser.get_result()

        results = self.template.compare(html_tree)
        return results
