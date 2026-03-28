set fallback := true
repo_root := justfile_directory()
python_qc_justfile := "/home/dzack/ai/quality-control/justfile"

default:
    @just test

install:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{repo_root}}"
    exec uv sync --group dev

[private]
_format:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{repo_root}}"
    exec uvx ruff format .

[private]
_lint:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{repo_root}}"
    exec uvx ruff check .

[private]
_typecheck:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{repo_root}}"
    exec env PROMPTS_DIR=prompts uv run mypy src

[private]
_quality-control:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{repo_root}}"
    exec env PROMPTS_DIR=prompts just --justfile "{{python_qc_justfile}}" --working-directory "{{repo_root}}" test

test: _lint _typecheck _quality-control

build:
    uv build

bump-patch: check
    uv version --bump patch
    git add pyproject.toml uv.lock
    git commit -m "chore: bump version to v$(uv version | awk '{print $2}')"
    git tag "v$(uv version | awk '{print $2}')"

bump-minor: check
    uv version --bump minor
    git add pyproject.toml uv.lock
    git commit -m "chore: bump version to v$(uv version | awk '{print $2}')"
    git tag "v$(uv version | awk '{print $2}')"

release: check
    git push && git push --tags

compile-agents:
    #!/usr/bin/env python3
    import json
    import os
    import subprocess
    import sys
    from pathlib import Path

    prompts_dir = Path("prompts")
    output_dir = Path("compiled-agents")
    output_dir.mkdir(exist_ok=True)
    os.environ["PROMPTS_DIR"] = str(prompts_dir)

    template_dirs = [
        prompts_dir / "interactive-agents",
        prompts_dir / "sub-agents",
    ]

    rendered_count = 0
    failed = []

    for template_dir in template_dirs:
        if not template_dir.exists():
            print(f"Skipping {template_dir} (does not exist)")
            continue

        for template_path in template_dir.glob("*.md"):
            name = template_path.stem
            print(f"Rendering {template_path}...")

            request = {
                "template": {"path": str(template_path.absolute())},
                "bindings": {"data": {}},
            }

            request_file = Path(f"/tmp/render-request-{name}.json")
            response_file = Path(f"/tmp/render-response-{name}.json")
            request_file.write_text(json.dumps(request, indent=2))

            result = subprocess.run(
                [
                    "uvx",
                    "--from",
                    "git+https://github.com/dzackgarza/llm-templating-engine.git",
                    "llm-template-render",
                    "--input",
                    str(request_file),
                    "--output",
                    str(response_file),
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                print(f"  ERROR: {result.stderr}")
                failed.append(name)
                continue

            response = json.loads(response_file.read_text())
            if "error" in response:
                print(f"  ERROR: {response['error']['message']}")
                failed.append(name)
                continue

            output_file = output_dir / f"{name}.md"
            output_file.write_text(response["rendered"]["document"])
            rendered_count += 1
            print(f"  -> {output_file}")

    print(f"\nRendered {rendered_count} templates to {output_dir}/")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)
