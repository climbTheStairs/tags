from stack import Stack
from operations import split_exp, shunting_yard

def main():
    head, items = get_items("songs.tsv")

    unary_ops = "!"
    binary_ops = "&|"
    infix = input()
    infix = split_exp(infix, unary_ops+binary_ops)
    rpn = shunting_yard(infix, unary_ops, binary_ops)

    name, _, tags = head
    print(name, tags, sep="\t")
    for name, by, tags in items:
        if eval_rpn(rpn, tags):
            print(name, " ".join(tags), sep="\t")

def get_items(fname):
    items = []
    with open(fname, "r") as f:
        head = f.readline()[:-1].split("\t")
        for l in f:
            name, by, tags = l[:-1].split("\t")
            by = set(by.split(","))
            tags = set(tags.split(","))
            items.append((name, by, tags))
    return head, items

def eval_rpn(rpn, tags):
    stk = Stack()
    for t in rpn.split(" "):
        if t == "!":
            stk.push(not stk.pop())
        elif t == "&":
            x, y = stk.pop(), stk.pop()
            stk.push(x and y)
        elif t == "|":
            x, y = stk.pop(), stk.pop()
            stk.push(x or y)
        else:
            stk.push(t in tags)
    out = stk.pop()
    assert stk.is_empty(), f"wtf stk={str(stk)} is not empty"
    return out

if __name__ == "__main__":
    main()

