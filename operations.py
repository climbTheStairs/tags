from stack import Stack

# Operations are in reverse
# because items are popped in reverse
MATH_OPS = {
    "+": { "nargs": 2, "f": lambda x, y : y+x },
    "-": { "nargs": 2, "f": lambda x, y : y-x },
    "*": { "nargs": 2, "f": lambda x, y : y*x },
    "/": { "nargs": 2, "f": lambda x, y : y/x },
    "%": { "nargs": 2, "f": lambda x, y : y%x },
}
BOOL_OPS = {
    "!": { "nargs": 1, "f": lambda x : not x },
    "&": { "nargs": 2, "f": lambda x, y : y and x },
    "|": { "nargs": 2, "f": lambda x, y : y or x },
}
BOOL_OPS_PY = {
    "not": { "nargs": 1, "f": lambda x : not x },
    "and": { "nargs": 2, "f": lambda x, y : y and x },
    "or":  { "nargs": 2, "f": lambda x, y : y or x },
}

def main():
    infix = input()
    infix = "1+2+(3+4+(5+6)+7+(8+(9)))+2+3+(3+(3+(3+((3+3)+3)+3)+3))" \
        if infix == "" else infix
    infix = split_exp(infix, MATH_OPS)
    rpn = infix_to_rpn(infix, MATH_OPS)
    print(" ".join(rpn))
    print(eval_rpn(rpn, MATH_OPS, float))

def split_exp(exp, ops):
    """
    split expression into tokens
    exp: str, typically in infix notation
    ops: iterable<str>
    return: list<str>
    """
    tokens = []
    curr = ""
    for c in exp+" ":
        if c in ops or c in "() ":
            if curr != "":
                tokens.append(curr)
                curr = ""
            if c != " ":
                tokens.append(c)
            continue
        curr += c
    return tokens

def infix_to_rpn(tokens, ops):
    """
    convert list of tokens of expression in infix notation
    to reverse Polish notation (RPN)
    using shunting yard algorithm invented by Edsger Dijkstra;
    see <https://en.wikipedia.org/wiki/Shunting_yard_algorithm?oldid=1102884909#The_algorithm_in_detail>
    tokens: iterable<str>
    ops: dict<str, function>
    return: list<str>
    """
    rpn = []
    ops_stk = Stack() # operators stack
    for t in tokens:
        if t in ops and ops[t]["nargs"]==1:
            ops_stk.push(t)
            continue
        if t in ops and ops[t]["nargs"]==2:
            while not ops_stk.is_empty() and ops_stk.peek() != "(":
                rpn.append(ops_stk.pop())
            ops_stk.push(t)
            continue
        if t == "(":
            ops_stk.push(t)
            continue
        if t == ")":
            while True:
                assert not ops_stk.is_empty(), \
                    "infix_to_rpn: unmatched \")\""
                op = ops_stk.pop()
                if op == "(":
                    break
                rpn.append(op)
            """
            if not ops_stk.is_empty() and \
                ops_stk.peek() in ops and ops[ops_stk.peek()]["nargs"]==1:
                rpn.append(ops_stk.pop())
            """
            continue
        rpn.append(t)
    while not ops_stk.is_empty():
        op = ops_stk.pop()
        assert op != "(", "infix_to_rpn: unmatched \"(\""
        rpn.append(op)
    return rpn

def eval_rpn(rpn, ops, f = lambda x : x):
    """
    evaluate expression in RPN
    rpn: iterable<str>
    ops: dict<str, function>
    f: function, apply f to each non-operator token
    return: object
    """
    assert len(rpn) > 0, "eval_rpn: cannot evaluate empty expression"
    stk = Stack()
    for t in rpn:
        if t in ops:
            args = []
            for _ in range(ops[t]["nargs"]):
                assert not stk.is_empty(), "eval_rpn: missing operand(s)"
                args.append(stk.pop())
            stk.push(ops[t]["f"](*args))
            continue
        stk.push(f(t))
    assert not stk.is_empty(), "eval_rpn: wtf, missing expression"
    out = stk.pop()
    assert stk.is_empty(), f"eval_rpn: wtf, stk={str(stk)} is not empty"
    return out

if __name__ == "__main__":
    main()

