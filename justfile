set fallback := true
default:
@just --list

install:
uv sync --group dev

test:
PROMPTS_DIR=prompts uv run pytest

typecheck:
PROMPTS_DIR=prompts uv run mypy src

check: typecheck test

build:
uv build

# Bump patch version, commit, and tag
bump-patch: check
uv version --bump patch
git add pyproject.toml uv.lock
git commit -m "chore: bump version to v$(uv version | awk '{print $2}')"
git tag "v$(uv version | awk '{print $2}')"

# Bump minor version, commit, and tag
bump-minor: check
uv version --bump minor
git add pyproject.toml uv.lock
git commit -m "chore: bump version to v$(uv version | awk '{print $2}')"
git tag "v$(uv version | awk '{print $2}')"

# Push commits and tags to trigger CI release
release: check
git push && git push --tags

# Compile all agent templates to markdown files
compile-agents:
#!/usr/bin/env bash
set -euo pipefail

# Create output directory
mkdir -p compiled-agents

# Export PROMPTS_DIR for the templating engine
export PROMPTS_DIR="prompts"

# Process interactive-agents
for template in prompts/interactive-agents/*.md; do
name=$(basename "$template" .md)
echo "Rendering $template..."

# Create JSON request with actual template path
cat > "/tmp/render-request-$name.json" << EOF
{
"template": {
"path": "$template"
},
"bindings": {
"data": {}
}
}
EOF

uvx --from git+https://github.com/dzackgarza/llm-templating-engine.git llm-template-render \
--input "/tmp/render-request-$name.json" \
--output "/tmp/render-response-$name.json"

# Extract the rendered document (frontmatter + body)
jq -r '.rendered.document' "/tmp/render-response-$name.json" > "compiled-agents/$name.md"
done

# Process sub-agents
for template in prompts/sub-agents/*.md; do
name=$(basename "$template" .md)
echo "Rendering $template..."

# Create JSON request with actual template path
cat > "/tmp/render-request-$name.json" << EOF
{
"template": {
"path": "$template"
},
"bindings": {
"data": {}
}
}
EOF

uvx --from git+https://github.com/dzackgarza/llm-templating-engine.git llm-template-render \
--input "/tmp/render-request-$name.json" \
--output "/tmp/render-response-$name.json"

# Extract the rendered document (frontmatter + body)
jq -r '.rendered.document' "/tmp/render-response-$name.json" > "compiled-agents/$name.md"
done

echo "Compiled agents written to compiled-agents/"
ls -la compiled-agents/
