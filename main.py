from os import sys

from operations import split_exp, infix_to_rpn, eval_rpn, BOOL_OPS

def main():
    infix = input()
    fname = input()
    infix = split_exp(infix, BOOL_OPS)
    rpn, e = infix_to_rpn(infix, BOOL_OPS)
    if e is not None:
        sys.exit(e)
    with (sys.stdin if fname in ("", "-") else open(fname, "r")) as f:
        filter_tsv(f, rpn)

def filter_tsv(f, rpn):
    """
    read TSV file and print lines matching rpn
    f: file, in IANA standard-compliant TSV format
    rpn: iterable<str>
    return: NoneType
    """
    head = f.readline()[:-1].split("\t")
    try:
        itags = head.index("tags") # index of "tags" in head
    except ValueError:
        sys.exit("missing tags column")
    print("\t".join(head))

    for l in f:
        l = l[:-1].split("\t")
        tags = set(l[itags].split(","))
        #l[itags] = " ".join(tags)
        is_matching, e = eval_rpn(rpn, BOOL_OPS, lambda x : x in tags)
        if e is not None:
            sys.exit(e)
        if is_matching:
            print("\t".join(l))

if __name__ == "__main__":
    main()

