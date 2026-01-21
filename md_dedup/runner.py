# runner.py

from langchain.llms import OpenAI
from loader import load_markdown, save_markdown
from passes import (
    dedupe_within_section,
    semantic_dedupe_lines,
    find_similar_section_groups,
    merge_sections_with_children,
    global_consistency,
)
from utils import print_info, print_error
import config

# Initialize cloud AI
llm = OpenAI(
    model_name=config.MODEL_NAME,
    temperature=config.TEMPERATURE,
    openai_api_key=config.OPENAI_API_KEY,
)


def llm_merge_sections(sections_to_merge, llm):
    """
    Use LLM to intelligently merge similar sections without losing information.
    Preserves children and hierarchy.
    """
    if len(sections_to_merge) == 1:
        return sections_to_merge[0]

    # Combine all section contents (only the section content, not children)
    combined_text = "\n\n---\n\n".join([sec.content for sec in sections_to_merge])

    # Get hierarchy info for context
    hierarchy_info = f"These sections are at level {sections_to_merge[0].heading_level}"
    if sections_to_merge[0].parent:
        hierarchy_info += f" under '{sections_to_merge[0].parent.heading_text}'"

    prompt = f"""You are helping to clean up a markdown document by merging similar/overlapping sections.

{hierarchy_info}

Below are {len(sections_to_merge)} sections that appear to cover similar topics. Please merge them into a single cohesive section:
- Keep the first heading (from the first section) at the same level
- Preserve all unique information from all sections
- Remove redundant or duplicate information
- Maintain markdown formatting
- Keep the content clear and well-organized
- Do NOT include any subsections (##, ###, etc.) - only merge the content at this level

Sections to merge:
{combined_text}

Return ONLY the merged markdown section, nothing else."""

    try:
        merged_content = llm(prompt)
        # Update first section with merged content
        sections_to_merge[0].update_content(merged_content.strip())

        # Merge children from all sections
        all_children = []
        for sec in sections_to_merge:
            all_children.extend(sec.children)

        sections_to_merge[0].children = all_children
        for child in all_children:
            child.parent = sections_to_merge[0]

        return sections_to_merge[0]
    except Exception as e:
        print_error(f"LLM merge failed: {e}. Falling back to simple merge.")
        return merge_sections_with_children(sections_to_merge)


def llm_semantic_dedupe(section, llm):
    """
    Use LLM to remove semantically duplicate content within a section.
    """
    if len(section.content.strip()) < 50:  # Skip very short sections
        return section

    prompt = f"""You are cleaning up a markdown section by removing semantically duplicate information.

Rules:
- Keep the heading exactly as-is
- Remove sentences or bullet points that convey the same information
- Keep all unique information
- Maintain markdown formatting
- Preserve the structure and flow

Section to clean:
{section.content}

Return ONLY the cleaned section, nothing else."""

    try:
        cleaned_content = llm(prompt)
        section.update_content(cleaned_content.strip())
    except Exception as e:
        print_error(f"LLM semantic dedup failed: {e}. Skipping.")

    return section


def run_pipeline(input_file, output_file):
    """
    Orchestrates the multi-pass cleanup pipeline.
    """
    print_info(f"Loading markdown from {input_file}")
    sections = load_markdown(input_file)
    print_info(f"Found {len(sections)} sections")

    # PASS 1: Exact deduplication within each section
    print_info("Pass 1: Removing exact duplicates within sections")
    for sec in sections:
        sec.update_content(dedupe_within_section(sec.content))

    # PASS 2: Semantic deduplication within sections using LLM
    print_info("Pass 2: Removing semantic duplicates within sections")
    sections = [llm_semantic_dedupe(sec, llm) for sec in sections]

    # PASS 3: Find and merge similar sections
    print_info("Pass 3: Identifying similar sections for merging")
    similar_groups = find_similar_section_groups(
        sections, threshold=config.SIMILARITY_THRESHOLD
    )

    # Filter out groups with only one section (nothing to merge)
    groups_to_merge = [g for g in similar_groups if len(g) > 1]
    print_info(f"Found {len(groups_to_merge)} groups of similar sections to merge")

    # Merge similar sections using LLM
    merged_sections = []
    processed_indices = set()

    for group in similar_groups:
        if group[0] in processed_indices:
            continue

        sections_to_merge = [sections[i] for i in group]

        if len(sections_to_merge) > 1:
            print_info(
                f"Merging {len(sections_to_merge)} similar sections: {[s.heading_text for s in sections_to_merge]}"
            )
            merged = llm_merge_sections(sections_to_merge, llm)
            merged_sections.append(merged)
        else:
            merged_sections.append(sections_to_merge[0])

        processed_indices.update(group)

    # PASS 4: Global consistency - remove cross-section duplicates
    print_info("Pass 4: Ensuring global consistency")
    final_sections = global_consistency(merged_sections)

    # Save cleaned markdown
    print_info(f"Saving cleaned markdown to {output_file}")
    save_markdown(final_sections, output_file)

    print_info(f"✅ Cleaned Markdown saved to {output_file}")
    print_info(
        f"Original sections: {len(sections)}, Final sections: {len(final_sections)}"
    )
