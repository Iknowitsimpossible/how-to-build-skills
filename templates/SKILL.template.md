---
name: your-skill-name
description: "[What it does, in one sentence with a verb]. [Key capabilities or file types]. Use when the user says \"[phrase 1]\", \"[phrase 2]\", or \"[phrase 3]\". Do NOT use for [nearby task that belongs to something else]."
license: MIT
metadata:
  author: your-github-username
  version: 0.1.0
---

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

[Specific actions. If the work depends on the situation, give a short decision table and point to the right reference file:]

| If... | Then read |
|---|---|
| [situation A] | `references/[topic-a].md` |
| [situation B] | `references/[topic-b].md` |

### Step 3: [Check the result]

Run `python3 scripts/[check].py [args]` and fix every error it reports. Repeat until it reports none.

Then confirm what a script can't check:

- [ ] [quality criterion 1]
- [ ] [quality criterion 2]

### Step 4: [Report back]

[What to show the user, and what to ask them before doing anything hard to undo.]

## Examples

**Example 1: [common case]**

User says: "[a realistic request]"

Actions:
1. [what the agent does first]
2. [then]

Result: [what the user ends up with]

## Troubleshooting

**[Symptom or error message].** Cause: [why it happens]. Fix: [what to do].
