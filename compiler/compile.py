import sys

from parser.parser import GrammarParser
from scanner.scanner import Scanner
from codegen.codegen import CodeGenerator


def compile_code(grammar_addr, xml_addr, code_addr, intermediate_code_address):
    scanner = Scanner(code_addr)
    code_generator = CodeGenerator(intermediate_code_address)
    parser = GrammarParser(grammar_addr, xml_addr, scanner, code_generator)
    return parser.get_parsed()


def main():
    if len(sys.argv) <= 4:
        print("{} <grammar> <code> <parse-xml> <intermediate-code>".format(sys.argv[0]))
    else:
        grammar_address = sys.argv[1]
        code_address = sys.argv[2]
        xml_address = sys.argv[3]
        intermediate_code_address = sys.argv[4]

        compile_code(grammar_address, xml_address, code_address, intermediate_code_address)


if __name__ == "__main__":
    main()
