import re
from warnings import warn


def _other():
    return True


def _get_code(code_address, chunk_size=1024):
    with open(code_address) as code_file:
        while True:
            data = code_file.read(chunk_size)
            if not data:
                break
            for c in data:
                yield str(c)
    yield None


class Scanner:
    def __init__(self, code_address):
        local_fsm, self._state_funcs, self._keywords = self._define_lang()
        self._fsm = self._bake_fsm(local_fsm)
        self._last_term = (None, None)
        self._cur_token_str = ""
        self._code = _get_code(code_address)
        self._current_char = self._code.__next__()
        if self._current_char is None:
            raise Exception("Code is empty!")

    def _define_lang(self):
        return {0: [('/', 1), ('[A-Za-z]', 4), ('[0-9]', 5), ('[+-]', 6), ('=', 8), ('[;\[\](){},:<*]', 'OP'),
                    ('\s', 9), ],
                1: [('\*', 2), ],
                2: [('\*', 3), ('[^*]', 2), ],
                3: [('\*', 3), ('/', 'CMT'), ('[^*/]', 2)],
                4: [('[A-Za-z0-9]', 4), (_other, 'IK')],
                5: [('[0-9]', 5), (_other, 'NUM')],
                6: [(self._must_add, 'OP'), (_other, 7)],
                7: [('[0-9]', 5)],
                8: [('=', 'OP'), [_other, 'OP']],
                9: [('\s', 9), [_other, 'SPC']]}, \
               {'OP': self._token_operator,
                'CMT': self._token_comment,
                'IK': self._token_id_or_keyword,
                'NUM': self._token_num,
                'SPC': self._token_whitespace,
                }, ['return', 'break', 'continue', 'int', 'void', 'if', 'while', 'switch', 'case', 'else', 'default']

    def _must_add(self):
        return self._last_term[0] in ['NUM', 'ID'] or self._last_term[1] in [')', ']']

    def _bake_fsm(self, fsm):
        baked_fsm = {}
        for state in fsm:
            baked_fsm[state] = [(cond if type(cond) != str else self._create_matcher_function(cond), nxt_state) for
                                cond, nxt_state in fsm[state]]
        return baked_fsm

    def _create_matcher_function(self, pattern):
        p = re.compile(pattern)

        def fun():
            if self._current_char is not None and p.match(self._current_char) is not None:
                self._cur_token_str += self._current_char
                self._current_char = self._code.__next__()
                return True
            return False

        return fun

    def get_token(self):
        if self._current_char is None:
            warn("End of file")
            return "EOF"
        state = 0
        while True:
            for cond, nxt_state in self._fsm[state]:
                if cond():
                    state = nxt_state
                    if state in self._state_funcs:
                        return self._state_funcs[state]()
                    break

    def _token_operator(self):
        self._last_term = (self._cur_token_str, self._cur_token_str)
        self._cur_token_str = ""
        return self._last_term

    def _token_id_or_keyword(self):
        self._last_term = (self._cur_token_str if self._cur_token_str in self._keywords else 'ID', self._cur_token_str)
        self._cur_token_str = ""
        return self._last_term

    def _token_num(self):
        self._last_term = ("NUM", int(self._cur_token_str))
        self._cur_token_str = ""
        return self._last_term

    def _token_comment(self):
        return self._token_skip()

    def _token_whitespace(self):
        return self._token_skip()

    def _token_skip(self):
        self._cur_token_str = ""
        return self.get_token()
