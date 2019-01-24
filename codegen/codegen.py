class ProgramBlock:
    _program_block = []

    def __init__(self, address):
        self.cur_program_counter = 0
        self._address = address

    def add_line(self, op, address_1, address_2="", address_3="", pc=None):
        code = "(" + op + ", " + str(address_1) + ", " + str(address_2) + ", " + str(address_3) + ")"
        if pc is None:
            self._program_block.append(code)
            self.cur_program_counter = self.cur_program_counter + 1
        else:
            self._program_block[pc] = code

    def write_to_file(self):
        with open(self._address, "w") as output_file:
            for idx, line in enumerate(self._program_block):
                output_file.write(str(idx) + "\t")
                output_file.write(line + "\n")

    def increment_program_counter(self):
        self._program_block.append("")
        address = self.cur_program_counter
        self.cur_program_counter = self.cur_program_counter + 1
        return address


class Symbol:
    def __init__(self, type, func_var, name, scope, address, program_block_addr):
        self.type = type
        self.func_var = func_var
        self.name = name
        self.scope = scope
        self.address = address
        self.program_block_addr = program_block_addr


class SymbolTable:
    def __init__(self):
        self._next_local_address = 200
        self._next_temp_address = 600
        self.stack_start_address = 2000
        self._table = {}  # key = (name, scope)

    def new_temp_symbol_address(self):
        address = self._next_temp_address
        self._next_temp_address = self._next_temp_address + 4
        return str(address)

    def _new_local_symbol(self, type, name, scope, program_block_addr):
        symbol = Symbol(type, False, name, scope, self._next_local_address, program_block_addr)
        self._table[(name, scope)] = symbol
        self._next_local_address = self._next_local_address + 4
        return symbol

    def _search_by_symbol(self, name, scope):
        for s in range(scope, -1, -1):
            key = (name, s)
            if key in self._table:
                return self._table[(name, s)]
        return None

    def find_symbol_by_address(self, address):
        for key, symbol in self._table.items():
            if str(symbol.address) == str(address):
                return symbol
        return None

    def find_symbol(self, name, scope, func_var):
        symbol = self._search_by_symbol(name, scope)
        if symbol is None:
            print("ERROR: Symbol " + name + " not defined!")
            return None
        elif symbol.func_var != func_var:
            print("ERROR: Symbol {} is a {}".format(name, "function" if symbol.func_var else "variable"))
        else:
            return symbol

    def add_symbol(self, type, name, scope, program_block_addr):
        symbol = self._search_by_symbol(name, scope)
        if symbol is not None and symbol.scope == scope:
            print("ERROR: Symbol " + name + " has been already defined in this scope!")
            return None
        else:
            return str(self._new_local_symbol(type, name, scope, program_block_addr).address)

    def print_symbols(self):
        print("Symbol".rjust(32) + "\t " +
              "Scope".rjust(10) + " \t " +
              "Memory Address".rjust(16) + " \t " +
              "Type".rjust(10) + " \t " +
              "Program Block Address".rjust(10))
        for key, symbol in self._table.items():
            print(
                str(symbol.name).rjust(32) + " \t " +
                str(symbol.scope).rjust(10) + " \t " +
                str(symbol.address).rjust(16) + " \t " +
                str(symbol.type).rjust(10) + " \t " +
                str(symbol.program_block_addr).rjust(10))

    def change_symbol_func_var(self, name, scope, target_func_var):
        symbol = self._search_by_symbol(name, scope)
        if symbol is None or symbol.scope != scope:
            print("ERROR: Symbol " + name + " has not been defined in this scope!")
        else:
            symbol.func_var = target_func_var
            self._table[(name, scope)] = symbol


class CodeGenerator:

    def __init__(self, address):
        self._semantic_stack = []
        self._symbol_table = SymbolTable()
        self._program_block = ProgramBlock(address)
        self._scope = 0
        self.sp = self._symbol_table.new_temp_symbol_address()

        self._program_block.add_line("ASSIGN", "#" + str(self._symbol_table.stack_start_address), self.sp)
        self._semantic_stack.append(self._program_block.increment_program_counter())  # for jumping to main
        self._generate_output_method()

    def _generate_output_method(self):
        self._symbol_table.add_symbol(type="void",
                                      name="output",
                                      scope=0,
                                      program_block_addr=self._program_block.cur_program_counter)
        tmp = self._symbol_table.new_temp_symbol_address()
        self._program_block.add_line("ASSIGN",
                                     "@{}".format(self.sp),
                                     tmp)

        tmp2 = self._symbol_table.new_temp_symbol_address()
        self._program_block.add_line("SUB",
                                     self.sp,
                                     '#4',
                                     tmp2)
        self._program_block.add_line("ASSIGN",
                                     tmp2,
                                     self.sp
                                     )

        self._program_block.add_line("PRINT", tmp)
        tmp = self._symbol_table.new_temp_symbol_address()
        self._program_block.add_line("ASSIGN",
                                     "@{}".format(self.sp),
                                     tmp)

        self._program_block.add_line("SUB",
                                     self.sp,
                                     '#4', tmp2)
        self._program_block.add_line("ASSIGN",
                                     tmp2,
                                     self.sp
                                     )

        self._program_block.add_line("JP",
                                     "@" + str(tmp))

    def generate_code(self, func, token):
        if func == "":
            return
        print("Semantic Stack : ")
        for entry in self._semantic_stack:
            print(entry)
        print("Token : " + str(token))
        print("Func : " + func)
        print("Scope : " + str(self._scope))
        print("\n")
        name = token[1]
        scope = self._scope

        functions = {
            "#id": self.id,                                   # add to symbol table only
            "#set_to_func": self.set_to_func,
            "#set_to_var": self.set_to_var,
            "#push_int":  self.push_int,                      # add to symbol table only
            "#push_void":     self.push_void,                 # add to symbol table only
            "#pid": self.pid,
            "#p_get_addr": self.p_get_addr,
            "#jp_main": self.jp_main,
            "#inc_scope": self.inc_scope,
            "#dec_scope": self.dec_scope,
            "#assign": self.assign,
            "#mult": self.mult,
            "#add": self.add,
            "#push_imm": self.push_immidiate,
            "#save": self.save,
            "#jpf_save": self.jpf_save,
            "#jp": self.jp,
            "#while": self.while_func,
            "#label": self.label,
            "#cmp_save": self.cmp_save,
            "#jpf": self.jpf,
            "#push_plus": self.push_plus,
            "#push_minus": self.push_minus,
            "#push_arg": self.push_arg,
            "#call": self.call,
            "#jp_break_pop": self.jp_break_pop,
            "#push_switch": self.push_switch,
            "#break_save": self.break_save,
        }
        if func in functions:
            functions[func](name, scope)

    def break_save(self, name, scope):
        case_address = self._semantic_stack.pop()
        case_condition = self._semantic_stack.pop()
        switch_condition = self._semantic_stack.pop()
        break_address = self._program_block.increment_program_counter()
        self._semantic_stack.append(break_address)
        self._semantic_stack.append(switch_condition)
        self._semantic_stack.append(case_condition)
        self._semantic_stack.append(case_address)

    def push_switch(self, name, scope):
        self._semantic_stack.append("switch")

    def jp_break_pop(self, name, scope):
        self._semantic_stack.pop()
        entry = self._semantic_stack.pop()
        while entry != "switch":
            self._program_block.add_line("JP", self._program_block.cur_program_counter, pc=entry)
            entry = self._semantic_stack.pop()

    def call(self, name, scope):
        args= [self._semantic_stack.pop()]
        while "ARG" not in args:
            args.append(self._semantic_stack.pop())
        args.pop() # remove arg from arguments

        func = self._semantic_stack.pop()
        symbol = self._symbol_table.find_symbol_by_address(func)

        if symbol.type == "int":
            temp = self._symbol_table.new_temp_symbol_address()
            self._program_block.add_line("ADD", self.sp, "#4", temp)
            self._program_block.add_line("ASSIGN", temp, str(self.sp))

        temp = self._symbol_table.new_temp_symbol_address()
        self._program_block.add_line("ADD", str(self.sp), "#4", temp)
        self._program_block.add_line("ASSIGN", temp, str(self.sp))
        # jump line = current program counter + next assignment statement + push args statement + jump to func
        jump_line = self._program_block.cur_program_counter + 1 + len(args) * 3 + 1
        self._program_block.add_line("ASSIGN", "#" + str(jump_line), "@" + str(self.sp))

        for arg in args:
            temp = self._symbol_table.new_temp_symbol_address()
            self._program_block.add_line("ADD", str(self.sp), "#4", temp)
            self._program_block.add_line("ASSIGN", temp, str(self.sp))
            self._program_block.add_line("ASSIGN", arg, "@" + str(self.sp))

        self._program_block.add_line("JP", symbol.program_block_addr)
        if symbol.type == "int":
            temp = self._symbol_table.new_temp_symbol_address()
            self._program_block.add_line("ASSIGN", "@" + str(self.sp), temp)
            self._semantic_stack.append(temp)



    def push_arg(self, name, scope):
        self._semantic_stack.append("ARG")

    def push_minus(self, name, scope):
        self._semantic_stack.append("SUB")

    def push_plus(self, name, scope):
        self._semantic_stack.append("ADD")

    def jpf(self, name, scope):
        pc = self._semantic_stack.pop()
        condition = self._semantic_stack.pop()
        self._program_block.add_line("JPF", condition, str(self._program_block.cur_program_counter), pc=pc)

    def cmp_save(self, name, scope):
        num = name
        switch = self._semantic_stack.pop()
        temp_1 = self._symbol_table.new_temp_symbol_address()
        self._program_block.add_line("SUB", switch, "#" + str(num), temp_1)
        temp_2 = self._symbol_table.new_temp_symbol_address()
        self._program_block.add_line("NOT", temp_1, temp_2)
        self._semantic_stack.append(switch)
        self._semantic_stack.append(temp_2)
        address = self._program_block.increment_program_counter()
        self._semantic_stack.append(address)

    def label(self, name, scope):
        self._semantic_stack.append(self._program_block.cur_program_counter)

    def while_func(self, name, scope):
        pc = self._semantic_stack.pop()
        condition = self._semantic_stack.pop()
        label = self._semantic_stack.pop()
        self._program_block.add_line("JPF", condition, str(self._program_block.cur_program_counter + 1), pc=pc)
        self._program_block.add_line("JP", label)

    def jp(self, name, scope):
        pc = self._semantic_stack.pop()
        self._program_block.add_line("JP",
                                     str(self._program_block.cur_program_counter),
                                     pc=pc)

    def jpf_save(self, name, scope):
        pc = self._semantic_stack.pop()
        condition = self._semantic_stack.pop()
        self._program_block.add_line("JPF",
                                     condition,
                                     str(self._program_block.cur_program_counter + 1),
                                     pc=pc)
        self._semantic_stack.append(self._program_block.increment_program_counter())

    def save(self, name, scope):
        self._semantic_stack.append(self._program_block.increment_program_counter())

    def push_immidiate(self, name, scope):
        self._semantic_stack.append("#{}".format(name))

    def add(self, name, scope):
        temp = self._symbol_table.new_temp_symbol_address()
        operand_2 = self._semantic_stack.pop()
        operation = self._semantic_stack.pop()
        operand_1 = self._semantic_stack.pop()
        self._program_block.add_line(operation,
                                     operand_1,
                                     operand_2,
                                     temp)
        self._semantic_stack.append(temp)

    def mult(self, name, scope):
        temp = self._symbol_table.new_temp_symbol_address()
        self._program_block.add_line("MULT",
                                     self._semantic_stack.pop(),
                                     self._semantic_stack.pop(),
                                     temp)
        self._semantic_stack.append(temp)

    def assign(self, name, scope):
        self._program_block.add_line("ASSIGN",
                                     self._semantic_stack.pop(),
                                     self._semantic_stack.pop())

    def dec_scope(self, name, scope):
        self._scope = self._scope - 1

    def inc_scope(self, name, scope):
        self._scope = self._scope + 1

    def jp_main(self, name, scope):
        symbol = self._symbol_table.find_symbol("main", 0, True)
        if symbol is None:
            print("ERROR: main function not defined")
        initial_line = self._semantic_stack.pop()
        self._program_block.add_line("JP", symbol.program_block_addr, pc=initial_line)
        if len(self._semantic_stack) != 0:
            print("Undefined Error!!!!!")

    def p_get_addr(self, name, scope):
        if name == "output":
            self._semantic_stack.append("output")
        else:
            self._semantic_stack.append(self._symbol_table
                                        .find_symbol(name, scope, func_var=False)
                                        .program_block_addr)

    def pid(self, name, scope):
        self._semantic_stack.append(self._symbol_table
                                    .find_symbol(name, scope, func_var=False)
                                    .address)

    def push_void(self, name, scope):
        self._semantic_stack.append("void")

    def push_int(self, name, scope):
        self._semantic_stack.append("int")

    def set_to_var(self, name, scope):
        self._semantic_stack.pop()

    def set_to_func(self, name, scope):
        symbol = self._semantic_stack.pop()
        print("HERE: {}".format(symbol))
        self._symbol_table.change_symbol_func_var(symbol[0], int(symbol[1]), target_func_var=True)

    def id(self, name, scope): # todo: fixme
        self._symbol_table.add_symbol(type=self._semantic_stack.pop(),
                                      name=name,
                                      scope=scope,
                                      program_block_addr=self._program_block.cur_program_counter)
        self._semantic_stack.append((name, scope))

    def write_output(self):
        for entry in self._semantic_stack:
            print("{}\n".format(entry))
        self._program_block.write_to_file()
        self._symbol_table.print_symbols()
