class Content(object):

    @staticmethod
    def getOrderedList(data, list_):
        title = None
        desc = None
        items = []

        _get_content = lambda item: data.get(item, {}).get('content', None)
        _get_assembled_item = lambda item: {
            'title': item,
            'data': _get_content(item),
        }

        for item in list_:
            if item == 'title':
                title = _get_content(item)
                continue
            elif item == 'desc':
                desc = _get_content(item)
                continue

            items.append(_get_assembled_item(item))

        return title, desc, items

    def __init__(self, data):
        self.list = data.get('__list__', [])
        self.title, self.desc, self.items = self.getOrderedList(data, self.list)

    @property
    def content(self):
        return [item.get('data') for item in self.items]
