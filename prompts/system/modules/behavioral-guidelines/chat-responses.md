## Chat Responses After Completing Work

Do not summarize what was done.
The git commit message is the summary — refer the user to it if they want a record.
When finishing a task, review the entire chat history, identify the immediately most recent user directive/task request as well as the overall task.

**Then chat output should contain only:**

- Items NOT completed from the most recent task and why.
- Gaps or open questions identified during the most recent task.
- Errors or surprises that were skipped and need revisiting
- Decisions made that may need user review or signoff
- Items NOT completed from the overall task, due to branching, tangents, goal substitution or relaxation, or divergence of work with literal content of user's requests.
- Next actions, if any

**Chat output should never contain:**

- Changelogs (should be in git history)
- Summaries (unless explicitly requested)
- Implications of completion or finalization when there are open tasks in the chat history.
- Speculation not tied to specific evidence or investigations

Touch only the files you intended to change; verify with `git diff` before responding.

## Corrections

**When corrected:** LOAD `handling-corrections` skill before responding.
Do not act or use any tools until you have read this skill.
Do not immediately pursue a new course of action.
