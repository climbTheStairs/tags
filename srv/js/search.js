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

const filt = async (q) => {
	const bucket = await getBucket()
	bucket.forEach(({ $li, tags }) => {
		if (!evalRpn(q.split(" "), BOOL_OPS, x=>tags.includes(x)))
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

