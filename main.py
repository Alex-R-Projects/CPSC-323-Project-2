# Symbol: {name} 
# Symbols table: { {name} {type:0=terminal / 1=non-terminal} }
# Rule: {LHS} {RHS: sequence of symbol names} {index of ·} {0=not visited / 1=visited}
# state: {index} {Rules} {leaf}
# Transitions graph: {List: {index of Source State} {index of Destination State} {transition symbol}}

class State:
    _n = 0  # start index of states (made to change manually here)
    _count = 0 + _n
    graph = []

    def __init__(self):
        self.rules = []
        self._i = State._count
        self.has_reduce = 0  # The state has a rule to reduce
        State._count = State._count + 1

    def add_rule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)
            if rule._closure == -1:
                self.has_reduce = 1

    def goto(self, destination_index, symbol):
        g = [self._i, destination_index, symbol]
        if g not in State.graph:
            State.graph.append(g)

    def closure(self):  # closure operation
        for rule in self.rules:
            if rule.visited:
                continue
            for r in rule.visit():
                if r not in self.rules:
                    self.add_rule(r)

    def __eq__(self, s):
        if not isinstance(s, State):
            return NotImplemented
        eq = True
        if len(self.rules) > len(s.rules):
            return False
        for r in self.rules:
            eq = eq and (r in s.rules)
        return eq

    def __str__(self):
        s = []
        max_len = 1
        for r in self.rules:
            line = '    [' + str(r)
            s.append(line)
            if len(line) > max_len:
                max_len = len(line)
        # make all lines with the same length
        for i in range(len(s)):
            pad = max_len - len(s[i])
            s[i] = s[i] + ' ' * pad + ']'
        s.insert(0, ''.join(['I', str(self._i), ':', ' ' * (max_len - 2)]))
        return '\n'.join(s)


class Rule:
    _n = 0  # start index of augmented grammar
    augmented = []

    def __init__(self, lhs, rhs=[], dot_index=0):
        self.lhs = lhs
        if rhs == ['!εpslon']:
            self.rhs = []
        else:
            self.rhs = rhs
        self._closure = dot_index

        if self.dot_at_end():
            self._closure = -1

        self.visited = 0

    def __str__(self):
        rhs = list(self.rhs)
        dot = self._closure
        if dot == -1:
            dot = len(rhs)
        rhs.insert(dot, '•')
        return self.lhs + ' → ' + ' '.join(rhs)

    def __eq__(self, rule):
        if not isinstance(rule, Rule):
            return NotImplemented
        return self.lhs == rule.lhs and self.rhs == rule.rhs and self._closure == rule._closure

    def handle(self):
        return self.rhs[self._closure]

    def visit(self):
        self.visited = 1
        # If dot is not at the end of rule and is a handle (non-terminal)
        if self._closure != -1:
            handle = self.rhs[self._closure]
            if handle.startswith('`'):
                return [r.copy() for r in Rule.augmented if r.lhs == handle]
        return []

    def dot_at_end(self):
        return self._closure == len(self.rhs)

    def move_dot(self):
        if self._closure == -1:
            return None
        return Rule(self.lhs, self.rhs, self._closure + 1)

    def copy(self):
        return Rule(self.lhs, self.rhs)


def first_pos(symbol):
    first = set()
    if not symbol.startswith('`'):
        return {symbol}

    for r in [i for i in Rule.augmented if i.lhs == symbol]:
        whole_rhs_has_e = True
        for s in r.rhs:
            has_e = False
            for f in first_pos(s):
                if f == '!εpslon':
                    has_e = True
                else:
                    first.add(f)
            if not has_e:
                whole_rhs_has_e = False
                break
        if whole_rhs_has_e:
            first.add('!εpslon')
    return list(first)


def follow_pos(symbol, A=None):
    follow = set()
    if symbol.endswith("'"):
        follow.add('$')
    for r in [i for i in Rule.augmented if symbol in i.rhs]:
        occurrences = r.rhs.count(symbol)
        if symbol == r.rhs[-1]:
            if symbol != r.lhs and A != r.lhs:
                for f in follow_pos(r.lhs, symbol):
                    follow.add(f)
            continue
        beta = r.rhs
        for i in range(occurrences):
            j = beta.index(symbol)
            beta = r.rhs[j + 1:]
            s = beta[0]
            f = first_pos(s)
            for f1 in f:
                if f1 == '!εpslon':
                    if symbol == r.lhs or A == r.lhs:
                        continue
                    for f2 in follow_pos(r.lhs, symbol):
                        follow.add(f2)
                else:
                    follow.add(f1)
    return follow


def test_frstfllw(symbols):
    c = []
    for s in symbols:
        f = first_pos(s)
        fo = follow_pos(s)
        c.append([s, ' '.join(f), ' '.join(fo)])
    return c


from pandas import DataFrame as df, MultiIndex


states = []
parsing_table = df()


def grammar_from_str(g):
    grm = g.split('\n')
    rules = []
    for r in grm:
        if r.strip() == '':
            continue  # skip empty lines
        lhs, rhs_ls = r.split('=>')
        for rhs in rhs_ls.split('|'):
            rules.append((lhs.strip(), rhs.strip().split()))
    return rules


def augment(grammar_str):
    grammar = grammar_from_str(grammar_str)
    rhs = [grammar[0][0]]  # The start symbol
    aug = Rule(grammar[0][0] + "'", tuple(rhs))
    s = State()
    s.add_rule(aug)
    Rule.augmented.append(aug)
    for r in grammar:
        Rule.augmented.append(Rule(r[0], r[1]))
    return s, extract_symbols(grammar)


def extract_symbols(rules):
    terminals = []
    non_terminals = []
    for r in rules:
        if r[0] not in non_terminals:
            non_terminals.append(r[0])
        for s in r[1]:
            if not s.startswith('`'):
                if s not in terminals and s != '!εpslon':  # Skip adding epsilon to terminals
                    terminals.append(s)
            else:
                if s not in non_terminals:
                    non_terminals.append(s)
    terminals.append('$')
    return non_terminals, terminals


def goto_operation():
    for s in states:
        transitions = []
        for r in s.rules:
            rule = r.move_dot()
            dot_at_end = rule is None
            if dot_at_end:
                continue
            transitions.append((r.handle(), rule))

        gotoself(transitions, s)

        for t in transitions:
            items_same_X = [r for r in transitions if r[0] == t[0]]
            make_transition(s, items_same_X)
    return State.graph


def gotoself(transitions, s):
    for t in transitions:
        if t[1] in s.rules:
            s.goto(s._i, t[0])
            transitions.remove(t)


def create_new_state(items_same_X):
    new_state = State()
    for r in items_same_X:
        new_state.add_rule(r[1])
    return new_state

...

def make_transition(source, items_same_X):
    new_st = create_new_state(items_same_X)
    exists = False
    for s in states:
        if new_st == s:
            source.goto(s._i, symbol=items_same_X[0][0])
            exists = True
            State._count = State._count - 1
            break
    if not exists:
        new_st.closure()
        states.append(new_st)
        source.goto(new_st._i, symbol=items_same_X[0][0])



def parsing_table_skeleton(non_terminals, terminals):
    levels = (['action'] * len(terminals) + ['goto'] * len(non_terminals))
    columns = terminals + non_terminals
    index = [s._i for s in states]
    return df(index=index, columns=MultiIndex.from_tuples(list(zip(levels, columns)), names=['table', 'symbol'])).fillna('_')


def slr_parsing_table(items):
    global parsing_table
    for i in items:
        is_terminal = not i[2].startswith('`')
        if is_terminal:  # Shift
            cell = parsing_table.loc[(i[0]), ('action', i[2])]
            if cell != '_':
                print('conflict: ' + cell + '    s' + str(i[1]))
                continue
            parsing_table.loc[(i[0]), ('action', i[2])] = 's' + str(i[1])
        else:  # goto
            parsing_table.loc[(i[0]), ('goto', i[2])] = i[1]
    n = Rule._n  # grammar rules start index
    reduce = [(s.rules[0].lhs, s._i, Rule.augmented.index(s.rules[0].copy())) for s in states if s.has_reduce]
    for r in reduce:
        if r[0].endswith("'"):
            parsing_table.loc[(r[1]), ('action', '$')] = 'accept'
        else:
            for f in follow_pos(r[0]):
                cell = parsing_table.loc[(r[1]), ('action', f)]
                if cell != '_':
                    print('conflict: ' + cell + '    r' + str(r[2] + n))
                parsing_table.loc[(r[1]), ('action', f)] = 'r' + str(r[2] + n)


def moves(s):
    snap = []
    stack = [('$', State._n)]
    input_ = s.split() + ['$']
    action = []
    while True:
        a = parsing_table.loc[(stack[-1][1]), ('action', input_[0])]
        action.append(a)
        snap.append((''.join([s[0] + str(s[1]) for s in stack]), ' '.join(input_)))
        if a == 'accept':
            print('Driver: accept')
            break
        if a.startswith('s'):  # Shift
            stack.append((input_[0], int(''.join(a[1:]))))
            input_.remove(input_[0])
        elif a.startswith('r'):  # Reduce
            r = Rule.augmented[(int(''.join(a[1:])))]
            for _ in range(len(r.rhs)):
                stack.pop()
            goto = parsing_table.loc[(stack[-1][1]), ('goto', r.lhs)]
            stack.append((r.lhs, goto))
            action[-1] = ' '.join([a, 'goto:' + str(goto), str(r).replace(' • ', ' ')])
        else:
            print('Driver: Syntax error')
            break
    return df(data=list(zip([s[0] for s in snap], [s[1] for s in snap], action)), columns=('Stack', 'Input', 'Action'))


def run(grammar):
    global parsing_table
    start_state, symbols = augment(grammar)
    start_state.closure()
    states.append(start_state)
    items = goto_operation()
    parsing_table = parsing_table_skeleton(symbols[0], symbols[1])
    slr_parsing_table(items)
    return items


def test(grammar, test_string):
    states_graph = run(grammar)
    for s in states:
        print(s.__str__().encode('utf-8').decode('utf-8'), end='\n')

    # draw(states_graph)

    print(parsing_table)

    driver_table = moves(test_string) # lexemes of test_string must be separated with spaces
    print(driver_table)

if __name__ == '__main__':
    print(augment.__doc__)
    g4 = """`E => `E + `T
    `E => `T 
    `T => `T * `F 
    `T => `F 
    `F => ( `E ) 
    `F => id"""

    print(g4, end='\n------grammar------\n\n')
    test(g4, 'id + id * id')
