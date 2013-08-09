import unittest
from storystream_skynet.client import StoryStreamClient
from storystream_skynet import constants, StoryNotFoundException


class SkyNetClientTestCase(unittest.TestCase):
    def test_client_default_values(self):
        client = StoryStreamClient('tester')
        self.assertEqual(client.endpoint, constants.ENDPOINT)
        self.assertEqual(client.version, constants.VERSION)
        self.assertEqual(client.timeout, constants.TIMEOUT)

    def test_client_override_values(self):
        endpoint = 'storystreamdemo.com'
        version = 1
        timeout = 10

        client = StoryStreamClient('tester', endpoint=endpoint, version=version, timeout=timeout)
        self.assertEqual(client.endpoint, endpoint)
        self.assertEqual(client.version, version)
        self.assertEqual(client.timeout, timeout)

    def test_throws_exception_when_invalid_story_name_used(self):
        endpoint = 'storystreamdemo.com'
        version = 2

        client = StoryStreamClient('tester', endpoint=endpoint, version=version)
        self.assertRaises(StoryNotFoundException, client.get_blocks)

    def test_get_blocks_throws_keyerror_when_passing_in_invalid_params(self):
        endpoint = 'storystreamdemo.com'
        version = 2

        client = StoryStreamClient('tester', endpoint=endpoint, version=version)
        self.assertRaises(KeyError, client.get_blocks, idont_exist=True)

    def test_get_blocks_from(self):
        endpoint = 'storystreamdemo.com'
        version = 2

        client = StoryStreamClient('storystream', endpoint=endpoint, version=version)
        results = client.get_blocks(rpp=10)

        self.assertIsNotNone(results)
        self.assertTrue(len(results['blocks']) == 10)

    def test_get_items_since(self):
        endpoint = 'storystreamdemo.com'
        version = 2
        client = StoryStreamClient('storystream', endpoint=endpoint, version=version)

        since_id = client.get_blocks(rpp=10)['blocks'][4]['content_block_id']

        results = client.get_blocks(since_id=since_id)
        self.assertIsNotNone(results)
        self.assertEqual(len(results['blocks']), 4)

    def test_search_for_published_items(self):
        endpoint = 'storystreamdemo.com'
        version = 2
        client = StoryStreamClient('storystream', endpoint=endpoint, version=version)

        results = client.search_published()
        self.assertEqual(len(results['blocks']), 20)





