---
name: term-consistency
description: Checks for consistent use of technical terminology throughout academic writing. Use when reviewing whether the same concepts use the same terms consistently.
---

Review the provided academic text for technical terminology consistency.

## What to Check

1. **Synonymous terms**: Same concept referred to by different names
   - Example: "model" vs. "framework" vs. "approach" for the same thing
   - Example: "users" vs. "participants" vs. "subjects"
   - Example: "algorithm" vs. "method" vs. "procedure"

2. **Abbreviation/full form mixing**: Inconsistent use after definition
   - Example: "machine learning" and "ML" used interchangeably without pattern

3. **Capitalization consistency**:
   - Example: "Random Forest" vs. "random forest"
   - Example: "Internet" vs. "internet"

4. **Hyphenation consistency**:
   - Example: "real-time" vs. "real time" vs. "realtime"
   - Example: "decision-making" vs. "decision making"

5. **Spelling variants**:
   - Example: "dataset" vs. "data set"
   - Example: "email" vs. "e-mail"

## Analysis Approach

1. Extract all technical terms and noun phrases
2. Group potentially synonymous terms
3. Check frequency and distribution
4. Identify the dominant term for each concept
5. Flag deviations from dominant usage

## Output Format

### Inline Suggestions

For each inconsistency found:

**Line/Section:** "variant term" → "preferred term"
- Concept: [what it refers to]
- Dominant usage: [preferred term] (N occurrences)

### Summary

| Concept | Variants Found | Recommended Term | Occurrences |
|---------|----------------|------------------|-------------|
| [concept] | term1, term2, term3 | [most frequent] | N, M, P |

### Terminology Decisions Needed

For terms with near-equal frequency, list options:
- [Concept]: "term1" (N uses) vs. "term2" (M uses) — recommend: [choice + rationale]

## Guidelines

- First occurrence of a term often sets the standard
- Some variation is acceptable (e.g., avoiding repetition in adjacent sentences)
- Field-specific conventions may dictate certain terms
- Defined abbreviations should be used consistently after definition
- Show proposed edits as a diff or a list; do not rewrite the document wholesale.
