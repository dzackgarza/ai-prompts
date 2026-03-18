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
