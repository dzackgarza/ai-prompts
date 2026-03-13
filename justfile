default:
    @just --list

setup:
    uv sync --group dev

test:
    uv run pytest

check: test

build:
    uv build
