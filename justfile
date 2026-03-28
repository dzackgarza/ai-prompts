set fallback := true
repo_root := justfile_directory()
qc_justfile := env_var_or_default("QC_JUSTFILE", "/home/dzack/ai/quality-control/justfile")
ai_justfile := env_var_or_default("AI_JUSTFILE", "/home/dzack/ai/justfile")

default:
    @just test

install:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{repo_root}}"
    exec uv sync --group dev

test:
    @just --justfile "{{ qc_justfile }}" --working-directory "{{ repo_root }}" test

build:
    uv build

bump-patch: test
    uv version --bump patch
    git add pyproject.toml uv.lock
    git commit -m "chore: bump version to v$(uv version | awk '{print $2}')"
    git tag "v$(uv version | awk '{print $2}')"

bump-minor: test
    uv version --bump minor
    git add pyproject.toml uv.lock
    git commit -m "chore: bump version to v$(uv version | awk '{print $2}')"
    git tag "v$(uv version | awk '{print $2}')"

release: test
    git push && git push --tags

compile-agents:
    @just --justfile "{{ ai_justfile }}" --working-directory "{{ repo_root }}" build-agents
