import unittest
from client import AzureClient

class MyTestCase(unittest.TestCase):
    def test_something(self):

        self._client = AzureClient()


if __name__ == '__main__':
    unittest.main()
