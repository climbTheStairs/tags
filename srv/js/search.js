"use strict"

const { $, $$ } = stairz.getShortcuts()

const bucket = [...$$(".bucket > li")].map($li => {
	const title = $li.$("a").textContent
	const url = $li.$("a").href
	const tags = [...$li.$(".tags").children]
		.map($tag => $tag.textContent)
	return { $li, title, url, tags }
})

const filt = async (q) => {
	const infix = splitExp(q, Object.keys(BOOL_OPS))
	const [rpn, e] = infixToRpn(infix, BOOL_OPS)
	if (e !== null) {
		window.alert(e.message)
		return
	}
	for (const { $li, tags } of bucket) {
		const [isMatching, e] = evalRpn(
			rpn,
			BOOL_OPS,
			tags.includes.bind(tags),
		)
		if (e !== null) {
			window.alert(e.message)
			return
		}
		if (!isMatching) {
			$li.css({ display: "none" })
			continue
		}
		$li.css({ display: "" })
	}
}

$("#search").onkeydown = function({ key }) {
	if (key === "Enter") {
		const q = this.value.toLowerCase()
		//console.time(q)
		filt(q)
		//console.timeEnd(q)
		return
	}
}

