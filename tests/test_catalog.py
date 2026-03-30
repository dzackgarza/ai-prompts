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

    assert len(prompts) >= 45
    assert slugs[0] == "interactive-agents/autonomous"
    assert "interactive-agents/interactive" in slugs
    assert "micro-agents/transcript-summary" in slugs
    assert "sub-agents/general" in slugs
    assert "system/AGENTS" in slugs
    assert not any(slug.startswith("system/modules/") for slug in slugs)


def test_get_prompt_expands_support_includes_without_leaking_include_tags() -> None:
    prompt = get_prompt("interactive-agents/lattice-orchestrator")

    assert prompt.name == "(Lattice) Orchestrator"
    assert "Primary Failure Mode: No Commit Created" in prompt.body
    assert "{% include" not in prompt.text


def test_get_prompt_expands_system_agents_includes() -> None:
    prompt = get_prompt("system/AGENTS")

    assert prompt.name == "AGENTS.md"
    assert "CRITICAL DIRECTIVE" in prompt.body
    assert "{% include" not in prompt.text


def test_get_prompt_expands_interactive_and_subagent_shared_includes() -> None:
    interactive = get_prompt("interactive-agents/interactive")
    general = get_prompt("sub-agents/general")
    correction_finder_ask = get_prompt("sub-agents/correction-finder-ask")

    assert "CRITICAL DIRECTIVE" in interactive.body
    assert "Repo Workflows" in interactive.body
    assert "{% include" not in interactive.text
    assert "CRITICAL DIRECTIVE" in general.body
    assert "{% include" not in general.text
    assert "Strong evidence is required." in correction_finder_ask.body
    assert "{% include" not in correction_finder_ask.text


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
