import unittest

from compiler.compile import compile_code


class TestCompiler(unittest.TestCase):

    def test_1(self):
        grammar_addr = "parser/grammar.txt"
        code_addr = "resources/tests/test_small.txt"

        compile_code(grammar_addr, code_addr)
        #
        # for parsed in compile_code(grammar_addr, code_addr):
        #     print(parsed, end=" ")


if __name__ == '__main__':
    unittest.main()
