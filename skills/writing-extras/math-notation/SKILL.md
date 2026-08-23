---
name: math-notation
description: Checks mathematical notation for consistency and correctness. Use when reviewing equations, symbols, and mathematical expressions in academic writing.
---

Review the provided text for mathematical notation consistency and correctness.

## What to Check

### 1. Variable/Symbol Consistency
- Same quantity should use same symbol throughout
- No symbol reused for different meanings
- Related quantities should use related notation (e.g., x for variable, X for set)

### 2. Symbol Definition
- Every symbol defined before or at first use
- Definitions are clear and unambiguous
- No "orphan" symbols (used but never defined)

### 3. Notation Style Consistency
| Element | Check for consistency |
|---------|----------------------|
| Vectors | Bold **v** vs. arrow v⃗ vs. underline |
| Matrices | Bold uppercase **A** vs. regular A |
| Sets | Calligraphic 𝒜 vs. blackboard 𝔸 vs. regular |
| Functions | f(x) vs. f_x vs. fx |
| Indices | i,j,k usage and ranges |
| Summations | Σ bounds notation |
| Norms | ‖·‖ vs. |·| |

### 4. Index Conventions
- Index variables used consistently (i for rows, j for columns, etc.)
- Index ranges clearly specified
- No index collisions (same index used for different ranges)

### 5. Equation References
- All numbered equations referenced in text
- References match actual equation numbers
- No dangling references to non-existent equations

### 6. Units and Dimensions
- Physical quantities include units where appropriate
- Dimensional consistency in equations
- Unit notation consistent (km vs. kilometers)

## Output Format

### Inline Suggestions

For each issue found:

**Equation/Section:** [location]
- Symbol: [the symbol in question]
- Problem: [what's inconsistent or undefined]
- Suggestion: [how to fix]

### Summary

#### Symbol Inventory

| Symbol | Meaning | First Defined | Consistent? |
|--------|---------|---------------|-------------|
| [sym] | [meaning] | [location] | [Yes/No] |

#### Issues Found

| Issue Type | Count | Examples |
|------------|-------|----------|
| Undefined symbols | N | [list] |
| Inconsistent notation | N | [list] |
| Equation reference errors | N | [list] |
| Index conflicts | N | [list] |

## Guidelines

- Field-specific conventions may override general rules
- Some notation variation is acceptable for clarity
- Focus on issues that affect reader comprehension
- Consider the target audience's familiarity with notation

- Show proposed edits as a diff or a list; do not rewrite the document wholesale.
