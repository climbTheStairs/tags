class Stack:
    def __init__(self):
        self._stk = []
        self._len = 0
    def push(self, x):
        assert len(self._stk) >= self._len, \
            f"Stack.push: wtf " \
            f"{len(self._stk)=} < {self._len=}, stk={str(self)}"
        if len(self._stk) > self._len:
            self._stk[self._len] = x
        else:
            self._stk.append(x)
        self._len += 1
        return self
    def pop(self):
        assert not self.is_empty(), \
            "Stack.pop: cannot pop empty stack"
        self._len -= 1
        return self._stk[self._len]
    def peek(self):
        assert not self.is_empty(), \
            "Stack.peek: cannot peek empty stack"
        return self._stk[self._len-1]
    def is_empty(self):
        return self._len == 0
    def __str__(self):
        return "<" + ", ".join(str(x) for x in self._stk[:self._len]) + ">"

