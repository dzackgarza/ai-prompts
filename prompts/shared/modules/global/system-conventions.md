# Mathematics

## Lattices

Note that `lattice` does NOT mean lattices related to cryptography in any meaningful sense.
A lattice, by definition, is a free $R$-module of finite rank with a (usually nondegenerate) symmetric bilinear form.
This may be definite or indefinite, and is NOT assumed to be positive-definite, embedding in a particular vector space, to have a "basis", to be unimodular, etc.

# Engineering Rules

- **Favor mature dependencies.** Do not reinvent wheels.
- **Iterate, don't replace.** Writing an entire file is rarely correct.
- Run `git diff` after rewrites — see what you lost. If valuable, restore it.

# Memory

Memories store durable, reusable agent context not captured in repository files.

**Store:** Stable operational guidance, environment quirks, cross-session execution context.

**Do not store:** Audit trails, decision logs, changelogs, work summaries. Those belong in git.

# Conventions for this system

- **Read all READMEs and AGENTS.md files** encountered.
- There are many symlinks on this system, check the file type if you find confusing duplication. Reusable agent-facing prompts now live in the `ai-prompts` repo and are consumed by slug; `~/ai/prompts` is reserved for `local_context` overlays and repo-specific guidance.
- Never store or use local secrets or inline them into any shell commands. They must be stored in ~/.envrc, trusted with `direnv allow`, and all projects should have a .envrc file that either sources ~/.envrc directly or uses the `source_up` directive.
  - Project-local envrc files should be tracked via git, and thus never store true secrets, only env vars. If a project truly needs a local secret (rare), then it should be in a gitignore .env file and the envrc file should source it.
- Do not probe secrets files in `.env` and `~/.envrc`. If you need secrets/keys/etc, they will be in your env.
- All projects must have centralized recipes in a justfile and be run with `just`. Always look for one and use its recipes, never bypass them.
  - In particular, all tests, type-checking, builds, publishing, etc must be routed through `just`, never run such processes or commands "manually".
- Dependencies between projects should be routed through github and use `uvx`/`npx -y` calls when possible, or explicitly declared as dependencies. Do not tie across file system boundaries unless absolutely necessary.
- **Never** set env vars inline in shell commands (e.g., `MYSECRET=123 some_command`) — these are visible in the process list. Use env files or exports instead.
- **Before editing any JSON or YAML file: LOAD `config-file-editing` skill.** Never raw-edit config files.
