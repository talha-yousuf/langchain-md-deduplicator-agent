# Configuration for LangChain/OpenAI

MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in environment variables")
