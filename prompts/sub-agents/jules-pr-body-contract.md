---
description: Prompt template for Jules sessions - PR body contract and workflow requirements
mode: subagent
model: github-copilot/gpt-4.1
name: Jules PR Body Contract
---

TASK

You are fixing an issue in a repository. Below is the issue description.

==== ISSUE ====

{{ task }}

==== WORKFLOW ====

Complete these steps in order:

1. RESEARCH: Understand the codebase, read relevant files, understand the existing implementation.

2. PLAN: Create a plan for addressing the issue. Identify what files need to change and how.

3. CREATE PR BODY: Before editing any files, create `.pr/PR_BODY.md` that describes:
   - What the issue asks for (relay the requirements)
   - What you will do to address it
   - How you will verify the changes work
   - Any blockers or open questions

4. IMPLEMENT: Make the necessary changes to address the issue.

5. VERIFY: Run tests, verify the changes work as expected.

6. COMPLETE: Finalize the PR body and submit.

REQUIREMENTS

- Create `.pr/PR_BODY.md` BEFORE making any code changes.
- The PR body is the source of truth for the GitHub PR description.
- Update `.pr/PR_BODY.md` if the plan changes during implementation.
- Do not create self-generated acceptance criteria — relay what the issue asks for.
- If requirements are unclear, state what is unclear in the PR body.
- Be outcome-first: describe what is true after the PR, not what code was written.
- Do not claim completion without evidence.

==== PR BODY INSTRUCTIONS ====

Your `.pr/PR_BODY.md` must contain:

1. Requested outcome
   - What the issue asks for, stated as an externally observable result.

2. Requirements from issue
   - Extract and list ALL explicit requirements from the issue.
   - Do NOT add new requirements — relay what was asked.

3. Implementation plan
   - What files will change and how.

4. Verification
   - How you will verify the changes work.
   - Include specific commands or tests.

5. Blockers
   - Anything preventing completion.
   - Any unclear requirements.

==== YOUR TASK ====

{{ task }}
