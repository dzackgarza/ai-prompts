[![Ko-Fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I57UKJ8)

# AI Prompts

Centralized reusable prompt library consumed by `llm-runner`, `opencode-plugin-prompt-transformer`, and other tools via the `PROMPTS_DIR` environment variable or the `ai-prompts` CLI.

## Features

- Catalog of reusable prompt templates organized by slug
- CLI for listing and retrieving prompt documents with metadata
- `uvx`-installable with no local setup required for read-only use

## Setup

```bash
direnv allow
just install
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

```bash
just check
```
