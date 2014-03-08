from datetime import datetime
import unittest
from storystream_skynet.client import StoryStreamClient
from storystream_skynet import constants
from storystream_skynet import StoryNotFoundException, SkyNetException


class SkyNetClientTestCase(unittest.TestCase):
    access_token = '8cd7c4d65c3488e85b6d0bc03722ea64f3258b92'

    default_params = {
        'endpoint': 'storystreamdemo.com',
        'version': 2,
        'timeout': 10
    }

    def test_client_default_values(self):
        client = StoryStreamClient('tester')
        self.assertEqual(client.base_url, constants.ENDPOINT)
        self.assertEqual(client.version, constants.VERSION)
        self.assertEqual(client.timeout, constants.TIMEOUT)

    def test_client_override_values(self):
        endpoint = self.default_params['endpoint']
        version = 1
        timeout = 10

        client = StoryStreamClient('tester', endpoint=endpoint, version=version, timeout=timeout)
        self.assertEqual(client.base_url, endpoint)
        self.assertEqual(client.version, version)
        self.assertEqual(client.timeout, timeout)

    def test_throws_exception_when_invalid_story_name_used(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('tester123', **params)
        self.assertRaises(StoryNotFoundException, client.get_blocks)

    def test_get_blocks_throws_keyerror_when_passing_in_invalid_params(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('tester', **params)
        self.assertRaises(KeyError, client.get_blocks, idont_exist=True)

    def test_get_blocks_from(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-test-sto', **params)
        results = client.get_blocks(rpp=3)

        self.assertIsNotNone(results)
        self.assertTrue(len(results['blocks']) == 3, msg='%s blocks returned' % len(results['blocks']))

    def test_get_items_since(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-test-sto', **params)

        initial_blocks = client.get_blocks(rpp=8)['blocks']

        since_id = initial_blocks[4].content_block_id

        results = client.get_blocks(since_id=since_id)
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 4, msg='%s blocks returned' % len(results['blocks']))

    def test_search_for_published_items(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-test-sto', **params)
        results = client.search_published(q='brighton', rpp=2)
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 2)

    def test_can_parse_datetimes(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-test-sto', **params)
        results = client.search_published(q='brighton', rpp=1)
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 1)

        self.assertEqual(type(results['blocks'][0].content_items[0].publish_date), datetime)

    def test_search_for_published_items_with_category(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-test-sto', **params)
        results = client.search_published(q='brighton', rpp=5, categories='test-category')
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 0)

    def test_search_for_approved_items_with_category(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-test-sto', **params)
        results = client.search_approved(q='brighton', rpp=5, categories='gas')
        self.assertIsNotNone(results)
        self.assertTrue(len(results['items']) <= 5)

    def test_search_for_approved_items(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-test-sto', **params)
        results = client.search_approved(q='brighton', rpp=5)
        self.assertIsNotNone(results)
        self.assertTrue(len(results['items']) <= 5)

    def test_search_for_not_published_items(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-bbq', **params)
        results = client.search_all(q='porsche', rpp=5)
        self.assertIsNotNone(results)
        self.assertTrue(len(results['items']) <= 5)

    def test_search_for_not_published_items_with_category(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream-bbq', **params)
        results = client.search_all(q='porsche', rpp=5, categories='music')
        self.assertIsNotNone(results)
        self.assertTrue(len(results['items']) <= 5)