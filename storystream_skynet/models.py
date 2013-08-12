__author__ = 'Rich @ StoryStream'
from dateutil.parser import parse as date_parser


class ModelBase:
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            name = k
            value = v
            if type(v) is str and v.endswith('_date'):
                if k == 'pub_date':
                    name = 'publish_date'
                try:
                    value = date_parser(value)
                except:
                    pass
            setattr(self, name, value)

        self.__dict__.update(kwargs)


class ContentItem(ModelBase):
    pass


class ContentBlock(ModelBase):
    def __init__(self, **kwargs):
        ModelBase.__init__(self, **kwargs)
        existing_items = self.content_items
        new_items = []
        for item in existing_items:
            new_items.append(ContentItem(**item))
        self.content_items = new_items