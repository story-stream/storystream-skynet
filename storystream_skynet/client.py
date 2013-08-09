import json
import urllib
import urllib2
from urllib2 import URLError, HTTPError
from storystream_skynet import SkyNetException
import storystream_skynet.constants as c

__all__ = ['StoryStreamClient']


class StoryStreamClient(object):
    __ENDPOINT_MAPS = {
        'blocks': {
            'url': 'blocks/published/',
            'allowed_params': ['page', 'rpp', 'since_id']
        },
        'search_published': {
            'url': 'search/published/',
            'allowed_params': ['q', 'page', 'rpp', 'types', 'order_by', 'all_media', 'tags']
        },
        'search_approved': {
            'url': 'search/approved/',
            'allowed_params': ['q', 'page', 'rpp', 'categories', 'types', 'order_by', 'all_media', 'tags']
        }
    }

    def __init__(self, story_name, endpoint=None, version=None, timeout=None):
        self.story_name = story_name
        self.endpoint = endpoint or c.ENDPOINT
        self.version = version or c.VERSION
        self.timeout = timeout or c.TIMEOUT

    def get_blocks(self):
        """
        Retrieve Content Blocks for a Story
        page -- current page of items
        rpp -- number of items to return per page. This is restricted to a maximum of 100 items per page. Default page size is 20
        since_id -- get items published after block with id
        """

    def search_published(self):
        """
        Search  for published Content Blocks for a Story
        q -- term to search by - must be 3 characters or more
        Possible kwargs:
        tags -- comma separated list of tags to filter by, tags are not inclusive of each other (OR query)
        types -- comma separated list of feed types to filter by e.g. Youtube, Twitter. Types are not include of each other (OR query)
        all_media -- true/false value will return all associated images & videos or first just associated image/video. (default: false)
        rpp -- number of items to return per page. This is restricted to a maximum of 100 items per page. (default: 20)
        order_by -- property to order items by. Format should be `-FIELDNAME` to search by FIELDNAME in DESCENDING order or `FIELDNAME` for ASCENDING results. (default: -publish_date)
        """
        pass

    def search_approved(self):
        """
        Search approved Content Items for a Story
        q -- term to search by - must be 3 characters or more
        Possible kwargs
        categories -- comma separated list of categories to filter by.
        tags -- comma separated list of tags to filter by, tags are not inclusive of each other (OR query)
        types -- comma separated list of feed types to filter by e.g. Youtube, Twitter. Types are not include of each other (OR query)
        all_media -- true/false value will return all associated images & videos or first just associated image/video. (default: false)
        rpp -- number of items to return per page. This is restricted to a maximum of 100 items per page. (default: 20)
        order_by -- property to order items by. Format should be `-FIELDNAME` to search by FIELDNAME in DESCENDING order or `FIELDNAME` for ASCENDING results. (default: -id)
        """
        pass

    def __request(self, endpoint, **params):
        url = self.__build_uri(endpoint) + '?' + urllib.urlencode(params)
        req = urllib2.Request(url, headers={'Accept': 'application/json'})
        try:
            response = urllib2.urlopen(req, timeout=self.timeout)
            parsed_response = json.loads(response.read())

            if 'detail' in parsed_response:
                raise SkyNetException(parsed_response['detail'])
            else:
                return parsed_response
        except HTTPError as e:
            raise e
        except URLError as e:
            raise e

    def __build_uri(self, endpoint):
        return 'http://%s/api/v%s/%s%s/' % (self.endpoint, self.version, endpoint, self.story_name)