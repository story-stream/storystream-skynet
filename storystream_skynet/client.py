__author__ = 'Rich @ StoryStream'

import re
from storystream_skynet.models import ContentBlock, ContentItem
import inspect
import json
import urllib
import urllib2
from urllib2 import URLError, HTTPError
from .exceptions import SkyNetException, StoryNotFoundException
import constants as c


class StoryStreamClient(object):
    __ENDPOINT_MAPS = {
        'get_blocks': {
            'url': 'blocks/published/',
            'allowed_params': ['page', 'rpp', 'since_id'],
            'contains_blocks': True
        },
        'search_published': {
            'url': 'search/published/',
            'allowed_params': ['q', 'page', 'rpp', 'categories', 'types', 'order_by', 'all_media', 'tags', 'content_type'],
            'contains_blocks': True
        },
        'search_approved': {
            'url': 'search/approved/',
            'allowed_params': ['q', 'page', 'rpp', 'categories', 'types', 'order_by', 'all_media', 'tags', 'content_type'],
            'contains_blocks': False
        },
        'search_all': {
            'url': 'search/all/',
            'allowed_params': ['q', 'page', 'rpp', 'categories', 'types', 'order_by', 'all_media', 'tags', 'content_type'],
            'contains_blocks': False
        }
    }

    def __init__(self, story_name, access_token=None, endpoint=None, version=None, timeout=None):
        self.story_name = story_name
        self.base_url = endpoint or c.ENDPOINT
        self.version = version or c.VERSION
        self.timeout = timeout or c.TIMEOUT
        self.access_token = access_token

    def get_blocks(self, **kwargs):
        """
        Retrieve Content Blocks for a Story
        Possible kwargs:
        page -- current page of items
        rpp -- number of items to return per page. This is restricted to a maximum of 100 items per page. Default page size is 20
        since_id -- get items published after block with id
        """
        endpoint = self.__validate_params(**kwargs)

        return self.__request(endpoint, **kwargs)

    def search_published(self, q, **kwargs):
        """
        Search  for published Content Blocks for a Story
        q -- term to search by - must be 3 characters or more if specified
        Possible kwargs
        categories: comma separated list of categories to filter by tags are not inclusive of each other (OR query)
        tags -- comma separated list of tags to filter by, tags are not inclusive of each other (OR query)
        types -- comma separated list of feed types to filter by e.g. Youtube, Twitter. You can also specify "social" for all social media feeds, or "created" for all author created content. Types are not inclusive of each other (OR query)
        content_type -- comma separated list of content item type to filter by e.g "video", "image", "text". Types are inclusive of each other (OR query)
        all_media -- true/false value will return all associated images & videos or first just associated image/video. (default: false)
        rpp -- number of items to return per page. This is restricted to a maximum of 100 items per page. (default: 20)
        order_by -- property to order items by. Format should be `-FIELDNAME` to search by FIELDNAME in DESCENDING order or `FIELDNAME` for ASCENDING results. (default: -publish_date)
        """
        endpoint = self.__validate_params(q=q, **kwargs)

        return self.__request(endpoint, q=q, **kwargs)

    def search_approved(self, q, **kwargs):
        """
        Search approved Content Items for a Story
        q -- term to search by - must be 3 characters or more
        Possible kwargs
        categories: comma separated list of categories to filter by tags are not inclusive of each other (OR query)
        tags -- comma separated list of tags to filter by, tags are not inclusive of each other (OR query)
        types -- comma separated list of feed types to filter by e.g. Youtube, Twitter. You can also specify "social" for all social media feeds, or "created" for all author created content. Types are not inclusive of each other (OR query)
        content_type -- comma separated list of content item type to filter by e.g "video", "image", "text". Types are inclusive of each other (OR query)
        all_media -- true/false value will return all associated images & videos or first just associated image/video. (default: false)
        rpp -- number of items to return per page. This is restricted to a maximum of 100 items per page. (default: 20)
        order_by -- property to order items by. Format should be `-FIELDNAME` to search by FIELDNAME in DESCENDING order or `FIELDNAME` for ASCENDING results. (default: -publish_date)
        """
        endpoint = self.__validate_params(q=q, **kwargs)
        return self.__request(endpoint, q=q, **kwargs)

    def search_all(self, q, **kwargs):
        """
        Search not published Content Items for a Story
        q -- term to search by - must be 3 characters or more
        Possible kwargs
        categories: comma separated list of categories to filter by tags are not inclusive of each other (OR query)
        tags -- comma separated list of tags to filter by, tags are not inclusive of each other (OR query)
        types -- comma separated list of feed types to filter by e.g. Youtube, Twitter. You can also specify "social" for all social media feeds, or "created" for all author created content. Types are not inclusive of each other (OR query)
        content_type -- comma separated list of content item type to filter by e.g "video", "image", "text". Types are inclusive of each other (OR query)
        all_media -- true/false value will return all associated images & videos or first just associated image/video. (default: false)
        rpp -- number of items to return per page. This is restricted to a maximum of 100 items per page. (default: 20)
        order_by -- property to order items by. Format should be `-FIELDNAME` to search by FIELDNAME in DESCENDING order or `FIELDNAME` for ASCENDING results. (default: -publish_date)
        """
        endpoint = self.__validate_params(q=q, **kwargs)
        return self.__request(endpoint, q=q, **kwargs)

    def __request(self, endpoint, **params):
        if self.access_token:
            params['access_token'] = self.access_token

        url = self.__build_uri(endpoint['url']) + '?' + urllib.urlencode(params)
        headers = {'Accept': 'application/json'}

        req = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(req, timeout=self.timeout)
            return self.__parse_response(response.read(), endpoint)
        except HTTPError as e:
            try:
                parsed_error = json.loads(e.read())
                if 'detail' in parsed_error:
                    if e.code == 404:
                        e = StoryNotFoundException('%s %s' % (parsed_error['detail'], url))
                    else:
                        e = SkyNetException('%s %s' % (parsed_error['detail'], url))
            except:
                pass

            raise e
        except URLError as e:
            raise e
        except Exception as e:
            raise e

    def __parse_response(self, response, endpoint):
        parsed_response = json.loads(response)

        if 'detail' in parsed_response:
            raise SkyNetException('%s %s' % (parsed_response['detail'], endpoint['url']))
        else:
            if endpoint['contains_blocks']:
                klass = ContentBlock
                key = 'blocks'
            else:
                klass = ContentItem
                key = 'items'

            items_to_parse = []
            for item in parsed_response[key]:
                items_to_parse.append(klass(**item))

            parsed_response[key] = items_to_parse

            return parsed_response

    def __validate_params(self, **kwargs):
        called_by = inspect.stack()[1][3]
        endpoint = self.__ENDPOINT_MAPS[called_by]
        valid_params = endpoint['allowed_params']
        invalid_params = list(set(kwargs or {})-set(valid_params))
        if invalid_params:
            raise KeyError('%s are invalid parameters for this method' % ', '.join(invalid_params))

        return endpoint

    def __build_uri(self, endpoint):
        path = re.sub(r'/{2,}', '/', '/api/v%s/%s/%s/' % (self.version, self.story_name, endpoint))
        return 'http://%s%s' % (self.base_url, path)