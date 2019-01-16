class ProgramBlock:
    _program_block = []

    def __init__(self, address):
        self.cur_program_counter = 0
        self.address = address

    def add_line(self, op, address_1, address_2="", address_3=""):
        self._program_block.append("(" + op + ", " + address_1 + ", " + address_2 + ", " + address_3 + ")")
        self.cur_program_counter = self.cur_program_counter + 1

    def write_to_file(self):
        output_file = open(self.address, "w")
        for line in self._program_block:
            output_file.write(line + "\n")
        output_file.close()





class Symbol:
    def __init__(self, name, scope, address):
        self.name = name
        self.scope = scope
        self.address = address


class SymbolTable:
    _next_local_address = 1000
    _next_temp_address = 2000
    _next_scope_id = 0
    _next_temp_id = 0

    _cur_scope = 0

    _scope_stack = []
    _table = {}

    def __init__(self):
        pass

    def _new_scope(self):
        self._cur_scope = CodeGenerator.our_scope_count
        CodeGenerator.our_scope_count = CodeGenerator.our_scope_count + 1
        return self._cur_scope

    def new_temp_symbol(self):
        address = self._next_temp_address
        self._next_temp_address = self._next_temp_address + 4
        return address

    def _new_local_symbol(self, name):
        symbol = Symbol(name, self._cur_scope, self._next_local_address)
        self._next_local_address = self._next_local_address + 4
        key = str(self._cur_scope) + name
        self._table[key] = symbol
        return symbol

    def find_symbol(self, name):
        key = str(self._cur_scope) + name
        if key in self._table:
            return str(self._table[key].address)
        else:
            return str(self._new_local_symbol(name).address)

    def add_symbol(self, name):
        self.find_symbol(name)
    def print_symbols(self):
        print("Symbol".rjust(32) + "\t "+ "Scope".rjust(10) + " \t " + "Address".rjust(10))
        for key, symbol in self._table.items():
            print(str(symbol.name).rjust(32) + " \t " + str(symbol.scope).rjust(10) + " \t " + str(symbol.address).rjust(10))


class CodeGenerator:
    semantic_stack = []

    def __init__(self, address):
        self.symbol_table = SymbolTable()
        self.program_block = ProgramBlock(address)

    def generate_code(self, sign, token):
        if sign == "#id":
            self.symbol_table.add_symbol(token)
        elif sign == "#pid":
            address = self.symbol_table.find_symbol(token)
            self.semantic_stack.append(address)
        elif sign == "#add":
            address = self.symbol_table.new_temp_symbol()
        elif sign == "#assign":
            for ss in self.semantic_stack:
                print(ss)
            print("\n")
            self.program_block.add_line("ASSIGN", self.semantic_stack.pop(), self.semantic_stack.pop())
        elif sign == "#mult":
            pass
        elif sign == "#add":
            temp = self.symbol_table.new_temp_symbol()
            self.program_block.add_line("ADD", self.semantic_stack.pop(), self.semantic_stack.pop(), temp)
            self.semantic_stack.append(temp)
            pass
        elif sign == "#push_imm":
            self.semantic_stack.append("#" + str(token))

    def write_output(self):
        self.program_block.write_to_file()
        self.symbol_table.print_symbols()
