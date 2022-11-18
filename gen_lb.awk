#!/bin/awk -f

BEGIN {
	FS="\t"
	printf "<!DOCTYPE html>\n" \
"<html>\n" \
"<head>\n" \
"	<title>LinkBucket</title>\n" \
"	<meta charset=\"utf-8\" />\n" \
"	<link rel=\"stylesheet\" href=\"css/tag.css\" />\n" \
"	<link rel=\"stylesheet\" href=\"css/main.css\" />\n" \
"</head>\n" \
"<body>\n" \
"	<div id=\"main\">\n" \
"	<input type=\"text\" id=\"search\" />\n" \
"	<ul class=\"bucket\">\n"
}

NR != 1 {
	title=$1
	url=$2
	split($3, tags, ",")

	printf "		<li>\n" \
"			<a href=\"%s\">%s</a>\n" \
"			<span class=\"tags\">\n", url, title
	for (i in tags) {
		printf \
"				<span class=\"tag\">%s</span>\n", tags[i]
	}
	printf "			</span>\n" \
"		</li>\n"
}

END {
	printf "	</ul>\n" \
"	</div>\n" \
"	<script src=\"js/stairz.js\"></script>\n" \
"	<script src=\"js/search.js\"></script>\n" \
"</body>\n" \
"</html>\n"
}

