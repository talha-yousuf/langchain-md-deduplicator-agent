def load_markdown(file_path):
    """
    Load a markdown file and split it into sections by headings.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sections = []
    current_section = []

    for line in lines:
        if line.startswith("#") and current_section:
            sections.append("".join(current_section))
            current_section = [line]
        else:
            current_section.append(line)
    if current_section:
        sections.append("".join(current_section))

    return sections


def save_markdown(sections, file_path):
    """
    Save sections back into a markdown file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for sec in sections:
            f.write(sec + "\n")
