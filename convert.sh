script_dir="$(dirname "$0")"
md_file="$1"
dest_file="$2"

python="$script_dir/venv/bin/python"

$python "$script_dir/md_expand.py" "$md_file" > tmp.md
$python "$script_dir/md_transform.py" "tmp.md" "markdown.xsl" > "$dest_file"
rm tmp.md
