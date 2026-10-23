---
name: your-skill-name
description: "[Specific outcome and when this skill is useful. Add examples or exclusions only to resolve likely ambiguity.]"
license: MIT
metadata:
  author: your-github-username
  version: 0.1.0
---

<!-- Workflow template: delete sections that do not help this task. For a small skill, start with SKILL.minimal.md. -->

# Your Skill Name

[One or two sentences: the outcome this skill produces and what "good" looks like.]

## Important

- [The rule that, if broken, ruins the result. Put it here, not in step 5.]
- [A second hard rule, if you have one. Delete this line if not.]

## Instructions

### Step 1: [Gather what you need]

[What to read or ask first. Name exact files, commands, or questions.]

```bash
[a command the agent should run, if any]
```

### Step 2: [Do the main work]

[Describe the outcome and decision criteria. Prescribe exact actions only when needed for correctness. Delete this table unless conditional references are useful:]

| If... | Then read |
|---|---|
| [situation A] | `references/[topic-a].md` |
| [situation B] | `references/[topic-b].md` |

### Step 3: [Check the result]

[If a checker is warranted, name it and declare its dependencies. Define success and a failure exit: fix errors and recheck, but stop and report a persistent failure or unavailable dependency. Do not invent a script just to fill this section.]

Then confirm what a script can't check:

- [ ] [quality criterion 1]
- [ ] [quality criterion 2]

### Step 4: [Report back]

[Show the result, checks actually performed, and any unresolved issues. Honor authorization already given; ask only for missing decisions or actions beyond the authorized scope.]

## Examples

**Example 1: [common case]**

User says: "[a realistic request]"

Actions:
1. [what the agent does first]
2. [then]

Result: [what the user ends up with]

## Troubleshooting

**[Symptom or error message].** Cause: [why it happens]. Fix: [what to do].
