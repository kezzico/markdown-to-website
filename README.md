# Markdown to Website Converter

A small shell-based Markdown to HTML converter with minimal dependencies.

The converter supports a subset of markdown features. With more advanced features intentionally ignored by the parser.

The goal is to create a markdown to html pipeline

## Requirements

* Python
* POSIX-compatible shell environment

## Usage

The converter takes a Markdown file and an output HTML file:

```sh
./convert.sh input.md output.html
```

For example:

```sh
./convert.sh ./www/index.md ./public/index.html
```

## Styling

Markdown to Website uses XSLT to transform the XML output

The transformation is defined in [`markdown.xsl`](markdown.xsl).

This makes the presentation layer independent from the Markdown itself. Modify the XSLT stylesheet to change the generated HTML without changing your Markdown files.

## How It Works

The conversion pipeline is intentionally simple:

```text
Markdown
   │
   ▼
  XML
   │
   ▼
markdown.xslt
   │
   ▼
 Website
```

A custom parser handles Markdown parsing and produces the initial HTML representation. The XSLT stylesheet then transforms that output into the final HTML used by the website.

## Metadata

You can add metadata to the top of a Markdown file using a YAML front matter block:

```yaml
---
title: My webpage
author: Lee Irvine
image: https://example.com/image.jpg
---
```

The metadata values are passed through to the XSLT transformation as attributes on the root document element.

For example, the metadata above is made available to the XSLT as attributes corresponding to:

```xml
<document
    title="My webpage"
    author="Lee Irvine"
    image="https://example.com/image.jpg">
```

This allows the XSLT stylesheet to use page metadata when generating the final HTML.

You can define additional metadata fields as needed. The fields are passed through to the XSLT as document attributes.

## License

Markdown to Website is licensed under the MIT License


See [LICENSE](LICENSE).
