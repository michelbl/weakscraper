import re

from weakscraper import exceptions


class Template():
    def __init__(self, raw_template, functions):
        self.functions = functions

        if raw_template['nodetype'] == 'tag':

            tag = raw_template['name']
            assert(tag != 'wp-nugget')

            if tag == 'wp-ignore':
                self.nodetype = 'ignore'
                self.params = raw_template['params']
                return

            self.nodetype = 'tag'
            self.name = raw_template['name']
            self.attrs = raw_template['attrs']
            self.params = raw_template['params']

            if 'wp-function' in self.params:
                if 'wp-name' not in self.params:
                    self.params['wp-name'] = self.params['wp-function']

            if 'wp-function-attrs' in self.params:
                if 'wp-name-attrs' not in self.params:
                    self.params['wp-name-attrs'] = self.params['wp-function-attrs']

            if 'wp-name-attrs' in self.params:
                self.params['wp-ignore-attrs'] = None

            if 'wp-ignore-content' in self.params:
                del self.params['wp-leaf']
                ignore = Template({'nodetype': 'tag', 'name': 'wp-ignore', 'params': {}}, functions)
                self.children = [ignore]
                return

            if 'wp-leaf' in self.params:
                assert(len(raw_template['children']) == 0)
                return

            text_flags = []
            for child in raw_template['children']:
                if child['nodetype'] == 'text':
                    text_flags.append(True)
                else:
                    assert(child['nodetype'] == 'tag')
                    if child['name'] == 'wp-nugget':
                        text_flags.append(True)
                    else:
                        text_flags.append(False)

            self.children = []
            grandchildren = []
            for i, child in enumerate(raw_template['children']):
                if text_flags[i]:
                    grandchildren.append(child)
                else:
                    if grandchildren:
                        text_template = {'nodetype': 'texts-and-nuggets', 'children': grandchildren}
                        grandchildren = []
                        new_child = Template(text_template, functions)
                        self.children.append(new_child)
                    new_child = Template(child, functions)
                    self.children.append(new_child)
            if grandchildren:
                text_template = {'nodetype': 'texts-and-nuggets', 'children': grandchildren}
                grandchildren = []
                new_child = Template(text_template, functions)
                self.children.append(new_child)

            return

        if raw_template['nodetype'] == 'texts-and-nuggets':
            if len(raw_template['children']) == 1:
                child = raw_template['children'][0]
                if child['nodetype'] == 'text':
                    self.nodetype = 'text'
                    self.content = child['content']
                    return

                if child['nodetype'] == 'tag':
                    assert(child['name'] == 'wp-nugget')
                    self.nodetype = 'nugget'
                    self.params = child['params']
                    return

                raise ValueError('Unexpected nodetype.')

            self.nodetype = 'texts-and-nuggets'
            self.regex = ''
            self.names = []
            self.functions = []

            expected_type = raw_template['children'][0]['nodetype']
            for child in raw_template['children']:
                if child['nodetype'] != expected_type:
                    raise ValueError('Unexpected nodetype.')

                if child['nodetype'] == 'text':
                    self.regex += re.escape(child['content'])
                    expected_type = 'tag'
                elif child['nodetype'] == 'tag':
                    self.regex += '(.*)'
                    name = child['params']['wp-name']
                    self.names.append(name)
                    if 'wp-function' in child['params']:
                        function = child['params']['wp-function']
                    else:
                        function = None
                    self.functions.append(function)
                    expected_type = 'text'
                else:
                    raise ValueError('Unexpected nodetype.')
            return

        raise ValueError('Unknown nodetype %s.'%raw_template['nodetype'])

    def f(self, obj):
        if ('wp-function' in self.params) and ('wp-list' not in self.params):
            function_name = self.params['wp-function']
            function = self.functions[function_name]
            return function(obj)
        return obj

    def compare_wrapper(self, child, html):
        try:
            results = child.compare(html)
        except exceptions.CompareError as e:
            e.register_parent(self)
            raise e
        return results


    def compare(self, html):
        results = {}

        if self.nodetype == 'text':
            assert(html['nodetype'] == 'text')
            if html['content'] != self.content:
                raise exceptions.TextError(self, html)

        elif self.nodetype == 'nugget':
            content = self.f(html['content'])

            name = self.params['wp-name']
            results[name] = content

        elif self.nodetype == 'texts-and-nuggets':
            regex = '^' + self.regex + '$'
            match = re.match(regex, html['content'])
            groups = match.groups()
            assert(len(groups) == len(self.names))
            assert(len(groups) == len(self.functions))

            for i in range(len(groups)):
                name = self.names[i]
                function_name = self.functions[i]
                result = groups[i]
                if function_name:
                    function = self.functions[function_name]
                    result = function(result)
                results[name] = result

        elif self.nodetype == 'tag':
            if (html['nodetype'] != 'tag'):
                raise exceptions.NodetypeError(self, html)
            if (self.name != html['name']):
                raise exceptions.TagError(self, html)
            if not self.attrs_match(html['attrs']):
                raise exceptions.AttrsError(self, html)

            if 'wp-name-attrs' in self.params:
                name = self.params['wp-name-attrs']
                content = html['attrs']
                if 'wp-function-attrs' in self.params:
                    function_name = self.params['wp-function-attrs']
                    function = self.functions[function_name]
                    content = function(content)
                results[name] = content

            if 'wp-leaf' in self.params:
                if 'wp-recursive' in self.params:
                    name = self.params['wp-name']
                    results[name] = self.f(html['children'])
                else:
                    if not 'wp-ignore-content' in self.params:
                        if 'wp-name' in self.params:
                            name = self.params['wp-name']
                            assert(len(html['children']) == 1)
                            html_child = html['children'][0]
                            assert(html_child['nodetype'] == 'text')
                            content = html_child['content']
                            results[name] = self.f(content)
                        else:
                            assert('children' not in html)

            else:
                # look at the children
                children_results = {}

                self_position = 0
                self_n_children = len(self.children)
                html_position = 0
                html_n_children = len(html['children'])

                def skip_children(html, html_position):
                    while (
                        (html_position < html_n_children) and
                        (html['children'][html_position]['nodetype'] == 'tag') and
                        (html['children'][html_position]['name'] == 'script')
                    ):
                        html_position += 1
                    return html_position

                while (self_position < self_n_children):
                    self_child = self.children[self_position]

                    html_position = skip_children(html, html_position)

                    if self_child.nodetype == 'ignore':
                        if 'wp-until' in self_child.params:
                            until = self_child.params['wp-until']
                            while (html_position < html_n_children) and (not (
                                (html['children'][html_position]['nodetype'] == 'tag')
                                and
                                (html['children'][html_position]['name'] == until)
                            )):
                                html_position += 1

                            self_position += 1
                        else:
                            html_position = html_n_children
                            self_position += 1

                    elif self_child.nodetype == 'tag' and 'wp-list' in self_child.params:
                        result_list = []
                        while (
                            (html_position < html_n_children) and
                            (html['children'][html_position]['nodetype'] == 'tag') and
                            (html['children'][html_position]['name'] == self_child.name)
                        ):
                            result = self.compare_wrapper(self_child, html['children'][html_position])
                            result_list.append(result)
                            html_position += 1
                        name = self_child.params['wp-name']
                        if 'wp-function' in self_child.params:
                            function_name = self_child.params['wp-function']
                            function = self.functions[function_name]
                            result_list = function(result_list)
                        children_results[name] = result_list
                        self_position += 1

                    elif self_child.nodetype == 'text':
                        self.compare_wrapper(self_child, html['children'][html_position])
                        html_position += 1
                        self_position += 1

                    elif self_child.nodetype in ['nugget', 'texts-and-nuggets', 'tag']:
                        if (
                            (self_child.nodetype == 'tag') and
                            ('wp-optional' in self_child.params) and
                            (
                                (html_position >= html_n_children) or
                                (html['children'][html_position]['nodetype'] != 'tag') or
                                (html['children'][html_position]['name'] != self_child.name)
                            )
                        ):
                            self_position += 1
                        else:
                            if html_position >= html_n_children:
                                e = exceptions.MissingNodeError(self_child, html)
                                e.register_parent(self)
                                raise e
                            result = self.compare_wrapper(self_child, html['children'][html_position])
                            for k, v in result.items():
                                if k in children_results:
                                    raise ValueError('Key already defined.')
                                children_results[k] = v
                            html_position += 1
                            self_position += 1
                    else:
                        raise ValueError('Unknown child type.')

                html_position = skip_children(html, html_position)

                if html_position != html_n_children:
                    raise exceptions.ExcessNodeError(self, html)

                if 'wp-name' in self.params:
                    name = self.params['wp-name']
                    results[name] = self.f(children_results)
                else:
                    for k, v in children_results.items():
                        if k in results:
                            raise ValueError('Key already defined.')
                        results[k] = v

        else:
            raise ValueError('Unexpected nodetype.')

        return results


    def attrs_match(self, attrs):
        wp_ignore_attrs = ('wp-ignore-attrs' in self.params)

        if not wp_ignore_attrs:
            return self.attrs == attrs

        for attr, value in self.attrs.items():
            if not attr in attrs:
                return False
            if attrs[attr] != value:
                return False

        return True
