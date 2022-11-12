from inspect import signature
from stack import Stack

# Operations are in reverse
# because items are popped in reverse
MATH_OPS = {
    "+": lambda x, y : y+x,
    "-": lambda x, y : y-x,
    "*": lambda x, y : y*x,
    "/": lambda x, y : y/x,
    "%": lambda x, y : y%x,
}
BOOL_OPS = {
    "!": lambda x : not x,
    "&": lambda x, y : y and x,
    "|": lambda x, y : y or x,
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
        if t in ops and get_nargs(ops[t])==1:
            ops_stk.push(t)
            continue
        if t in ops and get_nargs(ops[t])==2:
            while not ops_stk.is_empty() and ops_stk.peek() != "(":
                rpn.append(ops_stk.pop())
            ops_stk.push(t)
            continue
        if t == "(":
            ops_stk.push(t)
            continue
        if t == ")":
            while True:
                assert not ops_stk.is_empty()
                if ops_stk.peek() == "(":
                    break
                rpn.append(ops_stk.pop())
            assert ops_stk.pop() == "("
            if not ops_stk.is_empty() and \
                ops_stk.peek() in ops and get_nargs(ops[ops_stk.peek()])==1:
                rpn.append(ops_stk.pop())
            continue
        rpn.append(t)
    while not ops_stk.is_empty():
        op = ops_stk.pop()
        assert op != "("
        rpn.append(op)
    return rpn

def get_nargs(f):
    """
    get number of arguments of f
    f: function
    return: int
    """
    return len(signature(f).parameters)

def eval_rpn(rpn, ops, f = lambda x : x):
    """
    evaluate expression in RPN
    rpn: iterable<str>
    ops: dict<str, function>
    f: function, apply f to each non-operator token
    return: object
    """
    stk = Stack()
    for t in rpn:
        if t in ops:
            args = (stk.pop() for _ in range(get_nargs(ops[t])))
            stk.push(ops[t](*args))
            continue
        stk.push(f(t))
    out = stk.pop()
    assert stk.is_empty(), f"wtf stk={str(stk)} is not empty"
    return out

if __name__ == "__main__":
    main()

