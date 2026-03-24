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

### Adding a New Prompt

1. Create the template in `prompts/` with YAML frontmatter and Jinja2 body
2. Use relative paths from the template location: `{% include "../../system/modules/..." %}`
3. Place shared guidelines in `prompts/system/modules/`

### Testing Locally

```bash
# Render a template and verify includes expand
export PROMPTS_DIR=prompts
echo '{"template": {"path": "/path/to/prompt.md"}, "bindings": {"data": {}}}' > /tmp/render.json
uvx --from git+https://github.com/dzackgarza/llm-templating-engine.git llm-template-render \
  --input /tmp/render.json --output /tmp/response.json

# Check output
cat /tmp/response.json | jq '.rendered.document'
```

### Publishing

```bash
git add <your-files>
git commit -m "add: description"
git push
```

Then retrieve via uvx:

```bash
uvx --from git+https://github.com/dzackgarza/ai-prompts.git ai-prompts get <slug>
```

### Important Notes

- **Includes must be in the body**, not in frontmatter fields like `system_template`. The engine only processes the body through Jinja2.
- Use relative paths from the template's directory: `../../system/modules/guidelines.md`
