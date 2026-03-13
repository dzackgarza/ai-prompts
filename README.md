# AI Prompts

Centralized reusable prompt library.

## Setup

```bash
direnv allow
uv sync
```

## Direct Use

```bash
uvx --from git+https://github.com/dzackgarza/ai-prompts.git ai-prompts list --json
uvx --from git+https://github.com/dzackgarza/ai-prompts.git ai-prompts get interactive-agents/minimal --json
```

## Commands

- `ai-prompts list` returns the prompt catalog keyed by slug.
- `ai-prompts get <slug>` returns one prompt document and metadata.

## Development

- `uv sync --group dev`
- `uv run pytest`

---

[![Ko-Fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I57UKJ8)
