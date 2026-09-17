#!/bin/sh

script_dir="$(cd "$(dirname "$0")" && pwd)"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.md> <output.html>" >&2
    exit 1
fi

md_file="$1"
dest_file="$2"

if [ ! -f "$md_file" ]; then
    echo "Error: input file not found: $md_file" >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required" >&2
    exit 1
fi

venv="$script_dir/venv"
python="$venv/bin/python"

if [ ! -x "$python" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$venv" || exit 1
   
    "$venv/bin/pip" install -r "$script_dir/requirements.txt" || exit 1 
    echo "Installing Python dependencies..."

fi

tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

"$python" "$script_dir/md_expand.py" "$md_file" > "$tmp_file"
"$python" "$script_dir/md_transform.py" "$tmp_file" "$script_dir/markdown.xsl" > "$dest_file"
