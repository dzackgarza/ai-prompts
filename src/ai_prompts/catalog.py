"""Prompt catalog access for the centralized prompt library."""

from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

_PROMPT_ROOTS = ("interactive-agents", "sub-agents", "micro-agents", "system")
_INCLUDE_RE = re.compile(r"""{%\s*include\s+['"](.+?)['"]\s*%}""")


class PromptNotFoundError(FileNotFoundError):
    """Raised when a prompt slug is not present in the catalog."""


@dataclass(frozen=True)
class PromptEntry:
    """One prompt document plus its resolved metadata."""

    slug: str
    name: str | None
    description: str | None
    mode: str | None
    model: str | None
    text: str
    frontmatter: dict[str, Any]
    body: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)

def _library_root():
    if prompts_dir := os.getenv("PROMPTS_DIR"):
        return Path(prompts_dir)

    package_root = resources.files("ai_prompts").joinpath("library")
    if package_root.exists():
        return package_root

    repo_root = Path(__file__).resolve().parents[2]
    prompts_root = repo_root / "prompts"
    if prompts_root.exists():
        return prompts_root

    return package_root


def _iter_prompt_files():
    root = _library_root()
    for prompt_root in _PROMPT_ROOTS:
        base = root.joinpath(prompt_root)
        for path in sorted(base.rglob("*.md")):
            if any(part == "support" for part in path.parts):
                continue
            yield path


def _slug_for_resource(resource_path) -> str:
    root = _library_root()
    relative = Path(str(resource_path.relative_to(root)))
    if relative.name == "prompt.md":
        return relative.parent.as_posix()
    return relative.with_suffix("").as_posix()


def _resource_for_slug(slug: str):
    normalized = slug.strip().strip("/")
    if not normalized:
        raise PromptNotFoundError("Prompt slug must not be empty.")
    root = _library_root()
    for candidate in (
        root.joinpath(f"{normalized}.md"),
        root.joinpath(normalized, "prompt.md"),
    ):
        if candidate.is_file():
            return candidate
    raise PromptNotFoundError(f"Unknown prompt slug: {slug}")


def _split_frontmatter(document: str) -> tuple[dict[str, Any], str]:
    if not document.startswith("---\n"):
        return {}, document
    end_idx = document.find("\n---\n", 4)
    if end_idx == -1:
        raise ValueError("Prompt document is missing a closing frontmatter marker.")
    metadata = yaml.safe_load(document[4:end_idx]) or {}
    if not isinstance(metadata, dict):
        raise ValueError("Prompt frontmatter must be a mapping.")
    body = document[end_idx + len("\n---\n") :].lstrip("\n")
    return metadata, body


def _join_frontmatter(metadata: dict[str, Any], body: str) -> str:
    if not metadata:
        return body
    dumped = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=False).strip()
    return f"---\n{dumped}\n---\n\n{body.lstrip()}"


def _expand_includes(body: str, resource, seen: set[str]) -> str:
    root = _library_root()

    def replace(match: re.Match[str]) -> str:
        include_name = match.group(1)
        # Resolve from prompts root, not from the template's directory
        # "./foo.md" or "foo.md" -> resolve from root
        # "../foo.md" or "/absolute/foo.md" -> resolve from parent (fallback)
        if include_name.startswith("..") or Path(include_name).is_absolute():
            include_resource = resource.parent.joinpath(include_name)
        else:
            include_resource = root.joinpath(include_name)
        include_key = str(include_resource)
        if include_key in seen:
            raise ValueError(f"Cyclic prompt include detected: {include_name}")
        if not include_resource.is_file():
            raise PromptNotFoundError(
                f"Included prompt resource not found: {include_name}"
            )
        include_text = include_resource.read_text()
        _, include_body = _split_frontmatter(include_text)
        return _expand_includes(include_body, include_resource, seen | {include_key})

    return _INCLUDE_RE.sub(replace, body)


def list_prompts() -> list[PromptEntry]:
    """Return the full prompt catalog in slug order."""
    return [get_prompt(_slug_for_resource(path)) for path in _iter_prompt_files()]


def get_prompt(slug: str) -> PromptEntry:
    """Return one rendered prompt document by slug."""
    resource = _resource_for_slug(slug)
    document = resource.read_text()
    frontmatter, body = _split_frontmatter(document)
    body = _expand_includes(body, resource, {str(resource)})
    document = _join_frontmatter(frontmatter, body)
    return PromptEntry(
        slug=slug,
        name=frontmatter.get("name"),
        description=frontmatter.get("description"),
        mode=frontmatter.get("mode"),
        model=frontmatter.get("model"),
        text=document,
        frontmatter=frontmatter,
        body=body,
    )
