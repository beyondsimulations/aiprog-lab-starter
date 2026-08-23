---
name: tense-consistency
description: Checks for consistent verb tense usage in academic writing. Use when reviewing papers for tense consistency or when streamlining between present and past tense.
---

Review the provided academic text for verb tense consistency.

## Tense Conventions by Section

| Section | Recommended Tense | Rationale |
|---------|-------------------|-----------|
| Abstract | Mix: past (methods/results), present (conclusions) | Summarizes completed work + current significance |
| Introduction | Present | Establishes current state of knowledge |
| Literature Review | Present or past | Present for current relevance, past for historical context |
| Methods | Past | Describes what was done |
| Results | Past | Reports what was found |
| Discussion | Mix: past (your findings), present (interpretations) | Connects findings to broader context |
| Conclusions | Present | States current implications |

## What to Check

1. **Within-paragraph consistency**: Avoid switching tenses mid-paragraph without reason
2. **Section-appropriate tense**: Flag when tense doesn't match section conventions
3. **Logical shifts**: Some tense shifts are intentional (e.g., "We found X [past]. This suggests Y [present].")
4. **Passive vs. active consistency**: Note if passive/active voice shifts affect tense clarity

## Output Format

### Inline Suggestions

For each issue found:

**Line/Section:** "original text" → "suggested text"
- Reason: [explain why tense should change]

### Summary

| Section | Current Tense Pattern | Recommendation |
|---------|----------------------|----------------|
| [section] | [observed pattern] | [suggestion] |

## Guidelines

- Don't flag intentional, logical tense shifts
- Consider the context before suggesting changes
- Note when a section consistently uses non-standard tense (might be journal preference)
- Show proposed edits as a diff or a list; do not rewrite the document wholesale.
