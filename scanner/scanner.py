from warnings import warn
import re


def other():
    return True


class Scanner:
    def __init__(self, code_address):
        local_fsm, self.state_funcs, self.keywords = self._define_lang()
        self.fsm = self._bake_fsm(local_fsm)
        self.last_term = (None, None)
        self.cur_term = (None, "")
        self.code = open(code_address)
        self.current_char = self._next_char()
        if self.current_char is None:
            raise Exception("Code is empty!")

    def _define_lang(self):
        return {0: [('/', 1), ('[A-Za-z]', 4), ('[0-9]', 5), ('[+-]', 6), ('=', 8), ('[;\[\](){},:<*]', 'OP')],
                1: [('*', 2), ],
                2: [('*', 3), ('^[*]', 2), ],
                3: [('*', 3), ('/', 'CMT'), ('^[*/]', 2)],
                4: [('[A-Za-z0-9]', 4), (other, 'IK')],
                5: [('[0-9]', 5), (other, 'NUM')],
                6: [(self._must_add, 'OP'), (other, 7)],
                7: [('[0-9]', 5)],
                8: [('=', 'OP'), [other, 'OP']]}, \
               {'OP': self._token_operator,
                'CMT': self._token_comment,
                'IK': self._token_id_or_keyword,
                'NUM': self._token_num,
                }, ['return', 'break', 'continue', 'int', 'void', 'if', 'while', 'switch', 'case']

    def _next_char(self):
        chunk_size = 1024
        while True:
            data = self.code.read(chunk_size)
            if not data:
                break
            for c in data:
                yield str(c)
        return None

    def _must_add(self):
        return self.last_term[0] in ['NUM', 'id'] or self.last_term[1] in [')', ']']

    def _bake_fsm(self, fsm):
        baked_fsm = {}
        for state in fsm:
            baked_fsm[state] = [(cond if type(cond) != str else self._create_matcher_function(cond), nxt_state) for
                                cond, nxt_state in fsm[state]]
        return baked_fsm

    def _create_matcher_function(self, pattern):
        p = re.compile(pattern)

        def fun():
            if p.match(self.current_char) is not None:
                self.cur_term[1] += self.current_char
                self.current_char = self._next_char()
                return True
            return False

        return fun

    def get_token(self):
        if self.current_char is None:
            warn("End of file")
            return None
        state = 0
        while True:
            for cond, nxt_state in self.fsm[state]:
                if cond():
                    state = nxt_state
                    if state in self.state_funcs:
                        ans = function(self.state_funcs[state])()
                        if ans is not None:
                            return ans
                    break

    def _token_operator(self):
        self.cur_term[0] = "OP"
        self.last_term, self.cur_term = self.cur_term, (None, "")
        return self.last_term

    def _token_comment(self):
        self.cur_term[0] = "CMT"
        self.last_term, self.cur_term = self.cur_term, (None, "")
        return self.last_term

    def _token_id_or_keyword(self):
        if self.cur_term[1] in self.keywords:
            self.cur_term[0] = "keyword"
        else:
            self.cur_term[0] = "ID"
        self.last_term, self.cur_term = self.cur_term, (None, "")
        return self.last_term

    def _token_num(self):
        self.cur_term = ("NUM", int(self.cur_term[1]))
        self.last_term, self.cur_term = self.cur_term, (None, "")
        return self.last_term