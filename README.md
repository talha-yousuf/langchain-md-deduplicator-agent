# md_dedup

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-CC_BY--NC_4.0-lightgrey)
![Status](https://img.shields.io/badge/status-MVP-yellow)

Markdown Deduplication and Cleanup Tool using langChain and OpenAI. Designed to process large Markdown files, remove redundancy, merge overlapping sections, and maintain coherent structure. Ideal for developers, technical writers, and anyone managing documentation.

---

## Table of Contents

- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [External Requirements](#external-requirements)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Functionality](#functionality)
- [Design Decisions](#design-decisions)
- [Next Steps](#next-steps-)
- [License](#license)

## Requirements

- **Python**: 3.10 or higher

## Dependencies

- `langchain` – Orchestrates calls to cloud LLM
- `openai` – Free-tier API for text generation / merge logic
- `rich` – CLI output formatting
- `click` – Command-line interface
- `tiktoken` – Token counting for OpenAI requests

## External Requirements

- **OpenAI API Key**

  ```bash
  # powershell
  setx OPENAI_API_KEY "your_api_key_here"
  # close and reopen terminal after running this

  # git bash / MINGW64
  export OPENAI_API_KEY="your_api_key_here"
  # for persistence, add the export to `~/.bashrc` and run `source ~/.bashrc`
  ```

## Installation and Setup

```bash
# bash

# 1. Clone Repository

git clone https://github.com/<your-username>/md_dedup.git
cd md_dedup

# 2. Create Python Virtual Environment

python -m venv venv

# 3. Activate Virtual Environment

## powershell
.\venv\Scripts\Activate.ps1

## git bash / MINGW64
source venv/Scripts/activate

# 4. Install Dependencies

pip install -r requirements.txt

## or, if installing as a package for CLI usage:
pip install -e .
```

## Usage

```bash
python -m md_dedup.cli --input <input_file.md> --output <output_file.md>

# or, if installed with `pip install -e .`:
md-dedup --input <input_file.md> --output <output_file.md>
```

## Functionality:

1. **Load Markdown** – Reads input file and splits into sections by headings
2. **Deduplicate** – Removes repeated lines within each section
3. **Merge overlapping sections** – Uses OpenAI API to merge sections intelligently without losing information
4. **Global consistency** – Removes duplicate lines across all sections
5. **Save Markdown** – Writes cleaned output to file

**Result:** A Markdown file that is **concise, non-redundant, and readable**, ready for documentation, portfolio, or publication.

## Design Decisions

- **Cloud LLM via OpenAI** – Simplifies setup; free-tier sufficient for prototyping
- **CLI-first design** – Lightweight and easily portable
- **Modular architecture** – Easy to extend with new passes, AI logic, or file types
- **Python package structure** – Allows reuse and testing (`python -m md_dedup.cli`)

## Next Steps

- Support for **local LLM** if offline usage is needed
- Additional **text preprocessing passes** (e.g., formatting, grammar check)
- **Unit tests** for automated validation
- **Analytics** for processed Markdown (lines removed, tokens used, etc.)

## License

This project is licensed under **CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)**:

- Free to **view, run, and experiment** for educational purposes
- **Non-commercial use only**
- Commercial use, redistribution, or sale requires explicit permission from the author

For full license text, see [LICENSE](./LICENSE)
