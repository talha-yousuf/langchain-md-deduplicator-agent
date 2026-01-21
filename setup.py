from setuptools import setup, find_packages


setup(
    name="md_dedup",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["langchain", "openai", "rich", "click", "tiktoken"],
    entry_points={
        "console_scripts": [
            "md-dedup=md_dedup.cli:main",
        ],
    },
    python_requires=">=3.10",
    description="Markdown deduplication and cleanup tool using langchain + OpenAI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Talha Yousuf",
    license="Proprietary",
    url="https://github.com/<your-github-username>/md_dedup",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
