import os
import re
import sys

def strip_yaml_block(content):
    """Strip YAML block (--- delimited block at the beginning of a file)."""
    yaml_pattern = r"^---\n(.*?\n)---\n"
    return re.sub(yaml_pattern, "", content, flags=re.DOTALL)

def resolve_inclusions(file_path, base_dir=None, processed_files=None):
    """
    Resolve ![[file_to_include]] recursively.
    """
    if processed_files is None:
        processed_files = set()
    
    if base_dir is None:
        base_dir = os.path.dirname(file_path)

    if file_path in processed_files:
        return ""  # Prevent infinite recursion
    
    processed_files.add(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if file_path != input_file:
    	content = strip_yaml_block(content)

    inclusion_pattern = r"!\[\[(.+?)\]\]"
    def include_file(match):
        included_file = match.group(1)
        included_path = os.path.join(base_dir, included_file)
        if not os.path.isfile(included_path):
            return f"<!-- Missing file: {included_file} -->"
        return resolve_inclusions(included_path, os.path.dirname(included_path), processed_files)

    # Replace all ![[file_to_include]] occurrences
    resolved_content = re.sub(inclusion_pattern, include_file, content)

    return resolved_content

def process_markdown_file_to_stdout(input_file):
    """
    Process the input markdown file and output the result to stdout.
    """
    resolved_content = resolve_inclusions(input_file)
    sys.stdout.write(resolved_content)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]  # Take the input file path as a command-line argument
    process_markdown_file_to_stdout(input_file)

