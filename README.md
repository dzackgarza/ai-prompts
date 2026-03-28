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

## Workflow

### Prompt Sourcing

The library supports two sourcing modes:

1. **Remote (uvx)**: When installed via `uvx`, prompts are fetched from GitHub and read from the package's built-in `library/` directory.

2. **Local Override**: Set `PROMPTS_DIR` to a local directory to use uncommitted prompts (bypasses the GitHub package):

```bash
export PROMPTS_DIR=prompts
ai-prompts get interactive-agents/minimal
```

### Adding a New Prompt

1. Create the template in `prompts/` with YAML frontmatter and Jinja2 body
2. Use **prompts-root-relative** paths for includes (not relative to the template's location):
   
   ```jinja
   {% include "system/modules/hard-rules.md" %}
   ```
   
   This ensures includes work consistently regardless of where the template is located.
3. Place shared guidelines in `prompts/system/modules/`

### Testing Locally

Use the rendering tool to verify templates compile correctly (prompts must be pushed to GitHub to be available via uvx):

```bash
export PROMPTS_DIR=prompts
echo '{"template": {"path": "prompts/interactive-agents/minimal.md"}, "bindings": {"data": {}}}' > /tmp/render.json
uvx --from git+https://github.com/dzackgarza/llm-templating-engine.git llm-template-render \
  --input /tmp/render.json --output /tmp/response.json
cat /tmp/response.json | jq -r '.rendered.document'
```

### Publishing

Push your changes to make prompts available via uvx.

### Compiling Agents

The CLI can be used to build compiled agent files by piping output to other tools:

```bash
# Get a prompt and pipe to a compiler
uvx --from git+https://github.com/dzackgarza/ai-prompts.git ai-prompts get interactive-agents/minimal \
  | uv run opencode-permission-policy-compiler \
  > compiled-agents/minimal.md

# Fetch a specific slug (use --json for structured output)
uvx --from git+https://github.com/dzackgarza/ai-prompts.git ai-prompts get interactive-agents/autonomous --json
```

### Important Notes

- **Includes must be in the body**, not in frontmatter fields like `system_template`. The engine only processes the body through Jinja2.
- Include paths are resolved from the prompts root (not relative to the template location).
