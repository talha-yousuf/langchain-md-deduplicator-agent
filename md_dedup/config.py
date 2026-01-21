# config.py

# Configuration for LangChain/OpenAI

MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0

# Similarity and merging thresholds
SIMILARITY_THRESHOLD = 0.7  # Sections above this will be considered for merging
SEMANTIC_DEDUP_THRESHOLD = 0.85  # Lines above this similarity are duplicates

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in environment variables")
