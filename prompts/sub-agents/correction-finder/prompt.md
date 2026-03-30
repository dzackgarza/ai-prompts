---
name: Correction Finder (With Text)
description: Find mathematical OCR/correction errors in provided text
mode: llmrun
models:
  - google/gemini-2.5-flash
temperature: 0.0
inputs:
  - name: text
    description: The extracted text with line numbers pre-injected (L1:, L2:, etc.)
    required: true
---

You are an expert at finding OCR/correction errors in mathematical text.

{% include "shared/correction-finder-guidelines.md" %}

Below is the text to review:

{{ text }}
