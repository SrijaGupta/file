import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.policy import configure_address_book
from jnpr.toby.hldcl.juniper.security.srx import Srx

class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_address_book_0(self):
        self.assertRaises(Exception, configure_address_book.configure_address_book)
        self.assertRaises(Exception, configure_address_book.configure_address_book, device=self.mocked_obj)
        self.assertRaises(Exception, configure_address_book.configure_address_book, device=self.mocked_obj,
                          address_book_name='ab1', addresses=' ')
        self.assertRaises(Exception, configure_address_book.configure_address_book, device=self.mocked_obj,
                          address_book_name='ab1', address_set_name=' ')
        self.assertRaises(Exception, configure_address_book.configure_address_book, device=self.mocked_obj,
                          address_book_name='ab1')

    def test_configure_address_book_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(configure_address_book.configure_address_book(device=self.mocked_obj,
                                                                       address_book_name='global',
                                                                       addresses={'source': '10.10.10.2/32',
                                                                                  'd': '20.20.20.2/32'},
                                                                       attach_zone='trust',
                                                                       commit=False),
                         True)
        self.mocked_obj.config = MagicMock()
        self.assertEqual(configure_address_book.configure_address_book(device=self.mocked_obj,
                                                                       address_book_name='global',
                                                                       addresses={'source': '10.10.10.2/32',
                                                                                  'd': '20.20.20.2/32'},
                                                                       attach_zone='trust', logical_systems=' LSYS1',
                                                                       commit=False),
                         True)
        self.assertEqual(configure_address_book.configure_address_book(device=self.mocked_obj,
                                                                       address_book_name='global',
                                                                       address_set_name='add_set',
                                                                       address_set=['source1', 'source2', 'source3'],
                                                                       commit=False),
                         True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(configure_address_book.configure_address_book(device=self.mocked_obj,
                                                                       address_book_name='global',
                                                                       address_set_name='add_set',
                                                                       address_set=['source1', 'source2', 'source3'],
                                                                       commit=True),
                         True)

if __name__ == '__main__':
    unittest.main()
