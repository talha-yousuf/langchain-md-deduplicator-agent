# cli.py

import click
from md_dedup.runner import run_pipeline


@click.command()
@click.option(
    "--input", "input_file", required=True, help="Path to input Markdown file"
)
@click.option(
    "--output",
    "output_file",
    required=True,
    help="Path to output cleaned Markdown file",
)
def main(input_file, output_file):
    """
    CLI entry point for Markdown Cleanup Tool.
    """
    run_pipeline(input_file, output_file)


if __name__ == "__main__":
    main()
