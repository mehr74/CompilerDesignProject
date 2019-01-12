import unittest

from scanner.scanner import Scanner


class TestSimpleCodeScanner(unittest.TestCase):

    def test_1(self):
        scanner = Scanner("resources/tests/test_defined.txt")
        while True:
            token = scanner.get_token()
            if token is None:
                break
            print(token)


if __name__ == '__main__':
    unittest.main()
