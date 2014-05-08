import unittest

class FailureTestCase(unittest.TestCase):
    def test_should_fail(self):
        self.assertTrue(False)
