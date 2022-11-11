from operations import split_exp, infix_to_rpn, eval_rpn, BOOL_OPS

def main():
    infix = split_exp(input(), BOOL_OPS)
    rpn = infix_to_rpn(infix, BOOL_OPS)

    head, items = get_items("songs.tsv")
    print("\t".join(head))
    for name, by, tags in items:
        if eval_rpn(rpn, BOOL_OPS, lambda x : x in tags):
            print(name, ", ".join(by), " ".join(tags), sep="\t")

def get_items(fname):
    """
    read TSV file and return head, items
    fname: str, valid name of file in TSV format
    return head: list<str>, first line of file
    return items: list<tuple<str, set<str>, set<str>>>
    """
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

