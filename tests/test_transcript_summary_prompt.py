import json
from pathlib import Path

import tiktoken
from llm_templating_engine import Bindings, RenderTemplateRequest, TemplateReference, render_template

from ai_prompts.catalog import get_prompt


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "transcript_summary_input.json"


def render_transcript_summary_prompt() -> str:
    prompt = get_prompt("micro-agents/transcript-summary")
    transcript = json.loads(FIXTURE_PATH.read_text())
    response = render_template(
        RenderTemplateRequest(
            template=TemplateReference(
                text=prompt.text,
                name="micro-agents/transcript-summary.md",
            ),
            bindings=Bindings(data={"transcript": transcript}),
        )
    )
    return response.rendered.body


def test_transcript_summary_prompt_renders_compact_transcript_view() -> None:
    rendered = render_transcript_summary_prompt()

    assert "Session ID: ses_summary_fixture" in rendered
    assert "Turn 1 (duration 37.000s)" in rendered
    assert "Assistant message 1 (finish tool-calls, duration 4.500s)" in rendered
    assert "Need the README heading before changing the config." in rendered
    assert "The final answer must explain both the inspection and the edit." in rendered
    assert "Assistant reply:" in rendered
    assert "I verified the heading, updated the config, and confirmed the new value." in rendered
    assert "This paragraph is filler" in rendered
    assert "Tail marker README_END" in rendered
    assert "...[truncated " in rendered
    assert "should-not-appear" not in rendered
    assert "snapshot_abc" not in rendered
    assert "9999" not in rendered


def test_transcript_summary_prompt_stays_within_render_budget() -> None:
    rendered = render_transcript_summary_prompt()
    token_count = len(tiktoken.get_encoding("cl100k_base").encode(rendered))

    assert token_count < 900
