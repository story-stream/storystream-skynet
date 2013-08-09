import storystream_skynet.constants as c

__all__ = ['StoryStreamClient']


class StoryStreamClient(object):
    def __init__(self, story_name, endpoint=None, version=None, timeout=None):
        self.story_name = story_name
        self.endpoint = endpoint or c.ENDPOINT
        self.version = version or c.VERSION
        self.timeout = timeout or c.TIMEOUT
