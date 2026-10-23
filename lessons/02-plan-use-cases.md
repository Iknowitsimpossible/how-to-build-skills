# 2. Plan your use cases

The most common way a skill fails isn't bad writing. It's being built for a vague idea ("help with docs") instead of specific situations. Before writing any `SKILL.md`, write down **two or three concrete use cases**.

## Write use cases, not features

A use case has four parts: what the user says, what the agent does, in what order, and what the user ends up with.

```text
Use case: Review a finished project's README
Trigger:  "review my README", "make this presentable for GitHub"
Steps:    1. Check the project is committed and pushed
          2. Read manifests, scripts, and deploy configs
          3. Decide the project type (game, library, CLI, ...)
          4. Compare the README against that type's template
          5. Write suggestions to a separate file; don't overwrite
Result:   A ranked list of ready-to-paste fixes; README untouched
```

That's a use case from [the case study](../examples/03-readme-organizer/). Its pushed-state check and suggestions-only workflow are choices for that example, not requirements for README work generally. Preserve the user's scope and any authorization already given.

Questions to answer for each use case:

- What is the user trying to get done?
- What steps does that take, and does the order matter?
- What tools does the agent need: just reading and writing files, running commands, or an MCP server?
- What do *you* know about doing this well that the agent wouldn't? That knowledge is the real value of the skill.

One well-defined use case can justify a skill. Split a skill when its capabilities need different discovery descriptions or unrelated instructions, not at a fixed use-case count.

## Three kinds of skills

Most skills fall into one of three categories. Knowing which you're building tells you what to focus on.

| Category | What it does | Focus on | Example |
|---|---|---|---|
| **Creating documents and assets** | Produces consistent output: documents, slides, code, designs | Templates, style rules, a quality checklist before finishing | [`flashcard-maker`](../examples/02-with-references/flashcard-maker/), readme-organizer |
| **Automating a workflow** | Runs a process with explicit dependencies and checks | Ordered steps, checks between steps, what to do when a step fails | [`commit-message`](../examples/01-minimal/commit-message/) |
| **Enhancing an MCP server** | Teaches the agent to use a connected service well | Which tool calls to make, in what order, and how to handle API errors | A skill that turns "plan this sprint" into the right sequence of Linear calls |

## Define success before you build

Decide how you'll know the skill works. Rough targets are fine; you're aiming for "clearly better", not a precise score.

**Things you can count:**

- **Triggering:** of 10 to 20 requests that should use the skill, how many actually load it? Aim for about 9 in 10.
- **Effort:** run the same task with and without the skill. Does the skill version take fewer messages, tool calls, or corrections?
- **Errors:** does the workflow finish without failed commands or API calls?

**Things you judge:**

- Did you have to step in and redirect the agent?
- If you run the same request 3 times, are the results consistent?
- Could someone who's never seen the skill get a good result on the first try?

Write these down now. [Lesson 6](06-testing.md) turns them into tests.

## Exercise

Pick a task you've explained to an AI agent more than twice. Write two use cases for it in the format above, and one success criterion you could count.

## Your deliverable

One concrete use case and a quality criterion.

**Self-check:** Does success describe a useful result, rather than a fixed number of steps?

**Next:** [3. Write the frontmatter](03-frontmatter.md)
