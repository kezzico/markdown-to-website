#  REPLACING THESE COMMANDS WITH A SINGLE PYTHON SCRIPT
#   pandoc --quiet \
#           --from=markdown-markdown_in_html_blocks+raw_html+auto_identifiers+header_attributes \
#           "tmp.md" -o "tmp.xml" \
#           --template="$script_dir/template.xml"

#   # Apply XSLT transformation
#   xmlstarlet tr "$script_dir/markdown.xsl" "tmp.xml" > "$output_dir/${base_name}.html"
#   if [ $? -eq 0 ]; then
#     echo "\033[0;32m*** success ***\033[0m"
#   else
#     echo "\033[0;31m*** fail ***\033[0m"
#   fi


import sys
import pypandoc
import lxml.etree as etree
from read_markdown import read_markdown
from md_expand import resolve_inclusions

def transform_markdown(document_params, markdown, xslt_file='markdown.xsl'):
  try:
    html_content = pypandoc.convert_text(
      markdown, 'html', format='md')

    # print(f"html content >>>>>>>>>>>>>>>>>: {html_content}")
    # Parse the XSLT file and apply the transformation
    xslt_root = etree.parse(xslt_file)
    transform = etree.XSLT(xslt_root)
    doc = etree.Element("document", **{str(k): str(v) for k, v in document_params.items()})
    doc.append(etree.fromstring(f"<content>{html_content}</content>", parser=etree.HTMLParser()).find("body/content"))
    html_tree = doc
    # print(f"html_tree >>>>>>>>>>>>>>>>>: {etree.tostring(html_tree, pretty_print=True, encoding='unicode')}")

    return str(transform(html_tree))

  except KeyError as e:
    print(f"incomplete data in transform_mail {e}")

  except Exception as e:
    print(f"unexpected error transforming: {e}")

  return None


def process_markdown_file_to_stdout(md_file, xslt_file='markdown.xsl'):
    """
    Process the input markdown file and output the result to stdout.
    """
    metadata, markdown = read_markdown(md_file)
    # print(f"Processing markdown file: {md_file}")
    # print(f"Metadata: {metadata}")
    # print(f"Markdown content length: {len(markdown)} characters")
    # Transform the markdown to HTML using the provided XSLT file
    if not markdown:
        print("No markdown content to transform.")
        return
    if not xslt_file:
        print("No XSLT file provided for transformation.")
        return
    if not metadata:
        print("No metadata found in the markdown file.")
        return

    # Transform the markdown to HTML

    # resolved_markdown = resolve_inclusions(markdown)
    # resolved_markdown_plus_footer =  resolved_markdown + "\n\n<!-- Footer content can be added here -->"

    html = transform_markdown(metadata, markdown, xslt_file)
    sys.stdout.write(html)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Usage: python script.py <input_file> <xslt_file>")
        print("Please provide the input markdown file path as a command-line argument.")
        sys.exit(1)
    
    md_file = sys.argv[1]  # Take the input file path as a command-line argument
    xsl_file = sys.argv[2]  # Take the XSLT file path as a command-line argument
    process_markdown_file_to_stdout(md_file, xsl_file)


