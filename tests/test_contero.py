import unittest
import co_utils as u


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_zero_pad(self):
        self.assertEqual(str(3).zfill(5), "00003")
        self.assertEqual(str(15331).zfill(3), "15331")

    def test_mac_int(self):
        self.assertEqual(u.int_to_mac(180462667751767), "a4:21:3d:34:e1:57")
        self.assertEqual(u.mac_to_int("a4:21:3d:34:e1:57"), 180462667751767)
        self.assertEqual(u.mac_to_int("ff:ff:ff:ff:ff:ff"), u.MAC_MAX)
