import sys
from collections import defaultdict


class State:
    ourCnt = 0

    def __init__(self, name):
        self.id = name + str(State.ourCnt)
        State.ourCnt = State.ourCnt + 1


class Edge:
    ourCnt = 0

    def __init__(self, begin, end, con, nt, dir):
        self.begin = begin
        self.end = end
        self.con = con
        self.nt = nt
        self.dir = dir


class GrammarParser:
    epsilon = 'EPSILON'

    def __init__(self, grammar_addr, scanner):
        with open(grammar_addr) as grammar_file:
            grammar = grammar_file.read()
        self.scanner = scanner

        self.cur_token = ''

        self.states = set()
        self.edges = set()
        self.nt_states = {}
        self.states_edges = {}
        self.nts = []

        grammar = grammar.replace("→", "->")
        grammar = grammar.replace("ε", self.epsilon)
        grammar = grammar.replace("epsilon", self.epsilon)

        self.nt = set()
        self.productions = defaultdict(list)

        self.non_entry_nt = set()

        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.predict = defaultdict(set)

        self.symbols = set()
        self.eps = defaultdict(lambda: False)
        self.nt_order = []

        for production in filter(lambda x: "->" in x, grammar.split("\n")):
            nt, rhs = production.split("->")
            nt = nt.strip()
            if nt not in self.nt_order:
                self.nt_order.append(nt)

            self.nt.add(nt)
            self.symbols.add(nt)
            for s_prod in rhs.split("|"):
                cur_prod = []
                for symbol in s_prod.split():
                    symbol = symbol.strip()
                    self.non_entry_nt.add(symbol)
                    cur_prod.append(symbol)

                    if symbol == self.epsilon:
                        self.eps[nt] = True
                        self.symbols.add(symbol)
                        self.first[nt].add(self.epsilon)
                    else:
                        self.symbols.add(symbol)
                self.productions[nt].append(cur_prod)

        self.terminals = self.symbols - self.nt

        self.start_symbols = self.nt - self.non_entry_nt

        for terminal in self.terminals:
            self.first[terminal].add(terminal)

        # Calculate the first set
        changed = True
        while changed:
            changed = False
            for nt in self.nt:
                for prod in self.productions[nt]:
                    found = False
                    for symbol in prod:
                        if len(self.first[symbol] - self.first[nt]) > 0:
                            changed = True
                            self.first[nt] |= (
                                    self.first[symbol] - set(self.epsilon))
                        if self.epsilon not in self.first[symbol]:
                            break
                    else:
                        if self.epsilon not in self.first[nt]:
                            self.first[nt].add(self.epsilon)
                            changed = True

        # Calculate the follow set
        # The start_symbols represent the non terminals that don't appear in
        # rhs
        if not self.start_symbols:
            self.start_symbols.add(self.nt_order[0])

        for nt in self.start_symbols:
            # EOL can follow those symbols
            self.follow[nt].add("$")

        changed = True
        while changed:
            changed = False

            for nt in self.nt:
                for prod in self.productions[nt]:

                    for symbol1, symbol2 in zip(prod, prod[1:]):
                        # The first symbol must be non-terminal
                        if symbol1 in self.nt:
                            first_sym2 = self.first[
                                             symbol2] - set([self.epsilon])
                            if len(first_sym2 - self.follow[symbol1]) > 0:
                                changed = True
                                self.follow[symbol1] |= first_sym2

                    last_item = prod[-1]
                    if last_item in self.nt and len(self.follow[nt] - self.follow[last_item]) > 0:
                        changed = True
                        self.follow[last_item] |= self.follow[nt]

                    if len(prod) > 1:
                        last = prod[-1]
                        if self.epsilon in self.first[last]:
                            second_last = prod[-2]
                            if len(self.follow[nt] - self.follow[second_last]) > 0:
                                changed = True
                                self.follow[second_last] |= self.follow[nt]

        for production in filter(lambda x: "->" in x, grammar.split("\n")):
            nt, rhs = production.split("->")
            nt = nt.rstrip()
            s_begin = State('S')
            s_end = State('E')
            self.nt_states[nt] = s_begin
            self.nts.append(nt)
            s_mid = s_begin

            for s_prod in rhs.split("|"):
                symbols = s_prod.split()
                symbols_count = len(symbols)
                for idx, symbol in enumerate(symbols):
                    if idx == 0:
                        if idx == symbols_count - 1:
                            self.edges.add(Edge(s_begin, s_end, symbol, 0, nt))
                        else:
                            s_mid = State("m")
                            self.edges.add(Edge(s_begin, s_mid, symbol, 0, nt))
                    else:
                        if idx == symbols_count - 1:
                            self.edges.add(Edge(s_mid, s_end, symbol, 0, nt))
                        else:
                            tmp = s_mid
                            s_mid = State("m")
                            self.edges.add(Edge(tmp, s_mid, symbol, 0, nt))
        for edge in self.edges:
            if edge.con in self.nts:
                edge.nt = 1
            self.states_edges[edge.begin.id] = [edge] if edge.begin.id not in self.states_edges \
                else self.states_edges[edge.begin.id] + [edge]

    def _next_token(self):
        self.cur_token = self.scanner.get_token()[0]
        # self.cur_token.lstrip()
        # self.cur_token.rstrip()
        return self.cur_token

    def get_parsed(self):
        self._next_token()
        return self._parse('S0')

    def _parse(self, cur_state):
        cur_token = self.cur_token
        if cur_state[0] == 'E':
            pass
        else:
            for edge in self.states_edges[cur_state]:
                # print("[ " + edge.begin.id + ", " + edge.end.id + ", '"
                #      + edge.con + "', '" + str(edge.nt) + "', '" + edge.dir + "']")
                if edge.con == cur_token:
                    # print(cur_state + " --> " + edge.end.id + " # Token matched!")
                    yield cur_token
                    self._next_token()
                    for parsed in self._parse(edge.end.id):
                        yield parsed
                    break
                elif edge.nt == 1 and (cur_token in self.first[edge.con] or self.epsilon in self.first[edge.con]):
                    # print(cur_state + " --> " + self.nt_states[edge.con].id + " # non-terminal match (first)")
                    for parsed in self._parse(self.nt_states[edge.con].id):
                        yield parsed
                    yield edge.con
                    for parsed in self._parse(edge.end.id):
                        yield parsed
                    break
                elif edge.con == self.epsilon and cur_token in self.follow[edge.dir]:
                    # print(cur_state + " --> " + edge.end.id + " # epsilon (follow)")
                    for parsed in self._parse(edge.end.id):
                        yield parsed
                    break