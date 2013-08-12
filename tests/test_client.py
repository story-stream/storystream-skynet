import unittest
from storystream_skynet.client import StoryStreamClient
from storystream_skynet import constants
from storystream_skynet import StoryNotFoundException, SkyNetException


class SkyNetClientTestCase(unittest.TestCase):
    access_token = 'a39318c01b705e24a6b61d9fa7e5671ec0e09c20'

    default_params = {
        'endpoint': '127.0.0.1:8000',
        'version': 2,
        'timeout': 10
    }

    def test_client_default_values(self):
        client = StoryStreamClient('tester')
        self.assertEqual(client.endpoint, constants.ENDPOINT)
        self.assertEqual(client.version, constants.VERSION)
        self.assertEqual(client.timeout, constants.TIMEOUT)

    def test_client_override_values(self):
        endpoint = self.default_params['endpoint']
        version = 1
        timeout = 10

        client = StoryStreamClient('tester', endpoint=endpoint, version=version, timeout=timeout)
        self.assertEqual(client.endpoint, endpoint)
        self.assertEqual(client.version, version)
        self.assertEqual(client.timeout, timeout)

    def test_throws_exception_when_invalid_story_name_used(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('tester', **params)
        self.assertRaises(StoryNotFoundException, client.get_blocks)

    def test_get_blocks_throws_keyerror_when_passing_in_invalid_params(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('tester', **params)
        self.assertRaises(KeyError, client.get_blocks, idont_exist=True)

    def test_get_blocks_from(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream', **params)
        results = client.get_blocks(rpp=8)

        self.assertIsNotNone(results)
        self.assertTrue(len(results['blocks']) == 8, msg='%s blocks returned' % len(results['blocks']))

    def test_get_items_since(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('storystream', **params)

        since_id = client.get_blocks(rpp=8)['blocks'][4].content_block_id

        results = client.get_blocks(since_id=since_id)
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 4, msg='%s blocks returned' % len(results['blocks']))

    def test_search_for_published_items_throws_exception_when_passing_0_length_q_param(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('fos-2013', **params)
        self.assertRaises(SkyNetException, client.search_published, q='')

    def test_search_for_published_items(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('fos-2013', **params)
        results = client.search_published(q='fos', rpp=5)
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 5)

    def test_search_for_published_items_with_category(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('fos-2013', **params)
        results = client.search_published(q='fos', rpp=5, category='gas')
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 5)

    def test_search_for_approved_items_with_category(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('fos-2013', **params)
        results = client.search_approved(q='fos', rpp=5, categories='gas')
        self.assertIsNotNone(results)
        self.assertEqual(len(results['items']), 1)

    def test_search_for_approved_items(self):
        params = self.default_params
        params['access_token'] = self.access_token

        client = StoryStreamClient('fos-2013', **params)
        results = client.search_approved(q='fos', rpp=5)
        self.assertIsNotNone(results)
        self.assertEqual(len(results['items']), 4)