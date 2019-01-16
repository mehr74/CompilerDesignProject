class ProgramBlock:
    _program_block = []

    def __init__(self, address):
        self.cur_program_counter = 0
        self.address = address

    def add_line(self, op, address_1, address_2="", address_3=""):
        self._program_block.append("(" + op + ", " + str(address_1) + ", " + str(address_2) + ", " + str(address_3) + ")")
        self.cur_program_counter = self.cur_program_counter + 1

    def add_line_with_pc(self, pc, op, address_1, address_2="", address_3=""):
        self._program_block[pc] = "(" + op + ", " + str(address_1) + ", " + str(address_2) + ", " + str(address_3) + ")"

    def write_to_file(self):
        output_file = open(self.address, "w")
        for idx, line in enumerate(self._program_block):
            output_file.write(str(idx) + "\t")
            output_file.write(line + "\n")
        output_file.close()

    def increment_program_counter(self):
        self._program_block.append("")
        address = self.cur_program_counter
        self.cur_program_counter = self.cur_program_counter + 1
        return address


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
        return str(address)

    def _new_local_symbol(self, name):
        symbol = Symbol(name, self._cur_scope, self._next_local_address)
        self._next_local_address = self._next_local_address + 4
        key = str(self._cur_scope) + name
        self._table[key] = symbol
        return symbol

    def _find_symbol(self, name):
        key = str(self._cur_scope) + name
        if key in self._table:
            return str(self._table[key].address)
        return ""

    def find_symbol(self, name):
        if name == "output":
            return name
        symbol = self._find_symbol(name)
        if symbol == "":
            print("ERROR: Symbol " + name + " not defined!")
            return ""
        else:
            return symbol

    def add_symbol(self, name):
        symbol = self._find_symbol(name)
        if symbol != "":
            print("ERROR: Symbol " + name + " has been defined!")
            return
        else:
            return str(self._new_local_symbol(name).address)

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
        if sign == "":
            return
        print("Semantic Stack : ")
        for entry in self.semantic_stack:
            print(entry)
        print("Token : " + str(token))
        print("Sign : " + sign)
        print("\n")

        if sign == "#id":
            self.symbol_table.add_symbol(token)

        elif sign == "#pid":
            address = self.symbol_table.find_symbol(token)
            self.semantic_stack.append(address)

        elif sign == "#assign":
            self.program_block.add_line("ASSIGN", self.semantic_stack.pop(), self.semantic_stack.pop())

        elif sign == "#mult":
            temp = self.symbol_table.new_temp_symbol()
            self.program_block.add_line("MULT", self.semantic_stack.pop(), self.semantic_stack.pop(), temp)
            self.semantic_stack.append(temp)

        elif sign == "#add":
            temp = self.symbol_table.new_temp_symbol()
            operand_2 = self.semantic_stack.pop()
            operation = self.semantic_stack.pop()
            operand_1 = self.semantic_stack.pop()
            self.program_block.add_line(operation, operand_1, operand_2, temp)
            self.semantic_stack.append(temp)

        elif sign == "#push_imm":
            self.semantic_stack.append("#" + str(token))

        elif sign == "#save":
            address = self.program_block.increment_program_counter()
            self.semantic_stack.append(address)

        elif sign == "#jpf_save":
            pc = self.semantic_stack.pop()
            condition = self.semantic_stack.pop()
            self.program_block.add_line_with_pc(pc, "JPF", condition, str(self.program_block.cur_program_counter + 1))
            self.semantic_stack.append(self.program_block.cur_program_counter)
            self.program_block.increment_program_counter()

        elif sign == "#jp":
            pc = self.semantic_stack.pop()
            self.program_block.add_line_with_pc(pc, "JP", str(self.program_block.cur_program_counter))

        elif sign == "#while":
            pc = self.semantic_stack.pop()
            condition = self.semantic_stack.pop()
            label = self.semantic_stack.pop()
            self.program_block.add_line_with_pc(pc, "JPF", condition, str(self.program_block.cur_program_counter + 1))
            self.program_block.add_line("JP", label)

        elif sign == "#label":
            self.semantic_stack.append(self.program_block.cur_program_counter)

        elif sign == "#cmp_save":
            num = token
            switch = self.semantic_stack.pop()
            temp_1 = self.symbol_table.new_temp_symbol()
            self.program_block.add_line("SUB", switch, "#" + str(num), temp_1)
            temp_2 = self.symbol_table.new_temp_symbol()
            self.program_block.add_line("NOT", temp_1, temp_2)
            self.semantic_stack.append(switch)
            self.semantic_stack.append(temp_2)
            address = self.program_block.increment_program_counter()
            self.semantic_stack.append(address)

        elif sign == "#jpf":
            pc = self.semantic_stack.pop()
            condition = self.semantic_stack.pop()
            self.program_block.add_line_with_pc(pc, "JPF", condition, str(self.program_block.cur_program_counter))

        elif sign == "#push_plus":
            self.semantic_stack.append("ADD")

        elif sign == "#push_minus":
            self.semantic_stack.append("SUB")

        elif sign == "#push_arg":
            self.semantic_stack.append("ARG")

        elif sign == "#call":
            args = [self.semantic_stack.pop()]
            while "ARG" not in args:
                args.append(self.semantic_stack.pop())
            func = self.semantic_stack.pop()
            if func == "output" and (len(args) == 2):
                self.program_block.add_line("PRINT", args[0])

        elif sign == "#jp_break_pop":
            self.semantic_stack.pop()
            entry = self.semantic_stack.pop()
            while entry != "switch":
                self.program_block.add_line_with_pc(entry, "JP", self.program_block.cur_program_counter)
                entry = self.semantic_stack.pop()

        elif sign == "#push_switch":
            self.semantic_stack.append("switch")

        elif sign == "#break_save":
            case_address = self.semantic_stack.pop()
            case_condition = self.semantic_stack.pop()
            switch_condition = self.semantic_stack.pop()
            break_address = self.program_block.increment_program_counter()
            self.semantic_stack.append(break_address)
            self.semantic_stack.append(switch_condition)
            self.semantic_stack.append(case_condition)
            self.semantic_stack.append(case_address)

    def write_output(self):
        for entry in self.semantic_stack:
            print(entry + "\n")
        self.program_block.write_to_file()
        self.symbol_table.print_symbols()
