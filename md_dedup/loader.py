## loader.py

import re


class Section:
    """
    Represents a markdown section with metadata and hierarchy.
    """

    def __init__(
        self, content, heading_level=0, heading_text="", position=0, parent=None
    ):
        self.content = content
        self.heading_level = heading_level
        self.heading_text = heading_text
        self.position = position
        self.parent = parent  # Reference to parent section
        self.children = []  # List of child sections
        self.lines = content.split("\n")

    def __str__(self):
        return self.content

    def update_content(self, new_content):
        self.content = new_content
        self.lines = new_content.split("\n")

    def add_child(self, child):
        """Add a child section to this section."""
        self.children.append(child)
        child.parent = self

    def is_child_of(self, other):
        """Check if this section is a child of another section."""
        return self.parent == other

    def get_full_path(self):
        """Get the full heading path (e.g., 'Main > Sub > SubSub')"""
        if self.parent and self.parent.heading_text:
            return f"{self.parent.get_full_path()} > {self.heading_text}"
        return self.heading_text


def build_section_hierarchy(flat_sections):
    """
    Build a hierarchy tree from flat list of sections based on heading levels.
    Returns root sections (top-level) with children attached.
    """
    if not flat_sections:
        return []

    # Stack to track parent sections at each level
    parent_stack = [None]  # Start with root level
    root_sections = []

    for section in flat_sections:
        level = section.heading_level

        # Pop stack until we find the appropriate parent level
        while len(parent_stack) > level:
            parent_stack.pop()

        # Add this section to appropriate parent
        if parent_stack[-1] is not None:
            parent_stack[-1].add_child(section)
        else:
            # Top-level section
            root_sections.append(section)

        # Add this section to stack as potential parent
        parent_stack.append(section)

    return root_sections


def flatten_hierarchy(root_sections):
    """
    Flatten a hierarchical tree back to a list of sections.
    Maintains document order.
    """
    flat = []

    def traverse(section):
        flat.append(section)
        for child in section.children:
            traverse(child)

    for root in root_sections:
        traverse(root)

    return flat


def load_markdown(file_path):
    """
    Load a markdown file and split it into sections with hierarchy.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sections = []
    current_section = []
    current_heading_level = 0
    current_heading_text = ""

    for i, line in enumerate(lines):
        # Check if line is a heading
        heading_match = re.match(r"^(#{1,6})\s+(.+)", line)

        if heading_match and current_section:
            # Save previous section
            content = "".join(current_section)
            sections.append(
                Section(
                    content=content,
                    heading_level=current_heading_level,
                    heading_text=current_heading_text,
                    position=len(sections),
                )
            )
            # Start new section
            current_heading_level = len(heading_match.group(1))
            current_heading_text = heading_match.group(2).strip()
            current_section = [line]
        elif heading_match and not current_section:
            # First heading in document
            current_heading_level = len(heading_match.group(1))
            current_heading_text = heading_match.group(2).strip()
            current_section = [line]
        else:
            current_section.append(line)

    # Add final section
    if current_section:
        content = "".join(current_section)
        sections.append(
            Section(
                content=content,
                heading_level=current_heading_level,
                heading_text=current_heading_text,
                position=len(sections),
            )
        )

    # Build hierarchy
    root_sections = build_section_hierarchy(sections)

    # Return flattened list with hierarchy preserved in parent/child relationships
    return flatten_hierarchy(root_sections)


def save_markdown(sections, file_path):
    """
    Save sections back into a markdown file, preserving hierarchy.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for i, sec in enumerate(sections):
            # Add section content
            f.write(sec.content)
            # Add newline between sections if not the last one
            if i < len(sections) - 1 and not sec.content.endswith("\n"):
                f.write("\n")
