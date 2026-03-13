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
  description: Full markdown transcript rendered from opencode-manager
  required: true
---

Analyze this transcript and return the structured summary described in the schema.

<transcript>
{{ transcript }}
</transcript>
