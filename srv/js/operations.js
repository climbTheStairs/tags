"use strict"

const BOOL_OPS = {
	"!": { arity: 1, op: x=>!x },
	"&": { arity: 2, op: (x, y)=>y&&x },
	"|": { arity: 2, op: (x, y)=>y||x },
}

const splitExp = (exp, ops) => {
	/*
	split expression into tokens
	exp: string, typically in infix notation
	ops: array<string>
	return: array<string>
	*/
	const tokens = []
	let curr = ""
	for (const c of exp+" ") {
		if (ops.includes(c) || "()".includes(c) || c === " ") {
			if (curr !== "") {
				tokens.push(curr)
				curr = ""
			}
			if (c !== " ") {
				tokens.push(c)
			}
			continue
		}
		curr += c
	}
	return tokens
}

const processOp = (rpn, opsStk) => {
	while (true) {
		const [op, e] = opsStk.peek()
		if (e instanceof TypeError)
			return
		if (op === "(")
			return
		const [,] = opsStk.pop()
		rpn.push(op)
	}
}

const processParen = (rpn, opsStk) => {
	while (true) {
		const [op, e] = opsStk.pop()
		if (e instanceof TypeError)
			return RangeError(`infixToRpn: unmatched ")"`)
		if (op === "(")
			return null
		rpn.push(op)
	}
}

const processEnd = (rpn, opsStk) => {
	while (true) {
		const [op, e] = opsStk.pop()
		if (e instanceof TypeError)
			return null
		if (op === "(")
			return RangeError(`infixToRpn: unmatched "("`)
		rpn.push(op)
	}
}

const infixToRpn = (tokens, ops) => {
	/*
	convert list of tokens of expression in infix notation
	to reverse Polish notation (RPN)
	using Dijkstra's shunting yard algorithm;
	see <https://en.wikipedia.org/wiki/Shunting_yard_algorithm?oldid=1102884909#The_algorithm_in_detail>
	tokens: array<string>
	ops: object<string, function>
	return: [array<string>, RangeError]
	*/
	const rpn = []
	const opsStk = new Stack() // operators stack
	for (const t of tokens) {
		if (ops.hasOwnProperty(t) && ops[t].arity===1) {
			opsStk.push(t)
			continue
		}
		if (ops.hasOwnProperty(t) && ops[t].arity===2) {
			processOp(rpn, opsStk)
			opsStk.push(t)
			continue
		}
		if (t === "(") {
			opsStk.push(t)
			continue
		}
		if (t == ")") {
			const e = processParen(rpn, opsStk)
			if (e instanceof RangeError)
				return [rpn, e]
			continue
		}
		rpn.push(t)
	}
	return [rpn, processEnd(rpn, opsStk)]
}

const pushOpRes = (stk, op) => {
	const args = []
	for (let i = 0; i < op.arity; i++) {
		const [arg, e] = stk.pop()
		if (e instanceof TypeError)
			return RangeError("evalRpn: " +
				`missing operand(s) for operation "${t}"`)
		args.push(arg)
	}
	stk.push(op.op(...args))
	return null
}

const evalRpn = (rpn, ops, f = x=>x) => {
	/*
	evaluate expression in RPN
	rpn: array<string>
	ops: object<object<arity: number, op: function>>
	f: function, apply f to each non-operator token
	return: object, RangeError
	*/
	if (rpn.length == 0)
		return [null, RangeError("evalRpn: empty expression")]
	const stk = new Stack()
	for (const t of rpn) {
		if (ops.hasOwnProperty(t)) {
			const e = pushOpRes(stk, ops[t])
			if (e instanceof RangeError)
				return [null, e]
			continue
		}
		stk.push(f(t))
	}
	const [out,] = stk.pop() // stk cannot be possibly empty here
	if (!stk.isEmpty())
		return [null, RangeError("evalRpn: " +
			"expression contains multiple unrelated values")]
	return [out, null]
}

