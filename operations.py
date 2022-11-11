from stack import Stack

def main():
    unary_ops = ""
    binary_ops = "+-*/%"
    #infix = "1+2+(3+4+(5+6)+7+(8+(9)))+2+3+(3+(3+(3+((3+3)+3)+3)+3))"
    infix = input()
    infix = split_exp(infix, unary_ops+binary_ops)
    rpn = shunting_yard(infix, unary_ops, binary_ops)
    print(rpn)
    print(eval_rpn(rpn))

def split_exp(s, ops):
    out = []
    curr = ""
    for c in s:
        if c == " ":
            if curr != "":
                out.append(curr)
            curr = ""
        elif c in ops+"()":
            if curr != "":
                out.append(curr)
            out.append(c)
            curr = ""
        else:
            curr += c
    if curr != "":
        out.append(curr)
    return out

def shunting_yard(tokens, unary_ops, binary_ops):
    out = []
    ops = Stack()
    for t in tokens:
        if t in unary_ops:
            ops.push(t)
        elif t in binary_ops:
            while True:
                if ops.is_empty():
                    break
                if ops.peek() == "(":
                    break
                out.append(ops.pop())
            ops.push(t)
        elif t == "(":
            ops.push(t)
        elif t == ")":
            while True:
                assert not ops.is_empty()
                if ops.peek() == "(":
                    break
                out.append(ops.pop())
            assert ops.pop() == "("
            if not ops.is_empty and ops.peek() in unary_ops:
                out.append(ops.pop())
        else:
            out.append(t)

    while not ops.is_empty():
        op = ops.pop()
        assert op != "("
        out.append(op)

    return " ".join(out)

def eval_rpn(rpn):
    stk = Stack()
    for t in rpn.split(" "):
        if op == "+":
            x, y = float(stk.pop()), float(stk.pop())
            stk.push(x + y)
            continue
        if op == "-":
            x, y = float(stk.pop()), float(stk.pop())
            stk.push(x - y)
            continue
        if op == "*":
            x, y = float(stk.pop()), float(stk.pop())
            stk.push(x * y)
            continue
        if op == "/":
            x, y = float(stk.pop()), float(stk.pop())
            stk.push(x / y)
            continue
        if op == "%":
            x, y = float(stk.pop()), float(stk.pop())
            stk.push(x % y)
            continue
        stk.push(t)
    out = stk.pop()
    assert stk.is_empty(), f"wtf stk={str(stk)} is not empty"
    return out

if __name__ == "__main__":
    main()

