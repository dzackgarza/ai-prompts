from ai_prompts.catalog import PromptNotFoundError, get_prompt, list_prompts


def test_missing_slug_raises() -> None:
    try:
        get_prompt("interactive-agents/does-not-exist")
    except PromptNotFoundError:
        return
    raise AssertionError("Expected PromptNotFoundError for a missing slug.")


def test_list_prompts_returns_current_catalog() -> None:
    prompts = list_prompts()
    slugs = [prompt.slug for prompt in prompts]

    assert len(prompts) == 54
    assert slugs[0] == "interactive-agents/interactive"
    assert slugs[-1] == "micro-agents/transcript-summary"
    assert "sub-agents/researcher" in slugs


def test_get_prompt_expands_support_includes_without_leaking_include_tags() -> None:
    prompt = get_prompt("sub-agents/researcher")

    assert prompt.name == "Researcher: Documentation"
    assert "Documentation Discovery Library" in prompt.body
    assert "{% include" not in prompt.text


def test_get_prompt_preserves_runtime_placeholders() -> None:
    prompt = get_prompt("micro-agents/prompt-difficulty-classifier")

    assert "{{ prompt }}" in prompt.text
    assert prompt.frontmatter["kind"] == "llm-run"


def test_transcript_summary_prompt_exposes_structured_output_contract() -> None:
    prompt = get_prompt("micro-agents/transcript-summary")

    assert prompt.name == "Transcript Summary"
    assert prompt.frontmatter["kind"] == "llm-run"
    assert prompt.frontmatter["output_schema"]["required"] == [
        "tool_calls",
        "reasoning_steps",
        "edits",
        "outcome",
    ]
    assert "Session ID: {{ transcript.sessionID }}" in prompt.text
    assert "{% macro truncate_block" in prompt.text
