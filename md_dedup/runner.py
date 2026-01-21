from langchain.llms import OpenAI
from loader import load_markdown, save_markdown
from passes import dedupe_within_section, merge_sections, global_consistency
import config

# Initialize cloud AI
llm = OpenAI(
    model_name=config.MODEL_NAME,
    temperature=config.TEMPERATURE,
    openai_api_key=config.OPENAI_API_KEY,
)


def run_pipeline(input_file, output_file):
    """
    Orchestrates the passes to clean up a markdown file.
    """
    # Load markdown
    sections = load_markdown(input_file)

    # Deduplicate within sections
    sections = [dedupe_within_section(s) for s in sections]

    # Merge overlapping sections using LLM
    merged_sections = []
    for i, sec in enumerate(sections):
        if i == 0:
            merged_sections.append(sec)
        else:
            prompt = f"Merge these two sections into one without losing information:\n{merged_sections[-1]}\n{sec}"
            merged_text = llm(prompt)
            merged_sections[-1] = merged_text

    # Global consistency
    final_sections = global_consistency(merged_sections)

    # Save cleaned markdown
    save_markdown(final_sections, output_file)

    print(f"✅ Cleaned Markdown saved to {output_file}")
