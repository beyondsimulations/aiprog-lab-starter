---
name: english-variant
description: Checks for consistency between American and British English spelling and vocabulary. Use when reviewing text for English variant consistency.
---

Review the provided text for American vs. British English consistency.

## Common Differences to Check

### Spelling Patterns

| Pattern | American | British |
|---------|----------|---------|
| -ize/-ise | optimize, organize | optimise, organise |
| -or/-our | color, behavior, favor | colour, behaviour, favour |
| -er/-re | center, meter, fiber | centre, metre, fibre |
| -og/-ogue | catalog, dialog | catalogue, dialogue |
| -ense/-ence | defense, license (n.) | defence, licence (n.) |
| -l-/-ll- | traveled, modeling | travelled, modelling |
| -e-/-ae-/oe- | anemia, fetus | anaemia, foetus |

### Vocabulary Differences

| American | British |
|----------|---------|
| subway | underground/tube |
| elevator | lift |
| truck | lorry |
| apartment | flat |
| math | maths |
| toward | towards |
| gray | grey |

### Punctuation

| American | British |
|----------|---------|
| Periods inside quotes | Periods outside quotes |
| Serial comma (often) | Serial comma (less common) |

## Output Format

### Inline Suggestions

For each inconsistency found:

**Line/Section:** "word" → "word" (to match [American/British])
- Pattern: [which spelling pattern]

### Summary

| Variant | Occurrences | Examples |
|---------|-------------|----------|
| American | N | [words found] |
| British | N | [words found] |

**Recommendation:** Standardize to [American/British] English (majority variant: X%)

## Guidelines

- First, determine which variant dominates the text
- Suggest converting minority spellings to match the majority
- Note if specific terms have discipline-specific conventions
- Flag any words that appear in both variants within the same document

- Show proposed edits as a diff or a list; do not rewrite the document wholesale.
