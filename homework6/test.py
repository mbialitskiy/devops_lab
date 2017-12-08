from unittest import TestCase

import task6

class TestTask6(TestCase):

  def setUp(self):
    """Init"""

  def test_check_for_existance(self):
    self.assertEqual(task6.check_for_existance('/usr/bin/', 'bash'), None)


  def tearDown(self):
    """Finish"""
