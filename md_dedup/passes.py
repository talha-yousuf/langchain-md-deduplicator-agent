def dedupe_within_section(text):
    """
    Remove duplicate lines within a single section.
    """
    seen = set()
    result = []
    for line in text.split("\n"):
        if line not in seen:
            seen.add(line)
            result.append(line)
    return "\n".join(result)


def merge_sections(sec1, sec2):
    """
    Merge two sections while removing duplicates.
    """
    return dedupe_within_section(sec1 + "\n" + sec2)


def global_consistency(sections):
    """
    Remove duplicate lines across all sections.
    """
    seen_lines = set()
    final_sections = []

    for sec in sections:
        new_sec = []
        for line in sec.split("\n"):
            if line not in seen_lines:
                seen_lines.add(line)
                new_sec.append(line)
        final_sections.append("\n".join(new_sec))

    return final_sections
