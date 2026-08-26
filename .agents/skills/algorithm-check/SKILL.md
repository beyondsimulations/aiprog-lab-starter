---
name: algorithm-check
description: Reviews pseudocode and algorithm descriptions for correctness and completeness. Use when checking algorithm logic, termination conditions, and complexity claims.
---

Review the provided algorithm or pseudocode for correctness and completeness.

## What to Check

### 1. Input/Output Specification
- Inputs clearly listed with types/constraints
- Output clearly specified
- Preconditions stated if any
- Postconditions/guarantees stated

### 2. Variable Handling
- All variables initialized before use
- Variable types clear from context
- No unused variables
- Scope is clear (local vs. global)

### 3. Control Flow
- Loop bounds correctly specified
- Loop variables properly initialized and updated
- Termination guaranteed (no infinite loops)
- Base cases for recursion defined
- All branches have defined behavior

### 4. Correctness Indicators
- Loop invariants hold (if stated)
- Edge cases handled:
  - Empty input
  - Single element
  - Boundary values
  - Maximum/minimum cases
- Return statements present in all paths
- Return values match output specification

### 5. Algorithm-Text Consistency
- Algorithm matches prose description
- Referenced line numbers correct
- Variable names consistent with text
- Step descriptions accurate

### 6. Complexity Analysis
- Stated time complexity matches actual algorithm
- Stated space complexity matches actual algorithm
- Best/worst/average case distinguished if relevant
- Complexity notation correct (O, Θ, Ω)

### 7. Style and Clarity
- Consistent indentation showing nesting
- Comments where logic is non-obvious
- Meaningful variable/function names
- Standard pseudocode conventions followed

## Common Issues to Flag

| Issue | Example | Why It Matters |
|-------|---------|----------------|
| Off-by-one | for i = 1 to n (should be n-1?) | Incorrect results |
| Uninitialized | sum used before sum = 0 | Undefined behavior |
| Missing return | function ends without return | Unclear output |
| Wrong complexity | "O(n)" but nested loops | Misleading claims |
| Dead code | Unreachable statements | Confuses readers |

## Output Format

### Inline Suggestions

For each issue found:

**Line/Step:** [location in algorithm]
- Code: [the problematic code/pseudocode]
- Problem: [what's wrong]
- Suggestion: [how to fix]

### Summary

#### Algorithm Structure

| Component | Status | Notes |
|-----------|--------|-------|
| Input specification | [OK/Missing/Incomplete] | |
| Output specification | [OK/Missing/Incomplete] | |
| Initialization | [OK/Issues] | |
| Termination | [Guaranteed/Unclear] | |
| Edge cases | [Handled/Missing] | |
| Complexity claim | [Accurate/Incorrect/Missing] | |

#### Issues Found

| Issue Type | Count | Severity |
|------------|-------|----------|
| Correctness errors | N | High |
| Missing specifications | N | Medium |
| Style issues | N | Low |
| Complexity errors | N | Medium |

## Guidelines

- Focus on logical correctness over style preferences
- Consider the algorithm's stated purpose when evaluating
- Note if the algorithm is a standard one (cite if possible)
- Verify complexity claims carefully with step counting

- Show proposed edits as a diff or a list; do not rewrite the document wholesale.
