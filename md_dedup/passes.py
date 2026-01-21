# passes.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from difflib import SequenceMatcher


def dedupe_within_section(text):
    """
    Remove exact duplicate lines within a single section.
    """
    seen = set()
    result = []
    for line in text.split("\n"):
        if line not in seen:
            seen.add(line)
            result.append(line)
    return "\n".join(result)


def semantic_dedupe_lines(lines, llm, threshold=0.85):
    """
    Remove semantically similar lines using fuzzy matching.
    Falls back to simpler difflib if LLM is not needed.
    """
    if len(lines) <= 1:
        return lines

    unique_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            unique_lines.append(line)
            continue

        is_duplicate = False
        for existing in unique_lines:
            if not existing.strip():
                continue
            # Use difflib for fast similarity check
            similarity = SequenceMatcher(None, line.lower(), existing.lower()).ratio()
            if similarity > threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_lines.append(line)

    return unique_lines


def calculate_section_similarity(sec1, sec2):
    """
    Calculate similarity between two sections using TF-IDF and cosine similarity.
    Returns a score between 0 and 1.
    """
    # Extract text content, removing headings for better comparison
    text1 = "\n".join(
        [line for line in sec1.content.split("\n") if not line.startswith("#")]
    )
    text2 = "\n".join(
        [line for line in sec2.content.split("\n") if not line.startswith("#")]
    )

    if not text1.strip() or not text2.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return float(similarity)
    except:
        # Fallback to simple word overlap if TF-IDF fails
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0


def should_compare_sections(sec1, sec2):
    """
    Determine if two sections should be compared for merging.
    Only compare sections at the same hierarchical level with the same parent.
    """
    # Must be at same heading level
    if sec1.heading_level != sec2.heading_level:
        return False

    # Must have the same parent (or both be root level)
    if sec1.parent != sec2.parent:
        return False

    # Don't compare a section with itself
    if sec1 == sec2:
        return False

    return True


def find_similar_section_groups(sections, threshold=0.7):
    """
    Group sections that are similar to each other.
    Only groups sections at the same hierarchical level with the same parent.
    Returns list of lists, where each inner list contains indices of similar sections.
    """
    n = len(sections)
    if n <= 1:
        return [[i] for i in range(n)]

    # Calculate similarity matrix (only for comparable sections)
    similarity_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if should_compare_sections(sections[i], sections[j]):
                sim = calculate_section_similarity(sections[i], sections[j])
                similarity_matrix[i][j] = sim
                similarity_matrix[j][i] = sim

    # Simple greedy clustering
    visited = set()
    groups = []

    for i in range(n):
        if i in visited:
            continue

        group = [i]
        visited.add(i)

        # Find all sections similar to this one (at same level, same parent)
        for j in range(i + 1, n):
            if j not in visited and should_compare_sections(sections[i], sections[j]):
                if similarity_matrix[i][j] >= threshold:
                    group.append(j)
                    visited.add(j)

        groups.append(group)

    return groups


def merge_sections_with_children(sections_to_merge):
    """
    Merge multiple sections including their children.
    Preserves the heading of the first section and combines children.
    """
    if len(sections_to_merge) == 1:
        return sections_to_merge[0]

    # Use first section as base
    first_section = sections_to_merge[0]
    merged_content = first_section.content

    # Collect all children from all sections
    all_children = list(first_section.children)

    # Append content from other sections (without their headings)
    for sec in sections_to_merge[1:]:
        # Remove heading from subsequent sections
        content_lines = sec.content.split("\n")
        non_heading_lines = [line for line in content_lines if not line.startswith("#")]
        merged_content += "\n" + "\n".join(non_heading_lines)

        # Collect children from this section
        all_children.extend(sec.children)

    # Update the first section with merged content
    first_section.update_content(merged_content)

    # Update children list
    first_section.children = all_children
    for child in all_children:
        child.parent = first_section

    return first_section


def merge_sections(sections_to_merge):
    """
    Simple merge of sections without children (for backward compatibility).
    """
    if len(sections_to_merge) == 1:
        return sections_to_merge[0]

    # Use first section's heading
    first_section = sections_to_merge[0]
    merged_content = first_section.content

    # Append content from other sections (without their headings)
    for sec in sections_to_merge[1:]:
        # Remove heading from subsequent sections
        content_lines = sec.content.split("\n")
        non_heading_lines = [line for line in content_lines if not line.startswith("#")]
        merged_content += "\n" + "\n".join(non_heading_lines)

    # Update the first section with merged content
    first_section.update_content(merged_content)
    return first_section


def global_consistency(sections):
    """
    Remove duplicate lines across all sections while preserving structure.
    Only removes exact duplicates that appear in multiple sections at the same level.
    """
    # Group sections by hierarchical level to avoid removing content across levels
    levels = {}
    for sec in sections:
        level = sec.heading_level
        if level not in levels:
            levels[level] = []
        levels[level].append(sec)

    # Process each level independently
    for level, level_sections in levels.items():
        seen_lines = set()

        for sec in level_sections:
            new_lines = []
            for line in sec.lines:
                # Keep heading lines always
                if line.strip().startswith("#"):
                    new_lines.append(line)
                elif line.strip() and line not in seen_lines:
                    seen_lines.add(line)
                    new_lines.append(line)
                elif not line.strip():
                    # Keep empty lines for formatting
                    new_lines.append(line)

            sec.update_content("\n".join(new_lines))

    return sections
