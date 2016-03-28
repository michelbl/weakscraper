
class ResultTree():
    def __init__(self, functions):
        self.genealogy = []
        self.genealogy.append({'content': {}, 'index': None})
        self.functions = functions

    def assert_root(self):
        assert(len(self.genealogy) == 1)

    def get_data(self):
        return self.genealogy[0]['content']

    def add_child(self, nodetype, name):
        myself = self.genealogy[-1]['content']

        if nodetype == 'dict':
            child = {}
        elif nodetype == 'list':
            child = []
        else:
            raise ValueError('Unknown type.')

        if type(myself).__name__ == 'dict':
            if name in myself:
                raise ValueError("Key already used.")
            myself[name] = child
            self.genealogy[-1]['index'] = name
        elif type(myself).__name__ == 'list':
            if nodetype == 'dict':
                myself.append(child)
            elif nodetype == 'list':
                # if nodetype == 'list', then the list already exists, it's myself !
                return

        self.genealogy.append({'content': child, 'index': None})

    def add_leaf(self, name, content, function=None):
        myself = self.genealogy[-1]['content']

        if function:
            f = self.functions[function]
            child = f(content)
        else:
            child = content

        if type(myself).__name__ == 'dict':
            if name in myself:
                raise ValueError("Key already used.")
            myself[name] = child
        elif type(myself).__name__ == 'list':
            myself.append(child)

    def up(self, skip_a_level, function=None):
        myself = self.genealogy[-1]['content']
        parent = self.genealogy[-2]['content']
        index = self.genealogy[-2]['index']

        if skip_a_level:
            def skip_level(e):
                children = list(e.values())
                if len(children) != 1:
                    import ipdb
                    ipdb.set_trace()
                assert(len(children) == 1)
                return children[0]
            if type(myself).__name__ == 'dict':
                parent[index] = skip_level(myself)
            if type(myself).__name__ == 'list':
                parent[index] = [skip_level(e) for e in myself]

        if function:
            f = self.functions[function]
            parent[index] = f(parent[index])
        self.genealogy.pop()
        self.genealogy[-1]['index'] = None
