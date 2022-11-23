class Stack:
    def __init__(self):
        self._stk = []
        self._len = 0

    def push(self, x):
        if len(self._stk) > self._len:
            self._stk[self._len] = x
        else:
            self._stk.append(x)
        self._len += 1
        return self

    def pop(self):
        if self.is_empty():
            return None, IndexError("Stack.pop: empty stack")
        self._len -= 1
        x = self._stk[self._len]
        self._stk[self._len] = None
        return x, None

    def peek(self):
        if self.is_empty():
            return None, IndexError("Stack.peek: empty stack")
        return self._stk[self._len-1], None

    def is_empty(self):
        return self._len == 0

    def __str__(self):
        return "<" + ", ".join(str(x) for x in self._stk[:self._len]) + ">"

