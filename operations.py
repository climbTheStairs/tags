from os import sys

from stack import Stack

# Operations are in reverse
# because items are popped in reverse
MATH_OPS = {
    "+": { "arity": 2, "op": lambda x, y : y+x },
    "-": { "arity": 2, "op": lambda x, y : y-x },
    "*": { "arity": 2, "op": lambda x, y : y*x },
    "/": { "arity": 2, "op": lambda x, y : y/x },
    "%": { "arity": 2, "op": lambda x, y : y%x },
}
BOOL_OPS = {
    "!": { "arity": 1, "op": lambda x : not x },
    "&": { "arity": 2, "op": lambda x, y : y and x },
    "|": { "arity": 2, "op": lambda x, y : y or x },
}
BOOL_OPS_PY = {
    "not": { "arity": 1, "op": lambda x : not x },
    "and": { "arity": 2, "op": lambda x, y : y and x },
    "or":  { "arity": 2, "op": lambda x, y : y or x },
}

def main():
    infix = input()
    #infix = "1+2+(3+4+(5+6)+7+(8+(9)))+2+3+(3+(3+(3+((3+3)+3)+3)+3))"
    infix = split_exp(infix, MATH_OPS)

    rpn, e = infix_to_rpn(infix, MATH_OPS)
    if e is not None:
        sys.exit(e)
    print("RPN:", " ".join(rpn))

    res, e = eval_rpn(rpn, MATH_OPS, float)
    if e is not None:
        sys.exit(e)
    print("Result:", res)

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
        if c in ops or c in "()" or c == " ":
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
    using Dijkstra's shunting yard algorithm;
    see <https://en.wikipedia.org/wiki/Shunting_yard_algorithm?oldid=1102884909#The_algorithm_in_detail>
    tokens: iterable<str>
    ops: dict<str, dict<"arity": int, "op": function>>
    return: list<str>, ValueError
    """
    rpn = []
    ops_stk = Stack() # operators stack
    for t in tokens:
        if t in ops and ops[t]["arity"]==1:
            ops_stk.push(t)
            continue
        if t in ops and ops[t]["arity"]==2:
            while True:
                op, e = ops_stk.peek()
                if type(e) == IndexError:
                    break
                if op == "(":
                    break
                op, _ = ops_stk.pop()
                rpn.append(op)
            ops_stk.push(t)
            continue
        if t == "(":
            ops_stk.push(t)
            continue
        if t == ")":
            while True:
                op, e = ops_stk.pop()
                if type(e) == IndexError:
                    return rpn, ValueError("infix_to_rpn: unmatched \")\"")
                if op == "(":
                    break
                rpn.append(op)
            continue
        rpn.append(t)
    while True:
        op, e = ops_stk.pop()
        if type(e) == IndexError:
            break
        if op == "(":
            return rpn, ValueError("infix_to_rpn: unmatched \"(\"")
        rpn.append(op)
    return rpn, None

def eval_rpn(rpn, ops, f = lambda x : x):
    """
    evaluate expression in RPN
    rpn: iterable<str>
    ops: dict<str, dict<"arity": int, "op": function>>
    f: function, apply f to each non-operator token
    return: object, ValueError
    """
    if len(rpn) == 0:
        return None, ValueError("eval_rpn: empty expression")
    stk = Stack()
    for t in rpn:
        if t in ops:
            args = []
            for _ in range(ops[t]["arity"]):
                arg, e = stk.pop()
                if type(e) == IndexError:
                    return None, ValueError("eval_rpn: " \
                        f"missing operand(s) for operation \"{t}\"")
                args.append(arg)
            stk.push(ops[t]["op"](*args))
            continue
        stk.push(f(t))
    out, _ = stk.pop() # stk cannot be possibly empty here
    if not stk.is_empty():
        return None, ValueError("eval_rpn: " \
            "expression contains multiple unrelated values")
    return out, None

if __name__ == "__main__":
    main()

