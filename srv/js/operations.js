const BOOL_OPS = {
	"!": { arity: 1, op: x=>!x },
	"&": { arity: 2, op: (x, y)=>y&&x },
	"|": { arity: 2, op: (x, y)=>y||x },
}

const splitExp = (exp, ops) => {
	return exp.split(" ").filter(x => x.length !== 0)
}

const infixToRpn = (tokens, ops) => {
	return [tokens, null]
}

const evalRpn = (rpn, ops, f = x=>x) => {
	if (rpn.length == 0)
		return [null, RangeError("evalRpn: empty expression")]
	const stk = []
	for (const t of rpn) {
		if (ops.hasOwnProperty(t)) {
			const args = []
			for (let i = 0; i < ops[t].arity; i++) {
				arg = stk.pop()
				if (typeof arg === "undefined")
					return [null, RangeError("evalRpn: " +
						`missing operand(s) for operation "${t}"`)]
				args.push(arg)
			}
			stk.push(ops[t].op(...args))
			continue
		}
		stk.push(f(t))
	}
	const out = stk.pop()
	if (stk.length !== 0)
		return [null, RangeError("evalRpn: " +
			"expression contains multiple unrelated values")]
	return [out, null]
}

