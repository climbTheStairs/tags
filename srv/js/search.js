const $ = document.querySelector.bind(document)
const $$ = document.querySelectorAll.bind(document)
Element.prototype.$ = Element.prototype.querySelector
Element.prototype.$$ = Element.prototype.querySelectorAll

const bucket = [...$$(".bucket > li")].map($li => {
	const title = $li.$("a").textContent
	const url = $li.$("a").href
	const tags = [...$li.$(".tags").children]
		.map($tag => $tag.textContent)
	return { $li, title, url, tags }
})

const filt = (q) => {
	bucket.forEach(({ $li, tags }) => {
		if (!tags.includes(q)) {
			$li.style.display = "none"
			return
		}
		$li.style.display = ""
	})
}

$("#search").onkeydown = function({ key }) {
	if (key == "Enter") {
		const q = this.value.toLowerCase()
		//console.time(q)
		filt(q)
		//console.timeEnd(q)
	}
}

