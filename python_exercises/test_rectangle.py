"""
Run with:  python -m unittest python_exercises.test_rectangle -v
"""

import unittest

from .rectangle import Rectangle


class RectangleTests(unittest.TestCase):

    def test_initialization(self):
        rect = Rectangle(length=10, width=5)
        self.assertEqual(rect.length, 10)
        self.assertEqual(rect.width, 5)

    def test_is_iterable(self):
        rect = Rectangle(length=10, width=5)
        self.assertTrue(hasattr(rect, '__iter__'))
        # Should not raise
        iter(rect)

    def test_iteration_order_and_format(self):
        rect = Rectangle(length=10, width=5)
        results = list(rect)
        self.assertEqual(results, [{'length': 10}, {'width': 5}])


if __name__ == '__main__':
    unittest.main()
