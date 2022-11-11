from stack import Stack
from operations import split_exp, infix_to_rpn, eval_rpn

def main():
    ops = {
        "!": lambda x : not x,
        "&": lambda x, y : x and y,
        "|": lambda x, y : x or y,
    }

    infix = input()
    infix = split_exp(infix, ops)
    rpn = infix_to_rpn(infix, ops)

    head, items = get_items("songs.tsv")

    print("\t".join(head))
    for name, by, tags in items:
        if eval_rpn(rpn, ops, lambda x : x in tags):
            print(name, ", ".join(by), " ".join(tags), sep="\t")

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

if __name__ == "__main__":
    main()

