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
        self.assertEqual(u.int_to_mac(0x04_21_3D_34_00_57), "04:21:3d:34:00:57")
        self.assertEqual(u.mac_to_int("04:21:3d:34:00:57"), 0x04_21_3D_34_00_57)
        self.assertEqual(u.mac_to_int("ff:ff:ff:ff:ff:ff"), u.MAC_MAX)
