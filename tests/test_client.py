import unittest
from storystream_skynet.client import StoryStreamClient
from storystream_skynet import constants


class SkyNetClientTestCase(unittest.TestCase):
    def test_client_default_values(self):
        client = StoryStreamClient('tester')
        self.assertEqual(client.endpoint, constants.ENDPOINT)
        self.assertEqual(client.version, constants.VERSION)
        self.assertEqual(client.timeout, constants.TIMEOUT)

    def test_client_override_values(self):
        endpoint = 'http://storystreamdemo.com'
        version = 1
        timeout = 10

        client = StoryStreamClient('tester', endpoint=endpoint, version=version, timeout=timeout)
        self.assertEqual(client.endpoint, endpoint)
        self.assertEqual(client.version, version)
        self.assertEqual(client.timeout, timeout)