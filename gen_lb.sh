#!/bin/sh

ht=$(printf '\t')
f=${1:-'lb.tsv'}

cat << 'EOF'
<!DOCTYPE html>
<html>
<head>
	<title>LinkBucket</title>
	<meta charset="utf-8" />
	<link rel="stylesheet" href="css/tag.css" />
	<link rel="stylesheet" href="css/main.css" />
</head>
<body>
	<div id="main">
		<input type="text" id="search" />
		<ul class="bucket">
EOF

tail -n +2 "$f" | while IFS="$ht" read -r title url tags; do
	cat << EOF
			<li>
				<a href="$url">$title</a>
				<span class="tags">
EOF
	printf '%s' "$tags" | awk -v RS=, '{
	printf "\t\t\t\t\t<span class=\"tag\">%s</span>\n", $0
}'
	cat << EOF
				</span>
			</li>
EOF
done

cat << 'EOF'
		</ul>
	</div>
	<script src="js/stairz.js"></script>
	<script src="js/search.js"></script>
</body>
</html>
EOF

