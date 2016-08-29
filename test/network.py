import unittest

from logload import logload

class TestNetworkClient(unittest.TestCase):
    def test_get_client_sock_fail(self):
        with self.assertRaises(logload.ConnectFailedError):
            logload.get_client_sock("localhost", 3)
