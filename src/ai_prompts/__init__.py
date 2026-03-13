"""Slug-based access to the shared prompt library."""

from ai_prompts.catalog import PromptEntry, PromptNotFoundError, get_prompt, list_prompts

__all__ = ["PromptEntry", "PromptNotFoundError", "get_prompt", "list_prompts"]
