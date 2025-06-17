# tests.py

import unittest
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def getfilesall(self):
        test = get_files_info("calculator", ".")


if __name__ == "__main__":
    unittest.main()
