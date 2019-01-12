import unittest

from scanner.scanner import Scanner


class TestSimpleCodeScanner(unittest.TestCase):

    def test_1(self):
        scanner = Scanner("resources/tests/test_1.txt")
        correct_ans = [('keyword', 'void'), ('ID', 'main'), ('OP', '('), ('keyword', 'void'), ('OP', ')'), ('OP', '{'),
                       ('keyword', 'int'), ('ID', 'i'), ('OP', ';'), ('ID', 'i'), ('OP', '='), ('NUM', 0), ('OP', ';'),
                       ('keyword', 'if'), ('OP', '('), ('ID', 'i'), ('OP', '=='), ('NUM', 53), ('OP', ')'),
                       ('keyword', 'return'), ('NUM', -1), ('OP', ';'), ('keyword', 'else'),
                       ('keyword', 'return'), ('NUM', 0), ('OP', ';'), ('keyword', 'return'),
                       ('ID', 'i'), ('OP', ';'), ('OP', '}')]
        i = 0
        while True:
            token = scanner.get_token()
            if token is None:
                break
            print(token)
            print(correct_ans[i])
            assert correct_ans[i][0] == token[0] and correct_ans[i][1] == token[1]
            i += 1
        assert i == len(correct_ans)


if __name__ == '__main__':
    unittest.main()
