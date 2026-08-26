# Discipline-specific writing skills (optional)

These are extra [Agent Skills](../writing/README.md) that are useful for *some*
fields but not everyone — so they are kept out of the default writing pack and
offered here to grab only if they fit your work. They follow the same rules as
the core pack: each is a self-contained `SKILL.md`, and each ends with "show
proposed edits as a diff or a list; do not rewrite the document wholesale."

| Skill | Grab it if you... |
|---|---|
| [`math-notation`](math-notation/SKILL.md) | ...write equations — checks symbols, operators, and notation for consistency and correctness. |
| [`algorithm-check`](algorithm-check/SKILL.md) | ...present pseudocode or algorithms — checks logic, termination, edge cases, and complexity claims. |
| [`model-formulation`](model-formulation/SKILL.md) | ...write optimization or mathematical models — checks objective, constraints, and variable definitions. |
| [`english-variant`](english-variant/SKILL.md) | ...mix sources or co-authors across US/UK English — flags spelling and vocabulary inconsistencies. |

## Installing one

Copy just the skill(s) you want into your project's skill directory (the same
place the core pack goes):

```bash
# from a clone of this repository (course-site/):
cp -r course-site/skills/writing-extras/math-notation .claude/skills/
```

Or download a single `SKILL.md` straight from the repository on GitHub and drop
it into `.claude/skills/<name>/SKILL.md`. Restart OpenCode (or start a fresh
session) so it picks up the new skill, then invoke it by name like any other.
