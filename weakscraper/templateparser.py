import html.parser
import collections

from weakscraper import exceptions

class TemplateParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)

        self.genealogy = []
        self.genealogy.append([])

    def assert_complete(self):
        assert(len(self.genealogy) == 1)
        assert(len(self.genealogy[0]) == 1)
        root_node = self.genealogy[0][0]
        assert(root_node['nodetype'] == 'tag')
        assert(root_node['name'] == 'html')

    def get_result(self):
        self.assert_complete()
        root_node = self.genealogy[0][0]
        return root_node

    def feed(self, data):
        super().feed(data)

    def reset(self):
        super().reset()

    def handle_starttag(self, tag, attrs):
        attrs_dict = {}
        params = {}
        possible_params = ['wp-name', 'wp-leaf', 'wp-function', 'wp-list',
            'wp-optional', 'wp-until', 'wp-ignore', 'wp-recursive',
            'wp-ignore-attrs', 'wp-ignore-content', 'wp-name-attrs',
            'wp-function-attrs', 'wp-recursive-leaf']
        for k, v in attrs:
            if k in possible_params:
                if k == 'wp-ignore':
                    params['wp-ignore-content'] = None
                    params['wp-ignore-attrs'] = None
                elif k == 'wp-recursive-leaf':
                    params['wp-leaf'] = None
                    params['wp-recursive-leaf'] = None
                else:
                    params[k] = v
            elif k in attrs_dict:
                raise ValueError('Attribute defined multiple times in tag.')
            else:
                attrs_dict[k] = v

        brothers = self.genealogy[-1]

        children = []
        node = {'nodetype': 'tag', 'name': tag, 'attrs': attrs_dict,
            'params': params, 'children': children}
        brothers.append(node)

        if 'wp-leaf' not in node['params']:
            self.genealogy.append(node['children'])

    def handle_endtag(self, tag):
        parent = self.genealogy[-2][-1]

        if (parent['nodetype'] != 'tag'):
            raise exceptions.NodeTypeDiscrepancy(self.genealogy,
                parent['nodetype'])
        if (parent['name'] != tag):
            raise exceptions.EndTagDiscrepancy(self.genealogy,
                parent['name'])

        self.genealogy.pop()

    def handle_startendtag(self, tag, attrs):
        attrs.append(('wp-leaf', None))
        self.handle_starttag(tag, attrs)

    def handle_data(self, text):
        text = text.strip(' \t\n\r')
        if text:
            brothers = self.genealogy[-1]
            myself = {'nodetype': 'text', 'content': text}
            brothers.append(myself)

    def handle_entityref(self, name):
        raise AssertionError('This portion of code should never be reached.')

    def handle_charref(self, name):
        raise AssertionError('This portion of code should never be reached.')

    def handle_comment(self, text):
        raise AssertionError('This portion of code should never be reached.')
        #print('comment:' + text)

    def handle_decl(self, decl):
        self.handle_starttag('html', {})

    def handle_pi(self, decl):
        raise AssertionError('PI.')

    def unknown_decl(self, data):
        raise ValueError('Unknown declaration.')
