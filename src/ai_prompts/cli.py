"""CLI for listing and retrieving centralized prompts."""

from __future__ import annotations

import json

import typer

from ai_prompts import PromptNotFoundError, get_prompt, list_prompts


app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command("list")
def list_command(json_output: bool = typer.Option(False, "--json", help="Emit JSON.")) -> None:
    """List available prompt slugs."""
    prompts = [prompt.to_dict() for prompt in list_prompts()]
    if json_output:
        typer.echo(json.dumps(prompts, indent=2))
        return
    for prompt in prompts:
        label = prompt["name"] or prompt["slug"]
        typer.echo(f"{prompt['slug']}\t{label}")


@app.command("get")
def get_command(
    slug: str = typer.Argument(..., help="Prompt slug to resolve."),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON."),
) -> None:
    """Return one prompt document."""
    try:
        prompt = get_prompt(slug)
    except PromptNotFoundError as exc:
        raise typer.Exit(1) from exc
    if json_output:
        typer.echo(json.dumps(prompt.to_dict(), indent=2))
        return
    typer.echo(prompt.text)


def main() -> None:
    """Run the CLI."""
    app()
