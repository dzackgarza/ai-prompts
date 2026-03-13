---
name: Transcript Summary
description: Compresses an OpenCode transcript into structured execution notes
kind: llm-run
models:
- groq/llama-3.3-70b-versatile
temperature: 0.0
output_schema:
  title: TranscriptSummary
  type: object
  additionalProperties: false
  required:
  - tool_calls
  - reasoning_steps
  - edits
  - outcome
  properties:
    tool_calls:
      type: array
      items:
        type: object
        additionalProperties: false
        required:
        - tool
        - purpose
        - result
        properties:
          tool:
            type: string
          purpose:
            type: string
          result:
            type: string
    reasoning_steps:
      type: array
      items:
        type: string
    edits:
      type: array
      items:
        type: object
        additionalProperties: false
        required:
        - target
        - rationale
        properties:
          target:
            type: string
          rationale:
            type: string
    outcome:
      type: string
system_template:
  text: |-
    You summarize OpenCode execution transcripts into structured data.

    Rules:
    - Use only facts visible in the transcript.
    - Preserve actual tool ids exactly when they appear.
    - Prefer concise paraphrase over quoting long blocks.
    - Do not invent reasoning, edits, or tool calls that are not present.
    - If a category is absent, return an empty array for it.
    - `outcome` must be one sentence describing the final visible result.
    - `tool_calls` should focus on the most relevant concrete tool actions in execution order.
    - `reasoning_steps` should capture explicit or strongly evidenced inference steps, not generic filler.
    - `edits` should mention the file or target changed and why it was changed.
inputs:
- name: transcript
  description: Structured transcript JSON rendered from opencode-manager
  required: true
---

{% macro truncate_block(text, head=350, tail=175) -%}
{%- set cleaned = (text or "") | trim -%}
{%- if not cleaned -%}
(empty)
{%- elif cleaned | length <= (head + tail + 40) -%}
{{ cleaned }}
{%- else -%}
{{ cleaned[:head] }}

...[truncated {{ cleaned | length - head - tail }} chars]...

{{ cleaned[-tail:] }}
{%- endif -%}
{%- endmacro %}

Analyze this transcript and return the structured summary described in the schema.
Only the rendered transcript below is part of the model input; the bound JSON object is
not shown directly.

<transcript>
Session ID: {{ transcript.sessionID }}
Title: {{ transcript.title }}
Directory: {{ transcript.directory }}

{% for turn in transcript.turns %}
Turn {{ turn.index }} (duration {{ turn.duration }})
User prompt:
{{ turn.userPrompt }}

{% for message in turn.assistantMessages %}
Assistant message {{ message.index }} (finish {{ message.finish }}, duration {{ message.duration }})
{% if message.reasoning %}
Reasoning:
{% for reasoning in message.reasoning %}
- {{ reasoning }}
{% endfor %}
{% endif %}
{% for step in message.steps %}
Step {{ step.index }}: {{ step.heading }} (duration {{ step.duration }})
{% if step.type == "tool" %}
Tool: {{ step.tool }}
Status: {{ step.status }}
Input:
{{ truncate_block(step.inputText) }}
{% if step.outputText %}
Output:
{{ truncate_block(step.outputText) }}
{% endif %}
{% else %}
{{ step.contentText }}
{% endif %}
{% endfor %}
{% if message.text %}
Assistant reply:
{{ message.text }}
{% endif %}

{% endfor %}
{% endfor %}
</transcript>
