"use strict"

class Stack {
	constructor() {
		this._stk = []
		this._len = 0
	}

	push(x) {
		this._stk[this._len] = x
		this._len++
		return this
	}

	pop() {
		if (this.isEmpty())
			return [null, TypeError("Stack.pop: empty stack")]
		this._len--
		const x = this._stk[this._len]
		this._stk[this._len] = null
		return [x, null]
	}

	peek() {
		if (this.isEmpty())
			return [null, TypeError("Stack.peek: empty stack")]
		return [this._stk[this._len-1], null]
	}

	isEmpty() {
		return this._len === 0
	}

	toString() {
		return "<" + this._stk.slice(0, this._len).join(", ") + ">"
	}
}

