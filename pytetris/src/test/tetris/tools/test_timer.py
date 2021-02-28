import threading
import time
import unittest

from tetris.tools.timer import Timer

global_count = 0

class TestTimer(unittest.TestCase):

    def inc(self):
        global global_count
        global_count += 1


    def test_init(self):
        self.timer = Timer(1, self.inc, ())
        time.sleep(1)
        self.assertGreater(global_count,8)

