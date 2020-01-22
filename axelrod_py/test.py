import unittest
import ctypes as C
import os

libc = C.CDLL(os.getcwd() + '/libc.so')

class TestOverlap(unittest.TestCase):

    pass

if __name__ == '__main__':
    unittest.main()

