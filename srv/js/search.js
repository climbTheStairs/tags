const { $, $$ } = stairz.getShortcuts()

const BOOL_OPS = {
    "!": { arity: 1, op: x=>!x },
    "&": { arity: 2, op: (x, y)=>y&&x },
    "|": { arity: 2, op: (x, y)=>y||x },
}

const getBucket = async () => [...$$(".bucket > li")].map($li => {
	const title = $li.$("a").textContent
	const url = $li.$("a").href
	const tags = [...$li.$(".tags").children]
		.map($tag => $tag.textContent)
	return { $li, title, url, tags }
})

const evalRpn = (rpn, ops, f = x=>x) => {
	if (rpn.length <= 0)
		throw Error("evalRpn: cannot evaluate empty expression")
	const stk = []
	rpn.forEach(t => {
		if (ops.hasOwnProperty(t)) {
			const args = []
			for (let i = 0; i < ops[t].arity; i++) {
				if (stk.length === 0)
					throw Error("evalRpn: missing operand(s)")
				args.push(stk.pop())
			}
			stk.push(ops[t].op(...args))
			return
		}
		stk.push(f(t))
	})
	if (stk.length === 0)
		throw Error("evalRpn: wtf, missing expression")
	const out = stk.pop()
	if (stk.length !== 0)
		throw Error(`evalRpn: wtf, stk=[${stk}] is not empty`)
	return out
}

const filt = async (q) => {
	const bucket = await getBucket()
	bucket.forEach(({ $li, tags }) => {
		//if (!tags.includes(q)) {
		if (!evalRpn(q.split(" "), BOOL_OPS, x=>tags.includes(x))) {
			$li.css({ display: "none" })
			return
		}
		$li.css({ display: "" })
	})
}

$("#search").onkeydown = function({ key }) {
	if (key === "Enter") {
		const q = this.value.trim().toLowerCase()
		//console.time(q)
		filt(q)
		//console.timeEnd(q)
		return
	}
}

