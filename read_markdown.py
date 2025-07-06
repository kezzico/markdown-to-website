import yaml

def read_markdown(path):
  try:
    with open(path, 'r', encoding='utf-8') as file:
      lines = file.readlines()

      # Variables to store metadata and the content
      metadata_lines = []
      content_lines = []
      in_metadata = False
      metadata_complete = False

      # Loop through the file line by line
      for line in lines:
        if line.strip() == "---" and not metadata_complete:
          if not in_metadata:
            # Start of metadata block
            in_metadata = True
          else:
            # End of metadata block
            in_metadata = False
            metadata_complete = True

        elif in_metadata:
          metadata_lines.append(line)
        else:
          content_lines.append(line)

      # Parse the YAML metadata
    metadata = yaml.safe_load("\n".join(metadata_lines))

    # The rest of the markdown content (after the metadata)
    markdown = "".join(content_lines)

    return metadata, markdown

  except Exception as e:
    print(f"Error reading markdown file: {e}")
    return None, None

