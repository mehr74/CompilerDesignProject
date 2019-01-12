import sys

from parser.parser import GrammarParser
from scanner.scanner import Scanner


def compile_code(grammar_addr, code_addr):
    scanner = Scanner(code_addr)
    parser = GrammarParser(grammar_addr, scanner)
    return parser.get_parsed()


def main():
    if len(sys.argv) <= 2:
        print("{} <grammar> <code>".format(sys.argv[0]))
    else:
        grammar_addr = open(sys.argv[1]).read()
        code_addr = open(sys.argv[2]).read()
        compile_code(grammar_addr, code_addr)


if __name__ == "__main__":
    main()
