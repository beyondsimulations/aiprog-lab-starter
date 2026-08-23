# Academic-writing skills

Eight self-contained "Agent Skills" for editing academic and technical prose, adapted for this course from a personal Claude Code skill set. Each is a `SKILL.md` file with YAML frontmatter (`name`, `description` — the description states when the skill applies) followed by an instruction body an agent follows when applying it to a piece of text. They are tool-agnostic: nothing in them depends on Claude Code specifically, and each is self-contained (no references to files outside the skill itself).

| Skill | Use it to... |
|---|---|
| [`academic-grammar`](academic-grammar/SKILL.md) | Check grammar, wording, and scientific-writing conventions (formal tone, precise verbs, no contractions). |
| [`conciseness`](conciseness/SKILL.md) | Cut wordiness, redundant phrases, and filler ("in order to" → "to") without losing technical meaning. |
| [`hedging-language`](hedging-language/SKILL.md) | Check that claims are appropriately qualified — flag overclaiming ("proves", "always") and excessive hedging alike. |
| [`literature-grounder`](literature-grounder/SKILL.md) | Find claims that need a citation and ground them in your project's literature/`references.bib`; never invents sources. |
| [`acronym-check`](acronym-check/SKILL.md) | Verify that acronyms are defined on first use and used consistently; flag undefined, orphaned, or over-used acronyms. |
| [`term-consistency`](term-consistency/SKILL.md) | Check that the same concept always uses the same term (spelling, hyphenation, capitalization); flag synonym drift. |
| [`tense-consistency`](tense-consistency/SKILL.md) | Check verb tense against section conventions (past for methods/results, present for intro/conclusions) and within paragraphs. |
| [`humanizer`](humanizer/SKILL.md) | Remove common signs of AI-generated writing (inflated significance, rule-of-three, em-dash chains, AI vocabulary) and add a human voice. |

Every skill ends with the same instruction: **show proposed edits as a diff or a list, not a wholesale rewrite of the document.** This keeps you in control of what actually changes — you review and accept edits individually rather than trusting a full regeneration.

One exception: `humanizer` works differently from the others. It drafts and revises text (adding a human voice) rather than only flagging issues, and it keeps its detailed pattern catalog in [`humanizer/reference.md`](humanizer/reference.md) to keep the skill file itself lean.

A related but separate skill, [`reference-lookup`](../reference-lookup/SKILL.md), lives outside this writing pack: it looks up a paper's DOI and metadata from its title via the keyless OpenAlex API and cross-checks against Crossref. It sits apart because it runs code and calls an external API rather than editing prose.

Four more **discipline-specific** editors (`math-notation`, `algorithm-check`, `model-formulation`, `english-variant`) are offered separately in [`../writing-extras/`](../writing-extras/README.md) — they help only some fields, so grab the ones that fit your work rather than installing them for everyone.

## Installing in OpenCode

OpenCode discovers Claude Code-compatible skills at `.claude/skills/<name>/SKILL.md` (project-level) or `~/.claude/skills/<name>/SKILL.md` (global) — no conversion needed. To install these eight skills into your project, copy the `skills/writing/` folder into `.claude/skills/` from the repository root:

```bash
mkdir -p .claude/skills
cp -r skills/writing/* .claude/skills/
```

After that, ask your agent to apply a skill by name, e.g. "Apply the conciseness skill to the introduction of `report.md`; show the diff, don't write yet." OpenCode's `skill` tool (or your agent's equivalent skill-invocation mechanism) picks the matching `SKILL.md` by its `description` field, or you can name it directly.

> **Verify against current OpenCode docs before class.** Skill discovery paths and invocation details are version-sensitive and OpenCode moves fast. Check the [official skills docs](https://opencode.ai/docs/skills/) if anything above doesn't match what you see.

## License

CC BY-SA 4.0, matching the rest of this course site.
