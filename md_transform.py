import re
import sys
import os
import lxml.etree as etree
from read_markdown import read_markdown
from md_expand import resolve_inclusions

INLINE_RE = re.compile(
    r"""
    (`[^`]+`) |
    (\*\*.+?\*\*) |
    (__.+?__) |
    (\*.+?\*) |
    (_.+?_) |
    (!\[[^\]]*\]\([^)]+\)) |
    (\[[^\]]+\]\([^)]+\))
    """,
    re.VERBOSE,
)


def append_text(element, text):
    if not text:
        return

    if len(element):
        child = element[-1]
        child.tail = (child.tail or "") + text
    else:
        element.text = (element.text or "") + text


def parse_inline(text, element):
    pos = 0

    for match in INLINE_RE.finditer(text):
        append_text(element, text[pos:match.start()])

        value = match.group(0)

        if value.startswith("`"):
            child = etree.SubElement(element, "code")
            child.text = value[1:-1]

        elif value.startswith(("**", "__")):
            child = etree.SubElement(element, "strong")
            child.text = value[2:-2]

        elif value.startswith(("*", "_")):
            child = etree.SubElement(element, "em")
            child.text = value[1:-1]

        elif value.startswith("!["):
            match_image = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", value)
            child = etree.SubElement(element, "img")
            child.set("alt", match_image.group(1))
            child.set("src", match_image.group(2))

        elif value.startswith("["):
            match_link = re.match(r"\[([^\]]+)\]\(([^)]+)\)", value)
            child = etree.SubElement(element, "a")
            child.set("href", match_link.group(2))
            child.text = match_link.group(1)

        pos = match.end()

    append_text(element, text[pos:])


def flush_paragraph(content, lines):
    if not lines:
        return

    element = etree.SubElement(content, "p")

    for index, line in enumerate(lines):
        # Three trailing spaces = hard line break
        hard_break = line.endswith("   ")

        if hard_break:
            line = line[:-3]

        parse_inline(line, element)

        if hard_break and index < len(lines) - 1:
            etree.SubElement(element, "br")

        elif index < len(lines) - 1:
            append_text(element, " ")


def parse_markdown(markdown, document_params=None):
    document_params = document_params or {}

    doc = etree.Element(
        "document",
        **{str(k): str(v) for k, v in document_params.items()},
    )

    content = etree.SubElement(doc, "content")

    paragraph_lines = []
    code_lines = []
    in_code = False
    code_language = None
    current_list = None

    def flush():
        nonlocal paragraph_lines
        flush_paragraph(content, paragraph_lines)
        paragraph_lines = []


    def flush_list():
        nonlocal current_list
        current_list = None

    for line in markdown.splitlines():

        # ------------------------------------------------------------
        # Fenced code block
        # ------------------------------------------------------------

        if in_code:
            if line.startswith("```"):
                element = etree.SubElement(content, "pre")
                code = etree.SubElement(element, "code")

                if code_language:
                    code.set("class", f"language-{code_language}")

                code.text = "\n".join(code_lines) + "\n"

                code_lines = []
                code_language = None
                in_code = False
            else:
                code_lines.append(line)

            continue

        if line.startswith("```"):
            flush()

            in_code = True
            code_language = line[3:].strip() or None
            continue

        # ------------------------------------------------------------
        # Blank line terminates a paragraph
        # ------------------------------------------------------------

        if not line.strip():
            flush()
            continue

        # ------------------------------------------------------------
        # Headings
        # ------------------------------------------------------------

        match = re.match(r"^(#{1,6})\s+(.*)$", line)

        if match:
            flush()

            level = len(match.group(1))
            element = etree.SubElement(content, f"h{level}")
            parse_inline(match.group(2), element)
            continue

        # ------------------------------------------------------------
        # Unordered list
        # ------------------------------------------------------------

        match = re.match(r"^\s*[-*+]\s+(.*)$", line)

        if match:
            flush()

            if current_list is None:
                current_list = etree.SubElement(content, "ul")

            element = etree.SubElement(current_list, "li")
            parse_inline(match.group(1), element)
            continue

        # ------------------------------------------------------------
        # Normal paragraph line
        # ------------------------------------------------------------
        flush_list()
        paragraph_lines.append(line)

    # Flush anything left at EOF
    if in_code:
        element = etree.SubElement(content, "pre")
        code = etree.SubElement(element, "code")
        code.text = "\n".join(code_lines) + "\n"
    else:
        flush()

    return doc

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
        print("No markdown content to transform.", file=sys.stderr)
        return
    if not xslt_file:
      print("No XSLT file provided for transformation.", file=sys.stderr)
      return
    if not os.path.isfile(xslt_file):
      print(f"XSLT file not found: {xslt_file}", file=sys.stderr)
      return
    if not metadata:
      metadata = {}

    try:
      # resolved_markdown = resolve_inclusions(markdown)
      xml = parse_markdown(markdown, metadata)

      xslt_root = etree.parse(xslt_file)
      transform = etree.XSLT(xslt_root)
      # debugger output
      # print(etree.tostring(xml, pretty_print=True, encoding='unicode'), file=sys.stderr)
      sys.stdout.write(str(transform(xml)))
    except KeyError as e:
      print(f"incomplete data in transform_mail {e}", file=sys.stderr)

    except Exception as e:
      print(f"unexpected error transforming: {e}", file=sys.stderr)

    
    

# Example usage
if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Usage: python script.py <input_file> <xslt_file>")
        print("Please provide the input markdown file path as a command-line argument.")
        sys.exit(1)
    
    md_file = sys.argv[1]  # Take the input file path as a command-line argument
    xsl_file = sys.argv[2]  # Take the XSLT file path as a command-line argument
    process_markdown_file_to_stdout(md_file, xsl_file)


