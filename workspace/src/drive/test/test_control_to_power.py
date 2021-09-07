import unittest
import drive

class TestControlToPower(unittest.TestCase):
    def test_zero(self):
        left, right = drive.control_to_power(linear=0, angular=0)
        self.assertEqual(left, 0)
        self.assertEqual(right, 0)

    # 100 angular results in full power turns and linear is ignored
    def test_full_angular(self):
        # right turn
        left, right = drive.control_to_power(linear=100, angular=100)
        self.assertEqual(left, 100)
        self.assertEqual(right, 100)

        # left turn
        left, right = drive.control_to_power(linear=100, angular=-100)
        self.assertEqual(left, -100)
        self.assertEqual(right, -100)

    def test_full_linear(self):
        # forward
        left, right = drive.control_to_power(linear=100, angular=0)
        self.assertEqual(left, 100)
        self.assertEqual(right, -100)

        # reverse
        left, right = drive.control_to_power(linear=-100, angular=0)
        self.assertEqual(left, -100)
        self.assertEqual(right, 100)

    def test_partial_angular(self):
        # right turn, some forward
        left, right = drive.control_to_power(linear=10, angular=25)
        self.assertEqual(left, 35)
        self.assertEqual(right, 15)

        # left turn, some forward
        left, right = drive.control_to_power(linear=10, angular=-25)
        self.assertEqual(left, -15)
        self.assertEqual(right, -35)

        # right turn, some reverse
        left, right = drive.control_to_power(linear=-10, angular=25)
        self.assertEqual(left, 15)
        self.assertEqual(right, 35)

        # left turn, some reverse
        left, right = drive.control_to_power(linear=-10, angular=-25)
        self.assertEqual(left, -35)
        self.assertEqual(right, -15)