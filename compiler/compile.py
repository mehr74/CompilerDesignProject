import sys

from parser.parser import GrammarParser
from scanner.scanner import Scanner


def compile_code(grammar_addr, xml_addr, code_addr):
    scanner = Scanner(code_addr)
    parser = GrammarParser(grammar_addr, xml_addr, scanner)
    return parser.get_parsed()


def main():
    if len(sys.argv) <= 3:
        print("{} <grammar> <code> <parse-xml>".format(sys.argv[0]))
    else:
        grammar_addr = sys.argv[1]
        code_addr = sys.argv[2]
        xml_addr = sys.argv[3]
        compile_code(grammar_addr, xml_addr, code_addr)


if __name__ == "__main__":
    main()
