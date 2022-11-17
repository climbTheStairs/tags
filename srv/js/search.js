const { $, $$ } = stairz.getShortcuts()

const getBucket = async () => [...$$(".bucket > li")].map($li => {
	const title = $li.$("a").textContent
	const url = $li.$("a").href
	const tags = [...$li.$(".tags").children]
		.map($tag => $tag.textContent)
	return { $li, title, url, tags }
})

const filt = async (q) => {
	const bucket = await getBucket()
	bucket.forEach(({ $li, tags }) => {
		if (!tags.includes(q)) {
			$li.css({ display: "none" })
			return
		}
		$li.css({ display: "" })
	})
}

$("#search").onkeydown = function({ key }) {
	if (key == "Enter") {
		const q = this.value.toLowerCase()
		//console.time(q)
		filt(q)
		//console.timeEnd(q)
		return
	}
}

