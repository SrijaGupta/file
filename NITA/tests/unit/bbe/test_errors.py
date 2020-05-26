import unittest
from jnpr.toby.bbe.errors import BBEError

class TestBBEError(unittest.TestCase):
    """
    TestIxiaTester class to handle errors.py unit tests
    """
    def test_BBEError(self):
        obj1 = BBEError(message='msg', details='test')
        self.assertEqual(obj1.message, 'msg')



if __name__ == '__main__':
    unittest.main()